# Módulo IX. Combinación de estrategias y regímenes de mercado

Este módulo explica cómo el proyecto convierte las señales de varias estrategias en **una sola
señal**, cómo clasifica el mercado en regímenes y cómo mide si dos estrategias dicen lo mismo.
Todo el código está en `src/bybit_quant_lab/signals/` (tres archivos: `combiners.py`,
`regime.py`, `redundancy.py`) y en `Researcher.build_combinations`
(`src/bybit_quant_lab/validation/research.py`).

> **[Hecho]** Las combinaciones se han evaluado solo con datos sintéticos. Los números de este
> módulo describen el **comportamiento del código**, no la calidad de ninguna combinación.

---

## 9.0 Intuición: un comité de opiniones que no son independientes

Imagina un comité de diez personas que vota si conviene comprar. Si las diez leyeron el mismo
periódico, sus diez votos valen poco más que uno. El comité solo aporta algo si sus miembros
tienen **información distinta** y aciertan con alguna frecuencia.

Traducido al proyecto:

- Cada estrategia emite un **estado objetivo** por vela: +1 (largo), −1 (corto) o 0 (fuera).
- Una **combinación** cuenta esos estados con una regla (votación, consenso, pesos) y produce
  **otro estado objetivo** con el mismo formato.
- Si varias estrategias usan la misma información (por ejemplo, cinco de las diez siguen
  tendencias, Módulo VIII), sus votos están **correlacionados** y el consenso es más débil de lo
  que parece.

**[Diseño]** La combinación devuelve exactamente el mismo contrato de columnas que una
estrategia individual (`signal`, `conviction`, `stop_distance`, `take_profit_distance`,
`trailing_distance`). Por eso el motor no distingue entre una estrategia y una combinación.

<!-- cita: src/bybit_quant_lab/signals/combiners.py#L1-L29 -->
`src/bybit_quant_lab/signals/combiners.py` · líneas 1–29

```python
"""Combinación de señales de varias estrategias.

Entrada: un DataFrame de señales normalizadas por estrategia (mismo índice). Cada estrategia
emite su **estado** objetivo (-1/0/1); la combinación produce un nuevo estado objetivo con el
mismo contrato, de modo que el motor no distingue entre estrategia individual y combinación.

Modos:

``simple_vote``
    ``net = n_long - n_short``. LONG si ``net >= min_margin``; SHORT si ``net <= -min_margin``.
``weighted_vote``
    ``score = sum(w_i * s_i * c_i) / sum(w_i)`` (``c_i`` = convicción si ``use_conviction``,
    si no 1). LONG si ``score >= threshold``; SHORT si ``score <= -threshold``. Los pesos son
    configurables o se ajustan **solo** con datos de entrenamiento (``fit_weights``); un peso
    mayor no implica mayor capacidad predictiva.
``min_consensus``
    LONG si ``n_long >= min_votes`` (y SHORT análogo).
``category_consensus``
    Una categoría vota LONG si su voto neto interno es > 0. LONG si al menos ``min_categories``
    categorías distintas votan LONG.

Política de conflictos (``conflict_policy``): ``veto`` -> cualquier voto opuesto anula la señal
(FLAT); ``net`` -> se usa el resultado neto del modo. Las estrategias en FLAT o sin datos
(NaN) se consideran abstenciones.

Filtro de régimen (``regime_rules``): antes de votar, la señal de una estrategia se fuerza a
FLAT en las velas cuyo régimen no esté permitido. Reglas por nombre de estrategia, por
categoría o comodín ``*``; cada regla mapea dimensión -> valores permitidos.
"""
```

Términos que aparecen en esa cabecera:

- **Voto**: el estado de una estrategia en una vela. +1 cuenta como voto largo, −1 como voto
  corto y 0 (o dato ausente) como **abstención**.
- **`n_long` / `n_short`**: número de votos largos y cortos en una vela.
- **Voto neto** (`net`): `n_long − n_short`.
- **Umbral / margen**: cantidad mínima de apoyo para que la combinación tome posición.
- **Política de conflictos**: qué hacer cuando hay votos en ambas direcciones.

---

## 9.1 La configuración de una combinación

<!-- cita: src/bybit_quant_lab/signals/combiners.py#L42-L59 -->
`src/bybit_quant_lab/signals/combiners.py` · líneas 42–59

```python
class CombinationConfig(BaseModel):
    """Configuración de una combinación."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    name: str = "combo"
    mode: Literal["simple_vote", "weighted_vote", "min_consensus", "category_consensus"] = (
        "simple_vote"
    )
    members: list[str] | None = None
    min_margin: int = Field(2, ge=1)
    min_votes: int = Field(2, ge=1)
    min_categories: int = Field(2, ge=1)
    weights: dict[str, float] | None = None
    threshold: float = Field(0.3, gt=0, le=1)
    use_conviction: bool = False
    conflict_policy: Literal["veto", "net"] = "veto"
    regime_rules: dict[str, dict[str, list[str]]] | None = None
```

| Campo | Significado | Lo usa |
|---|---|---|
| `name` | Nombre del candidato en informes y registros | todos |
| `mode` | Regla de combinación | todos |
| `members` | Estrategias que votan (`None` = todas las disponibles) | todos |
| `min_margin` | Voto neto mínimo | `simple_vote` |
| `min_votes` | Votos mínimos en una dirección | `min_consensus` |
| `min_categories` | Categorías mínimas de acuerdo | `category_consensus` |
| `weights` | Peso por estrategia (`None` = se ajustan en entrenamiento) | `weighted_vote` |
| `threshold` | Puntuación mínima, en (0, 1] | `weighted_vote` |
| `use_conviction` | Multiplicar cada voto por su convicción | `weighted_vote` |
| `conflict_policy` | `veto` o `net` | todos |
| `regime_rules` | Regímenes permitidos por estrategia/categoría | todos |

**[Diseño]** `extra="forbid"` rechaza campos desconocidos: un error tipográfico en el YAML
(`min_vote` en lugar de `min_votes`) produce un error de validación en lugar de pasar
inadvertido. `frozen=True` impide modificar la configuración después de crearla; los ajustes
se hacen con `model_copy(update=...)`, que devuelve una copia nueva. Recuerda la limitación de
la sección 2.15: esa copia **no se vuelve a validar** (hallazgo B-06). `build_combinations` la usa
para pesos, umbrales y miembros; los valores que introduce (umbrales de 0,2 a 0,5, pesos no
negativos) cumplen las restricciones, pero nada lo comprueba en ese punto.

**Comprobación.** ¿Qué campo se ignora si `mode` es `min_consensus`?

<details><summary>Ver respuesta</summary>

`min_margin`, `min_categories`, `weights`, `threshold` y `use_conviction`. Pydantic los acepta
(tienen valor por defecto), pero `combine_signals` no los lee en esa rama.
</details>

---

## 9.2 El flujo de `combine_signals`, línea a línea

<!-- cita: src/bybit_quant_lab/signals/combiners.py#L86-L110 -->
`src/bybit_quant_lab/signals/combiners.py` · líneas 86–110

```python
def combine_signals(
    frames: dict[str, pd.DataFrame],
    categories: dict[str, str],
    config: CombinationConfig,
    regime: pd.DataFrame | None = None,
) -> pd.DataFrame:
    """Combina señales individuales en un DataFrame con el contrato ``SIGNAL_COLUMNS``."""
    members = config.members or list(frames)
    missing = [m for m in members if m not in frames]
    if missing:
        raise KeyError(f"Estrategias no disponibles para la combinación: {missing}")
    if not members:
        raise ValueError("La combinación necesita al menos una estrategia")
    use = {m: frames[m] for m in members}
    index = next(iter(use.values())).index
    sig = _stack(use, "signal", index).fillna(0).astype(int)
    if config.regime_rules:
        if regime is None:
            raise ValueError("regime_rules requiere el DataFrame de régimen")
        sig = apply_regime_filter(sig, categories, regime, config.regime_rules)
    conv = _stack(use, "conviction", index).fillna(0.0)
    n_long = (sig > 0).sum(axis=1)
    n_short = (sig < 0).sum(axis=1)
    n = len(members)

```

- **93–98:** valida los miembros. Un nombre inexistente lanza `KeyError`; una lista vacía,
  `ValueError`.
- **100:** el índice de referencia es el de la **primera** estrategia. `_stack` (líneas 82–83)
  reindexa todas las demás a ese índice.
- **101:** `fillna(0)`: si a una estrategia le faltan velas, en esas velas **se abstiene**.
- **102–105:** el filtro de régimen se aplica **antes** de votar (sección 9.10).
- **106:** las convicciones, con 0 donde falten.
- **107–108:** `(sig > 0).sum(axis=1)` cuenta, fila a fila, cuántas columnas valen +1. El
  `axis=1` significa "a lo largo de las columnas" (Módulo V).

Después vienen las cuatro ramas (secciones 9.3–9.7) y el cierre común:

<!-- cita: src/bybit_quant_lab/signals/combiners.py#L136-L150 -->
`src/bybit_quant_lab/signals/combiners.py` · líneas 136–150

```python
    out_s = pd.Series(out, index=index).astype("int64")
    if config.conflict_policy == "veto":
        conflict = ((out_s > 0) & (n_short > 0)) | ((out_s < 0) & (n_long > 0))
        out_s[conflict] = 0
    result = empty_signal_frame(index)
    result["signal"] = out_s
    result["conviction"] = pd.Series(strength, index=index).clip(0, 1).where(out_s != 0, 0.0)
    for col in SIGNAL_COLUMNS[2:]:
        values = _stack(use, col, index)
        agree = sig.eq(out_s, axis=0) & (out_s != 0).to_numpy()[:, None]
        result[col] = values.where(agree).median(axis=1, skipna=True)
    no_stop = result["stop_distance"].isna() | (result["stop_distance"] <= 0)
    result.loc[no_stop, "signal"] = 0
    result.loc[result["signal"] == 0, "conviction"] = 0.0
    return result
```

- **137–139:** política `veto` (sección 9.4).
- **142:** la convicción de la combinación es la **fuerza del acuerdo** (`strength`), recortada a
  [0, 1] y a 0 cuando la combinación está fuera.
- **143–146:** stops, take profit y trailing salen de la **mediana** de los miembros que
  **coinciden** con la dirección final (sección 9.8).
- **147–149:** sin stop válido no hay posición (misma regla que en las estrategias individuales,
  Módulo VIII, sección 8.0).

---

## 9.3 Ejemplo de referencia construido a mano

Para todo el módulo se usa el ejemplo de `tests/unit/test_signals.py`: cuatro estrategias
ficticias (`a`, `b`, `c`, `d`) y seis velas.

<!-- cita: tests/unit/test_signals.py#L20-L37 -->
`tests/unit/test_signals.py` · líneas 20–37

```python
IDX = pd.date_range("2024-01-01", periods=6, freq="1h", tz="UTC")
CATS = {"a": "volume", "b": "trend", "c": "indicator", "d": "indicator"}


def _frame(values: list[int], stop: float = 2.0, conv: float = 1.0) -> pd.DataFrame:
    f = empty_signal_frame(IDX)
    f["signal"] = values
    f["conviction"] = [conv if v else 0.0 for v in values]
    f["stop_distance"] = stop
    return f


FRAMES = {
    "a": _frame([1, 1, 1, 0, -1, 1], stop=1.0),
    "b": _frame([1, 1, 0, 0, -1, -1], stop=3.0),
    "c": _frame([1, -1, 0, 0, -1, 0], stop=5.0),
    "d": _frame([0, 0, 1, 1, 0, 0], stop=7.0),
}
```

Tabla de votos (categorías: `a`=volume, `b`=trend, `c` y `d`=indicator):

| Vela | a | b | c | d | `n_long` | `n_short` | `net` |
|---|---|---|---|---|---|---|---|
| 0 | +1 | +1 | +1 | 0 | 3 | 0 | +3 |
| 1 | +1 | +1 | −1 | 0 | 2 | 1 | +1 |
| 2 | +1 | 0 | 0 | +1 | 2 | 0 | +2 |
| 3 | 0 | 0 | 0 | +1 | 1 | 0 | +1 |
| 4 | −1 | −1 | −1 | 0 | 0 | 3 | −3 |
| 5 | +1 | −1 | 0 | 0 | 1 | 1 | 0 |

Las secciones siguientes calculan a mano cada modo sobre esta tabla, y un único bloque
ejecutable al final (sección 9.7) lo comprueba con el código real.

---

## 9.4 Votación simple y política de conflictos

**Regla.** Con `m = min_margin`:

```text
señal = +1  si  net ≥  m
señal = −1  si  net ≤ −m
señal =  0  en otro caso
```

<!-- cita: src/bybit_quant_lab/signals/combiners.py#L111-L114 -->
`src/bybit_quant_lab/signals/combiners.py` · líneas 111–114

```python
    if config.mode == "simple_vote":
        net = n_long - n_short
        out = np.where(net >= config.min_margin, 1, np.where(net <= -config.min_margin, -1, 0))
        strength = net.abs() / n
```

`np.where(cond, a, b)` elige `a` donde la condición es verdadera y `b` donde no; anidado,
implementa el "si / si no si / si no". `strength = |net| / n` es la fracción de miembros que
forman la mayoría neta.

**Cálculo con `m = 2`.** `net` = [+3, +1, +2, +1, −3, 0] → señal antes de conflictos:
[+1, 0, +1, 0, −1, 0].

**Política de conflictos.**

- `net`: se queda con el resultado anterior.
- `veto`: si la combinación quedó larga pero **algún** miembro vota corto (o al revés), la
  señal pasa a 0 (líneas 137–139).

Con `m = 2` no cambia nada: en las velas 0 y 2 nadie vota corto y en la 4 nadie vota largo. El
resultado es [+1, 0, +1, 0, −1, 0] en ambos casos.

**Cálculo con `m = 1`.** Antes de conflictos: [+1, +1, +1, +1, −1, 0].

- Con `net`: [+1, +1, +1, +1, −1, 0].
- Con `veto`: en la vela 1 la estrategia `c` vota −1 → se anula. Resultado:
  [+1, 0, +1, +1, −1, 0].

**Equivalencia que detectó la auditoría (B-01).** Con `veto`, la condición de entrar largo es
`net ≥ m` **y** `n_short = 0`. Si `n_short = 0`, entonces `net = n_long`, así que la condición es
`n_long ≥ m` y `n_short = 0`, que es exactamente `min_consensus` con `min_votes = m` y `veto`.
Las dos combinaciones de la configuración original (`vote_all`, margen 3, y `consensus_3`) eran
**la misma regla con dos nombres**. Eso inflaba el número de pruebas (Módulo XIII, DSR) sin
aportar información. Corrección en `a50ac62`: `vote_all` usa `conflict_policy: net`.

<!-- cita: configs/strategies.yaml#L152-L162 -->
`configs/strategies.yaml` · líneas 152–162

```yaml
combinations:
  - name: vote_all
    mode: simple_vote
    min_margin: 3
    conflict_policy: net         # con 'veto' sería idéntica a consensus_3 (auditoría L1)
  - name: weighted_train
    mode: weighted_vote          # pesos = Sharpe de entrenamiento (no negativos)
    use_conviction: false
  - name: consensus_3
    mode: min_consensus
    min_votes: 3
```

La prueba que documenta la equivalencia y la que impide repetir el error:

<!-- cita: tests/unit/test_audit_statistics.py#L157-L182 -->
`tests/unit/test_audit_statistics.py` · líneas 157–182

```python
def test_configured_combinations_are_not_equivalent() -> None:
    import yaml

    raw = yaml.safe_load((ROOT / "configs/strategies.yaml").read_text())["combinations"]
    cfgs = [CombinationConfig.model_validate(c) for c in raw]

    def key(c: CombinationConfig) -> tuple | None:
        # simple_vote(margen k, veto) ≡ min_consensus(k, veto): n_dir ≥ k y n_opuesto = 0.
        if c.conflict_policy == "veto" and c.members is None and not c.regime_rules:
            if c.mode == "simple_vote":
                return ("veto", c.min_margin)
            if c.mode == "min_consensus":
                return ("veto", c.min_votes)
        return None

    keys = [k for k in map(key, cfgs) if k is not None]
    assert len(keys) == len(set(keys)), "dos combinaciones configuradas son idénticas"


def test_simple_vote_veto_equals_min_consensus_veto(synth: pd.DataFrame) -> None:
    # Documenta la equivalencia matemática que motivó el cambio de configuración.
    frames = {n: create_strategy(n).generate_signals(synth) for n in available_strategies()}
    cats = {n: create_strategy(n).category.value for n in frames}
    a = combine_signals(frames, cats, CombinationConfig(mode="simple_vote", min_margin=3))
    b = combine_signals(frames, cats, CombinationConfig(mode="min_consensus", min_votes=3))
    pd.testing.assert_series_equal(a["signal"], b["signal"])
```

**[Discrepancia]** Si `configs/strategies.yaml` no tiene sección `combinations`, la CLI crea
una combinación por defecto llamada también `vote_all`, pero con la política por defecto
(`veto`), es decir, la versión anterior a la corrección:

<!-- cita: src/bybit_quant_lab/cli.py#L94-L98 -->
`src/bybit_quant_lab/cli.py` · líneas 94–98

```python
def _combos(args: argparse.Namespace) -> list[CombinationConfig]:
    raw = _strategies_file(args).get("combinations") or []
    if not raw:
        return [CombinationConfig(name="vote_all", mode="simple_vote", min_margin=3)]
    return [CombinationConfig.model_validate(c) for c in raw]
```

Con el YAML del repositorio esa rama no se ejecuta.

**Error común.** Pensar que `veto` es "más prudente y por tanto mejor". Es más restrictivo:
reduce operaciones, y con menos operaciones las métricas son más inciertas (Módulo VI).

---

## 9.5 Consenso mínimo

**Regla.** Con `k = min_votes`: largo si `n_long ≥ k` y **no** `n_short ≥ k`; corto en espejo.

<!-- cita: src/bybit_quant_lab/signals/combiners.py#L123-L126 -->
`src/bybit_quant_lab/signals/combiners.py` · líneas 123–126

```python
    elif config.mode == "min_consensus":
        long_ok, short_ok = n_long >= config.min_votes, n_short >= config.min_votes
        out = np.where(long_ok & ~short_ok, 1, np.where(short_ok & ~long_ok, -1, 0))
        strength = pd.Series(np.maximum(n_long, n_short) / n, index=index)
```

La condición `& ~short_ok` resuelve el empate extremo (k votos en cada dirección → 0).

**Cálculo con `k = 3`.** `n_long ≥ 3` solo en la vela 0; `n_short ≥ 3` solo en la vela 4 →
[+1, 0, 0, 0, −1, 0].

**Cálculo con `k = 2` y `veto`.** `n_long ≥ 2` en las velas 0, 1 y 2; `n_short ≥ 2` en la 4 →
[+1, +1, +1, 0, −1, 0]. El veto anula la vela 1 (voto corto de `c`) →
[+1, 0, +1, 0, −1, 0].

**Diferencia con la votación simple (`net`).** `min_consensus` no resta los votos contrarios:
con 3 largos y 2 cortos y `k = 3`, entra largo con `net` aunque el voto neto sea solo +1.

---

## 9.6 Votación ponderada y ajuste de pesos

**Fórmula.** Con pesos `w_i ≥ 0`, estados `s_i ∈ {−1, 0, 1}` y factor `c_i` (la convicción si
`use_conviction`, si no 1):

```text
score = Σ w_i · s_i · c_i / Σ w_i        (score ∈ [−1, 1])
señal = +1 si score ≥ θ,  −1 si score ≤ −θ,  0 en otro caso       (θ = threshold)
```

<!-- cita: src/bybit_quant_lab/signals/combiners.py#L115-L122 -->
`src/bybit_quant_lab/signals/combiners.py` · líneas 115–122

```python
    elif config.mode == "weighted_vote":
        w = pd.Series({m: (config.weights or {}).get(m, 1.0) for m in members}, dtype=float)
        if (w < 0).any() or w.sum() <= 0:
            raise ValueError("Los pesos deben ser no negativos y sumar > 0")
        factor = conv if config.use_conviction else pd.DataFrame(1.0, index=index, columns=members)
        score = (sig * factor).mul(w, axis=1).sum(axis=1) / w.sum()
        out = np.where(score >= config.threshold, 1, np.where(score <= -config.threshold, -1, 0))
        strength = score.abs()
```

- **116:** un miembro sin peso explícito recibe 1.
- **117–118:** pesos negativos o suma no positiva → `ValueError`.
- **120:** `.mul(w, axis=1)` multiplica cada columna por su peso (alineando por nombre).

**Cálculo a mano** (test `test_weighted_vote_uses_weights_and_threshold`): pesos a=3, b=1, c=0,
d=0; θ = 0,5; política `net`. Σw = 4, así que `score = (3·a + 1·b) / 4`:

| Vela | a | b | score | señal |
|---|---|---|---|---|
| 0 | +1 | +1 | (3+1)/4 = 1,00 | +1 |
| 1 | +1 | +1 | 1,00 | +1 |
| 2 | +1 | 0 | 3/4 = 0,75 | +1 |
| 3 | 0 | 0 | 0 | 0 |
| 4 | −1 | −1 | −1,00 | −1 |
| 5 | +1 | −1 | (3−1)/4 = 0,50 | +1 (0,50 ≥ 0,5) |

La vela 5 está justo en el umbral: el `>=` la convierte en larga. Con θ = 0,51 sería 0.

### Cómo se ajustan los pesos (`fit_weights`)

<!-- cita: src/bybit_quant_lab/signals/combiners.py#L153-L169 -->
`src/bybit_quant_lab/signals/combiners.py` · líneas 153–169

```python
def fit_weights(
    train_returns: dict[str, pd.Series], method: Literal["equal", "train_sharpe"] = "train_sharpe"
) -> dict[str, float]:
    """Ajusta pesos con retornos por vela del período de **entrenamiento** exclusivamente.

    ``train_sharpe``: peso = max(Sharpe no anualizado, 0); si todos son 0 se usan pesos iguales.
    """
    if method == "equal":
        return dict.fromkeys(train_returns, 1.0)
    weights = {}
    for name, r in train_returns.items():
        std = float(r.std(ddof=1)) if len(r) > 1 else 0.0
        weights[name] = max(float(r.mean()) / std, 0.0) if std > 0 else 0.0
    total = sum(weights.values())
    if total <= 0:
        return dict.fromkeys(train_returns, 1.0)
    return {k: v / total for k, v in weights.items()}
```

**Intuición.** Cada estrategia recibe un peso proporcional a su Sharpe por vela en
entrenamiento; las de Sharpe negativo reciben 0. Luego se normaliza para que sumen 1.

**Fórmula.** Para la estrategia `i` con retornos por vela `r_i` en entrenamiento:

```text
SR_i = media(r_i) / desv(r_i)        (ddof=1, sin anualizar)
w_i  = max(SR_i, 0) / Σ_j max(SR_j, 0)
```

Si todas tienen `SR ≤ 0`, se usan pesos iguales (líneas 167–168): no hay información para
preferir a ninguna.

**Ejemplo** (test `test_fit_weights_uses_only_given_returns`): `good` = [0,01, 0,02, 0, 0,01]
tiene media 0,01 y desviación > 0 → SR > 0; `bad` tiene media negativa → peso 0. Tras normalizar,
`good` = 1,0 y `bad` = 0.

**[Diseño]** El peso refleja el comportamiento **pasado** en entrenamiento. Un peso alto no
implica capacidad predictiva futura (lo dice la propia cabecera, líneas 14–15).

### Dónde se usan pesos y umbral: `build_combinations`

<!-- cita: src/bybit_quant_lab/validation/research.py#L196-L242 -->
`src/bybit_quant_lab/validation/research.py` · líneas 196–242

```python
    def build_combinations(
        self, singles: dict[str, Candidate], combos: list[CombinationConfig]
    ) -> tuple[dict[str, Candidate], dict[str, Any]]:
        """Construye combinaciones; redundancia, pesos y umbrales se ajustan con entrenamiento."""
        tr = self.segments["train"]
        frames = {n: c.signals for n, c in singles.items()}
        cats = {n: create_strategy(n).category.value for n in singles}
        train_sig = pd.DataFrame(
            {n: f["signal"].iloc[tr.start_pos : tr.end_pos + 1] for n, f in frames.items()}
        )
        corr = signal_correlation(train_sig)
        out: dict[str, Candidate] = {}
        info: dict[str, Any] = {"train_correlation": corr}
        for combo in combos:
            cfg = combo
            if cfg.members is None and cfg.name.startswith("dedup"):
                kept, dropped = select_non_redundant(corr.fillna(0), 0.7)
                cfg = cfg.model_copy(update={"members": kept})
                info["dedup"] = {"kept": kept, "dropped": dropped}
            if cfg.mode == "weighted_vote" and cfg.weights is None:
                members = cfg.members or list(frames)
                train_rets = {
                    n: bar_returns(r.equity["equity"], r.initial_capital)
                    for n in members
                    for r in [self.simulate(singles[n], tr, record=False)]
                }
                cfg = cfg.model_copy(update={"weights": fit_weights(train_rets)})
                info.setdefault("weights", {})[cfg.name] = cfg.weights
                # Umbral elegido en ENTRENAMIENTO (rejilla pequeña y registrada). Validación
                # queda reservada para seleccionar candidatos sin doble uso de los datos.
                best_t, best_s = cfg.threshold, float("-inf")
                for t in (0.2, 0.3, 0.4, 0.5):
                    trial = cfg.model_copy(update={"threshold": t})
                    c = Candidate(
                        f"{cfg.name}@{t}",
                        "combo_trial",
                        combine_signals(frames, cats, trial, self.regime),
                        {},
                    )
                    s = self._score(self.metrics(self.simulate(c, tr)))
                    if s > best_s:
                        best_t, best_s = t, s
                cfg = cfg.model_copy(update={"threshold": best_t})
                info.setdefault("thresholds", {})[cfg.name] = best_t
            sig = combine_signals(frames, cats, cfg, self.regime)
            out[cfg.name] = Candidate(cfg.name, "combination", sig, cfg.model_dump())
        return out, info
```

- **203–206:** la correlación de señales se calcula **solo** con las velas de entrenamiento.
- **211–214:** las combinaciones cuyo nombre empieza por `dedup` y no tienen miembros reciben
  los miembros "no redundantes" (sección 9.11).
- **215–223:** si `weighted_vote` no trae pesos, se simula cada miembro en entrenamiento y se
  ajustan con `fit_weights`.
- **226–239:** se prueba una rejilla de cuatro umbrales (0,2; 0,3; 0,4; 0,5) **en entrenamiento**
  y se elige el de mejor puntuación (`_score`, líneas 188–193: la métrica de selección, o −∞
  con menos de `min_trades_selection` operaciones). Cada ensayo se registra como
  `combo_trial`.

### Historia de una corrección: el umbral se elegía con validación (M-01)

Antes de la auditoría, la línea que puntuaba cada umbral simulaba en **validación**:

```text
-                    s = self._score(self.metrics(self.simulate(c, self.segments["validation"])))
+                    s = self._score(self.metrics(self.simulate(c, tr)))
```

(Extracto de `git show a50ac62 -- src/bybit_quant_lab/validation/research.py`.)

**Por qué era un error.** La validación se usa después para **seleccionar** candidatos. Si el
umbral se elige mirando validación, la combinación ponderada llega a la selección con una
ventaja: su mejor versión ya se escogió con esos mismos datos (doble uso del segmento,
Módulo XIII). La prueba que lo impide comprueba que todos los ensayos `combo_trial` están en
`train`:

<!-- cita: tests/unit/test_audit_statistics.py#L148-L154 -->
`tests/unit/test_audit_statistics.py` · líneas 148–154

```python
def test_combination_thresholds_not_tuned_on_validation(researcher: Researcher) -> None:
    combos = [CombinationConfig(name="weighted", mode="weighted_vote")]
    researcher.run_comparison(combos, ["ema_crossover", "adx_di", "macd_momentum"])
    trials = [r for r in researcher.log.records() if r.get("candidate_kind") == "combo_trial"]
    assert trials, "los ensayos de umbral deben registrarse"
    # El umbral se elige en entrenamiento; validación queda limpia para la selección.
    assert {r["segment"] for r in trials} == {"train"}
```

**[Discrepancia] Dos textos quedaron desactualizados tras la corrección.** El código y
`docs/methodology.md` (punto 3 de la sección 4) dicen "entrenamiento", pero:

- la cabecera del módulo `research.py` sigue diciendo "validación":

<!-- cita: src/bybit_quant_lab/validation/research.py#L7-L8 -->
`src/bybit_quant_lab/validation/research.py` · líneas 7–8

```python
2. Redundancia y pesos de combinación se ajustan **solo con entrenamiento**; los umbrales de
   la votación ponderada se eligen **solo con validación**.
```

- y el informe HTML rotula esas decisiones como "validación (umbrales)":

<!-- cita: src/bybit_quant_lab/reporting/html.py#L279-L282 -->
`src/bybit_quant_lab/reporting/html.py` · líneas 279–282

```python
    secs[-1].pre = (
        "Decisiones de combinación ajustadas en entrenamiento (pesos, redundancia) y "
        "validación (umbrales):\n"
        + json.dumps(to_jsonable(out.redundancy), indent=2, ensure_ascii=False)
```

Manda el código: el umbral se ajusta en entrenamiento. Corregir esos dos textos es un ejercicio
del Módulo XVI.

### Hallazgo: los miembros con peso 0 siguen influyendo

**[Hecho, verificado con el código]** En `weighted_train` (YAML, líneas 157–159) la política de
conflictos es la de por defecto, `veto`. El veto (líneas 137–139) usa `n_short`/`n_long`, que
cuentan los votos de **todos** los miembros, incluidos los que `fit_weights` dejó con peso 0.
Además, la mediana del stop (líneas 143–146) incluye a los miembros con peso 0 que coinciden en
dirección.

Medición con datos sintéticos (6000 velas, semilla 42, parámetros del YAML):

<!-- ejecutar -->
```python
import yaml

from bybit_quant_lab.config.loader import load_config, load_strategy_params
from bybit_quant_lab.data.synthetic import generate_synthetic_ohlcv
from bybit_quant_lab.signals import CombinationConfig, combine_signals
from bybit_quant_lab.strategies import available_strategies
from bybit_quant_lab.validation.research import Researcher

datos = generate_synthetic_ohlcv(bars=6000, seed=42)
params = load_strategy_params("configs/strategies.yaml")
r = Researcher(datos, "BTCUSDT", "1h", load_config(), strategy_params=params)
combos = [
    CombinationConfig.model_validate(c)
    for c in yaml.safe_load(open("configs/strategies.yaml"))["combinations"]
]
singles = {n: r.strategy_candidate(n) for n in available_strategies()}
cands, info = r.build_combinations(singles, combos)

w = info["weights"]["weighted_train"]
print("pesos (entrenamiento):", {k: round(v, 3) for k, v in w.items() if v > 0})
print("con peso 0:", sorted(k for k, v in w.items() if v == 0))
print("umbral elegido en entrenamiento:", info["thresholds"]["weighted_train"])

cfg = CombinationConfig.model_validate(cands["weighted_train"].params)
frames = {n: c.signals for n, c in singles.items()}
cats = {n: "x" for n in frames}
todos = combine_signals(frames, cats, cfg)["signal"]
activos = [n for n, v in w.items() if v > 0]
solo = combine_signals(
    frames, cats, cfg.model_copy(update={"members": activos, "weights": {n: w[n] for n in activos}})
)["signal"]
print("política:", cfg.conflict_policy)
print("velas en posición, 10 miembros:", int((todos != 0).sum()))
print("velas en posición, solo miembros con peso > 0:", int((solo != 0).sum()))
```
<!-- salida -->
```text
pesos (entrenamiento): {'adx_di': 0.162, 'donchian_breakout': 0.316, 'macd_momentum': 0.284, 'obv_trend': 0.238}
con peso 0: ['bollinger_reversion', 'ema_crossover', 'rsi_reversion', 'stoch_rsi', 'volume_spike', 'vwap_deviation']
umbral elegido en entrenamiento: 0.5
política: veto
velas en posición, 10 miembros: 307
velas en posición, solo miembros con peso > 0: 2483
```

Interpretación: seis estrategias con peso 0 no suman nada a la puntuación, pero con `veto`
**bloquean** la mayor parte de las posiciones. "Peso 0" no significa "excluida". Es una
interacción entre dos decisiones de diseño razonables por separado, no un error de cálculo; se
recoge como pendiente en el Módulo XVII.

**Comprobación.** Con pesos a=3, b=1, c=0, d=0, θ=0,5 y política `veto`, ¿qué señal da la
vela 1 del ejemplo de referencia?

<details><summary>Ver respuesta</summary>

0. El `score` es 1,0 (≥ 0,5), pero `c` vota −1. Aunque su peso es 0, `n_short = 1 > 0` y el veto
anula la señal larga.
</details>

---

## 9.7 Consenso por categorías

**Intuición.** En lugar de contar estrategias, se cuentan **familias**: dos estrategias de
volumen que coinciden valen como una categoría, no como dos votos.

<!-- cita: src/bybit_quant_lab/signals/combiners.py#L127-L134 -->
`src/bybit_quant_lab/signals/combiners.py` · líneas 127–134

```python
    else:
        cats = pd.Series({m: categories.get(m, m) for m in members})
        cat_net = sig.T.groupby(cats).sum().T
        c_long, c_short = (cat_net > 0).sum(axis=1), (cat_net < 0).sum(axis=1)
        long_ok = c_long >= config.min_categories
        short_ok = c_short >= config.min_categories
        out = np.where(long_ok & ~short_ok, 1, np.where(short_ok & ~long_ok, -1, 0))
        strength = pd.Series(np.maximum(c_long, c_short) / max(cats.nunique(), 1), index=index)
```

- **128:** asigna a cada miembro su categoría (`volume`, `trend` o `indicator`).
- **129:** `sig.T.groupby(cats).sum().T` suma los estados **dentro de cada categoría**. Se
  transpone porque `groupby` agrupa filas; tras transponer, las estrategias son filas. El
  resultado es una columna por categoría con su voto neto interno.
- **130–133:** una categoría vota largo si su neto es > 0; la combinación entra si al menos
  `min_categories` categorías coinciden.

**Cálculo con `min_categories = 2`:**

| Vela | volume (a) | trend (b) | indicator (c+d) | categorías L / C | antes de veto | final (`veto`) |
|---|---|---|---|---|---|---|
| 0 | +1 | +1 | +1 | 3 / 0 | +1 | +1 |
| 1 | +1 | +1 | −1 | 2 / 1 | +1 | 0 (`c` corto) |
| 2 | +1 | 0 | +1 | 2 / 0 | +1 | +1 |
| 3 | 0 | 0 | +1 | 1 / 0 | 0 | 0 |
| 4 | −1 | −1 | −1 | 0 / 3 | −1 | −1 |
| 5 | +1 | −1 | 0 | 1 / 1 | 0 | 0 |

Resultado [+1, 0, +1, 0, −1, 0]. Comprobación de los cálculos a mano de 9.4–9.7 con el código:

<!-- ejecutar -->
```python
import pandas as pd

from bybit_quant_lab.signals import CombinationConfig, combine_signals
from bybit_quant_lab.strategies.base import empty_signal_frame

idx = pd.date_range("2024-01-01", periods=6, freq="1h", tz="UTC")


def marco(valores, stop):
    f = empty_signal_frame(idx)
    f["signal"] = valores
    f["conviction"] = [1.0 if v else 0.0 for v in valores]
    f["stop_distance"] = stop
    return f


frames = {
    "a": marco([1, 1, 1, 0, -1, 1], 1.0),
    "b": marco([1, 1, 0, 0, -1, -1], 3.0),
    "c": marco([1, -1, 0, 0, -1, 0], 5.0),
    "d": marco([0, 0, 1, 1, 0, 0], 7.0),
}
cats = {"a": "volume", "b": "trend", "c": "indicator", "d": "indicator"}
casos = {
    "simple m=2 veto": CombinationConfig(mode="simple_vote", min_margin=2),
    "simple m=1 net": CombinationConfig(mode="simple_vote", min_margin=1, conflict_policy="net"),
    "simple m=1 veto": CombinationConfig(mode="simple_vote", min_margin=1),
    "consenso k=3": CombinationConfig(mode="min_consensus", min_votes=3),
    "consenso k=2 veto": CombinationConfig(mode="min_consensus", min_votes=2),
    "ponderada net": CombinationConfig(
        mode="weighted_vote", weights={"a": 3, "b": 1, "c": 0, "d": 0},
        threshold=0.5, conflict_policy="net",
    ),
    "ponderada veto": CombinationConfig(
        mode="weighted_vote", weights={"a": 3, "b": 1, "c": 0, "d": 0}, threshold=0.5,
    ),
    "categorías 2": CombinationConfig(mode="category_consensus", min_categories=2),
}
for nombre, cfg in casos.items():
    out = combine_signals(frames, cats, cfg)
    print(f"{nombre:18s} {out['signal'].tolist()}")
```
<!-- salida -->
```text
simple m=2 veto    [1, 0, 1, 0, -1, 0]
simple m=1 net     [1, 1, 1, 1, -1, 0]
simple m=1 veto    [1, 0, 1, 1, -1, 0]
consenso k=3       [1, 0, 0, 0, -1, 0]
consenso k=2 veto  [1, 0, 1, 0, -1, 0]
ponderada net      [1, 1, 1, 0, -1, 1]
ponderada veto     [1, 0, 1, 0, -1, 0]
categorías 2       [1, 0, 1, 0, -1, 0]
```

**[Limitación] Categorías heterogéneas (M-05, pendiente).** La categoría `indicator` mezcla
estrategias de tendencia (`macd_momentum`, `adx_di`) y de reversión (`rsi_reversion`,
`bollinger_reversion`, `stoch_rsi`). En una vela, el neto de `indicator` puede ser 0 porque
una estrategia de tendencia y otra de reversión se cancelan, o +1 por pura información de
tendencia, que ya cuenta en la categoría `trend`. El consenso "entre dos categorías" puede ser,
en la práctica, la misma hipótesis contada dos veces. La clasificación en tres categorías viene
del encargo original y no se cambió (`docs/audit_report.md`, M-05).

---

## 9.8 Stops, take profit y convicción de una combinación

<!-- cita: src/bybit_quant_lab/signals/combiners.py#L143-L146 -->
`src/bybit_quant_lab/signals/combiners.py` · líneas 143–146

```python
    for col in SIGNAL_COLUMNS[2:]:
        values = _stack(use, col, index)
        agree = sig.eq(out_s, axis=0) & (out_s != 0).to_numpy()[:, None]
        result[col] = values.where(agree).median(axis=1, skipna=True)
```

- `agree` es una matriz booleana: verdadero donde el miembro vota **igual** que la combinación y
  la combinación no está en 0. `sig.eq(out_s, axis=0)` compara cada columna con la serie
  `out_s` fila a fila.
- `values.where(agree)` deja `NaN` donde el miembro no coincide; `median(skipna=True)` calcula la
  mediana de los que coinciden.

**Ejemplo** (test `test_stop_is_median_of_agreeing_members`): en la vela 0 coinciden `a`, `b`
y `c` con stops 1, 3 y 5 → mediana 3. En la vela 2 coinciden `a` y `d` (stops 1 y 7) → con dos
valores la mediana es su media, 4.

**Por qué la mediana.** Es robusta: un miembro con un stop desproporcionado no lo arrastra.

**[Hecho] Matiz del take profit y el trailing.** Con `skipna=True`, si solo uno de los miembros
coincidentes define take profit, la combinación usa **ese** take profit. Una regla de salida de
una sola estrategia puede gobernar toda la posición combinada.

**[Hecho] La convicción de la combinación es informativa.** `strength` se guarda en la
columna `conviction` y el motor la copia a cada operación (`backtesting/engine.py`, líneas 98
y 200), pero **ningún módulo de riesgo la usa** para dimensionar: una búsqueda de
`conviction` en `src/bybit_quant_lab/risk/` no devuelve resultados. El tamaño depende del stop
y del riesgo por operación (Módulo XI). `use_conviction` solo cambia la **puntuación** de
`weighted_vote`, no el tamaño.

---

## 9.9 Regímenes de mercado: qué son y cómo se calculan

**Intuición.** Un **régimen** es una etiqueta que describe el estado del mercado en una vela:
"hay tendencia o no", "la volatilidad es alta o baja", "hay poco volumen". Sirve para dos
cosas: desglosar resultados (¿la estrategia gana solo en tendencia?) y filtrar estrategias (no
usar reversión a la media en plena tendencia).

<!-- cita: src/bybit_quant_lab/signals/regime.py#L1-L13 -->
`src/bybit_quant_lab/signals/regime.py` · líneas 1–13

```python
"""Clasificación causal del régimen de mercado.

Tres dimensiones independientes, calculadas solo con datos hasta cada vela:

* ``trend``: ``trend`` si ``ADX >= adx_trend``, si no ``range``.
* ``volatility``: ``high_vol`` si el percentil del ATR % respecto a las ``vol_window`` velas
  anteriores es ``>= high_vol_pct``; ``low_vol`` si es ``<= low_vol_pct``; si no ``normal_vol``.
* ``liquidity``: ``low_liq`` si el volumen relativo a la mediana de las ``liq_window`` velas
  anteriores es ``< low_liq_ratio``; si no ``normal_liq``. Es una aproximación por volumen: sin
  datos de libro de órdenes no se mide la liquidez real.

Durante el calentamiento las dimensiones valen ``unknown``.
"""
```

<!-- cita: src/bybit_quant_lab/signals/regime.py#L41-L60 -->
`src/bybit_quant_lab/signals/regime.py` · líneas 41–60

```python
def classify_regime(data: pd.DataFrame, config: RegimeConfig | None = None) -> pd.DataFrame:
    """Devuelve columnas ``trend``, ``volatility``, ``liquidity`` y ``label`` (combinada)."""
    cfg = config or RegimeConfig()
    a = adx(data, cfg.adx_period)["adx"]
    trend = np.where(a.isna(), "unknown", np.where(a >= cfg.adx_trend, "trend", "range"))
    atr_pct = atr(data, cfg.atr_period) / data["close"]
    pct = rolling_percentile(atr_pct, cfg.vol_window)
    vol = np.select(
        [pct.isna(), pct >= cfg.high_vol_pct, pct <= cfg.low_vol_pct],
        ["unknown", "high_vol", "low_vol"],
        default="normal_vol",
    )
    med = data["volume"].rolling(cfg.liq_window, min_periods=cfg.liq_window).median().shift(1)
    rel = data["volume"] / med.replace(0, np.nan)
    liq = np.select(
        [rel.isna(), rel < cfg.low_liq_ratio], ["unknown", "low_liq"], default="normal_liq"
    )
    out = pd.DataFrame({"trend": trend, "volatility": vol, "liquidity": liq}, index=data.index)
    out["label"] = out["trend"] + "|" + out["volatility"]
    return out
```

Tres dimensiones independientes:

| Dimensión | Valores | Regla (valores por defecto) |
|---|---|---|
| `trend` | `trend` / `range` / `unknown` | ADX(14) ≥ 25 → `trend` |
| `volatility` | `high_vol` / `normal_vol` / `low_vol` / `unknown` | percentil del ATR % frente a las 500 velas **anteriores**: ≥ 0,8 alta, ≤ 0,2 baja |
| `liquidity` | `low_liq` / `normal_liq` / `unknown` | volumen / mediana de las 200 velas anteriores < 0,5 → `low_liq` |

- **45:** `np.where` anidado, igual que en las combinaciones. Mientras el ADX es `NaN`, la
  etiqueta es `unknown`.
- **46–47:** el ATR % (ATR / cierre) hace comparable la volatilidad a distintos precios. El
  percentil móvil (`rolling_percentile`, Módulo VII) compara el valor actual con las `n` velas
  anteriores: 0,9 significa "mayor que el 90 % de las últimas 500".
- **48–52:** `np.select(condiciones, valores, default)` evalúa las condiciones **en orden** y
  toma la primera verdadera. Por eso `unknown` va primero.
- **53:** la mediana del volumen lleva `shift(1)`: la vela actual no entra en su propia
  referencia (causalidad, Módulo VII).
- **59:** `label` combina tendencia y volatilidad (`trend|high_vol`). Es la etiqueta que el
  motor guarda en cada operación para los desgloses por régimen (`Researcher.simulate`,
  `research.py`, línea 160).

**[Limitación]** `liquidity` es una **aproximación por volumen**: sin libro de órdenes no se
mide la liquidez real (diferencial, profundidad). Lo dice la cabecera (líneas 8–10).

**Causalidad.** `test_regime_is_causal` compara el régimen calculado con toda la serie y con
solo las primeras 1200 velas: deben coincidir en esas 1200.

<!-- cita: tests/unit/test_signals.py#L134-L139 -->
`tests/unit/test_signals.py` · líneas 134–139

```python
def test_regime_is_causal(synth: pd.DataFrame) -> None:
    full = classify_regime(synth)
    part = classify_regime(synth.iloc[:1200])
    pd.testing.assert_frame_equal(full.iloc[:1200], part)
    assert set(full["trend"].unique()) <= {"trend", "range", "unknown"}
    assert np.all(full["liquidity"].isin(["low_liq", "normal_liq", "unknown"]))
```

Distribución en la serie sintética:

<!-- ejecutar -->
```python
from bybit_quant_lab.data.synthetic import generate_synthetic_ohlcv
from bybit_quant_lab.signals import classify_regime

reg = classify_regime(generate_synthetic_ohlcv(bars=6000, seed=42))
for dim in ("trend", "volatility", "liquidity"):
    print(dim, reg[dim].value_counts().to_dict())
t = reg["trend"]
validas = t.isin(["trend", "range"]) & t.shift(1).isin(["trend", "range"])
print("cambios trend<->range:", int(((t != t.shift(1)) & validas).sum()))
```
<!-- salida -->
```text
trend {'range': 3287, 'trend': 2686, 'unknown': 27}
volatility {'high_vol': 2131, 'normal_vol': 1727, 'low_vol': 1629, 'unknown': 513}
liquidity {'normal_liq': 5701, 'unknown': 200, 'low_liq': 99}
cambios trend<->range: 185
```

Lectura:

- **`unknown` en `trend` (27 velas):** el calentamiento del ADX(14), igual que en la sección
  8.10.
- **`unknown` en `volatility`:** el ATR necesita 14 velas y el percentil 501 valores más.
- **`high_vol` > 20 %:** el percentil es **relativo a las 500 velas anteriores**. Si la
  volatilidad crece de forma sostenida, muchas velas quedan por encima del percentil 80 de su
  pasado reciente. No es una proporción fija.
- **185 cambios entre `trend` y `range`:** el régimen de tendencia **no tiene histéresis**
  (a diferencia de `adx_di`, que entra con 25 y sale con 20). Un ADX que oscila alrededor de 25
  cambia la etiqueta muchas veces. Consecuencia en la sección siguiente.

---

## 9.10 Filtro de régimen

<!-- cita: src/bybit_quant_lab/signals/combiners.py#L62-L79 -->
`src/bybit_quant_lab/signals/combiners.py` · líneas 62–79

```python
def apply_regime_filter(
    signals: pd.DataFrame,
    categories: dict[str, str],
    regime: pd.DataFrame,
    rules: dict[str, dict[str, list[str]]],
) -> pd.DataFrame:
    """Fuerza a 0 las señales de cada estrategia fuera de sus regímenes permitidos."""
    out = signals.copy()
    reg = regime.reindex(signals.index)
    for name in out.columns:
        allowed = pd.Series(True, index=out.index)
        for key in ("*", categories.get(name, ""), name):
            for dim, values in (rules.get(key) or {}).items():
                if dim not in reg.columns:
                    raise ValueError(f"Dimensión de régimen desconocida: {dim}")
                allowed &= reg[dim].isin(values)
        out.loc[~allowed, name] = 0
    return out
```

- **73:** para cada estrategia se consultan tres claves de reglas, en este orden: el comodín
  `*`, el nombre de su categoría y su propio nombre.
- **74–77:** cada regla exige que el régimen esté en la lista de valores permitidos. Las
  condiciones se combinan con `&=`, es decir, **todas** deben cumplirse. Una regla específica
  de una estrategia **no puede relajar** una regla de `*`; solo puede añadir restricciones.
- **75–76:** una dimensión inexistente es un error, no se ignora en silencio.
- **78:** donde no está permitido, el estado de la estrategia se fuerza a 0 **antes de votar**.

La combinación configurada que usa reglas:

<!-- cita: configs/strategies.yaml#L169-L178 -->
`configs/strategies.yaml` · líneas 169–178

```yaml
  - name: regime_switch
    mode: min_consensus
    min_votes: 2
    regime_rules:
      trend: {trend: [trend]}                         # categoría tendencia solo en tendencia
      rsi_reversion: {trend: [range]}                 # reversión solo en lateral
      bollinger_reversion: {trend: [range]}
      vwap_deviation: {trend: [range]}
      stoch_rsi: {trend: [range]}
      "*": {liquidity: [normal_liq, unknown]}         # bloquear baja liquidez
```

**Cuidado con la lectura de la línea 173.** `trend: {trend: [trend]}` contiene tres "trend"
distintos: la **categoría** `trend` (clave exterior), la **dimensión** `trend` y el **valor**
`trend`. Significa: "a las estrategias de la categoría tendencia, permíteles operar solo cuando
la dimensión de tendencia vale `trend`".

**[Hecho] Efecto lateral: entradas a mitad de una posición.** El filtro actúa sobre el
**estado**, no sobre los eventos. Si una estrategia está larga desde hace 30 velas, el régimen
pasa a `range` (estado forzado a 0) y vuelve a `trend`, la señal filtrada pasa de 0 a +1: para
el motor es una **entrada nueva**, aunque la estrategia no haya generado ninguna. Medición con
una sola estrategia y la regla de tendencia:

<!-- ejecutar -->
```python
from bybit_quant_lab.data.synthetic import generate_synthetic_ohlcv
from bybit_quant_lab.signals import CombinationConfig, classify_regime, combine_signals
from bybit_quant_lab.strategies import create_strategy

datos = generate_synthetic_ohlcv(bars=6000, seed=42)
reg = classify_regime(datos)
frames = {"ema_crossover": create_strategy("ema_crossover").generate_signals(datos)}
cfg = CombinationConfig(
    mode="min_consensus",
    min_votes=1,
    conflict_policy="net",
    regime_rules={"ema_crossover": {"trend": ["trend"]}},
)
orig = frames["ema_crossover"]["signal"]
filt = combine_signals(frames, {"ema_crossover": "trend"}, cfg, reg)["signal"]


def entradas(s):
    return (s != 0) & (s != s.shift(1, fill_value=0))


sin_evento = entradas(filt) & (orig == orig.shift(1, fill_value=0))
forzadas = (filt == 0) & (filt.shift(1, fill_value=0) != 0) & (orig != 0)
print("entradas de la estrategia:", int(entradas(orig).sum()))
print("entradas tras el filtro:", int(entradas(filt).sum()))
print("  de ellas, sin cambio en la estrategia:", int(sin_evento.sum()))
print("salidas forzadas por el régimen:", int(forzadas.sum()))
print("velas en posición:", int((orig != 0).sum()), "->", int((filt != 0).sum()))
```
<!-- salida -->
```text
entradas de la estrategia: 23
entradas tras el filtro: 17
  de ellas, sin cambio en la estrategia: 9
salidas forzadas por el régimen: 11
velas en posición: 642 -> 343
```

Interpretación:

- El filtro **reduce** la exposición (de 642 a 343 velas), pero **no** reduce las operaciones en
  la misma proporción: de las entradas filtradas, más de la mitad son **reentradas** creadas
  por el regreso del régimen, a un precio peor que el de la entrada original, y cada una paga
  comisión y deslizamiento (Módulo X).
- Las salidas forzadas no son decisiones de la estrategia: las provoca el cambio de etiqueta,
  que sin histéresis oscila (sección 9.9).

**[Diseño]** Es coherente con el contrato del motor: entra en cada **transición** del estado
objetivo, venga de donde venga. Una alternativa sería filtrar solo los **eventos de entrada**
(bloquear entradas en régimen no permitido, pero no expulsar posiciones abiertas). No está
implementada.

**[Hecho] El régimen no bloquea operaciones de estrategias individuales.** En los backtests de
una sola estrategia, el régimen solo se usa como **etiqueta** de las operaciones. Filtra únicamente
dentro de una combinación con `regime_rules`.

**Comprobación.** Con la regla `"*": {liquidity: [normal_liq]}` (sin `unknown`), ¿qué ocurre en
las primeras 200 velas?

<details><summary>Ver respuesta</summary>

Ninguna estrategia puede operar: la mediana del volumen necesita 200 velas anteriores, así que
`liquidity` vale `unknown` y no está en la lista permitida. Por eso la configuración del
repositorio incluye `unknown` en esa regla.
</details>

---

## 9.11 Detección de redundancia

<!-- cita: src/bybit_quant_lab/signals/redundancy.py#L1-L46 -->
`src/bybit_quant_lab/signals/redundancy.py` · líneas 1–46

```python
"""Redundancia entre señales: correlación, coincidencia y selección de estrategias no redundantes.

Estas medidas deben calcularse **en el período de entrenamiento** cuando se usan para decidir
qué estrategias entran en una combinación.
"""

from __future__ import annotations

import pandas as pd


def signal_correlation(signals: pd.DataFrame) -> pd.DataFrame:
    """Correlación de Pearson entre series de estado (-1/0/1). Columnas constantes -> NaN."""
    return signals.astype(float).corr()


def signal_agreement(signals: pd.DataFrame) -> pd.DataFrame:
    """Proporción de velas con la misma dirección entre las velas en que ambas están activas."""
    names = list(signals.columns)
    out = pd.DataFrame(index=names, columns=names, dtype=float)
    for a in names:
        for b in names:
            both = (signals[a] != 0) & (signals[b] != 0)
            out.loc[a, b] = (
                float((signals[a][both] == signals[b][both]).mean()) if both.any() else float("nan")
            )
    return out


def select_non_redundant(
    corr: pd.DataFrame, threshold: float = 0.7, priority: list[str] | None = None
) -> tuple[list[str], dict[str, str]]:
    """Selección voraz: recorre ``priority`` y descarta las que superan ``|corr| > threshold``
    con alguna ya seleccionada. Devuelve (seleccionadas, {descartada: correlacionada_con})."""
    order = priority or list(corr.columns)
    values = corr.astype(float).fillna(0.0).to_numpy()
    pos = {str(c): i for i, c in enumerate(corr.columns)}
    kept: list[str] = []
    dropped: dict[str, str] = {}
    for name in order:
        clash = next((k for k in kept if abs(float(values[pos[name], pos[k]])) > threshold), None)
        if clash is None:
            kept.append(name)
        else:
            dropped[name] = clash
    return kept, dropped
```

Dos medidas:

- **Correlación de Pearson** (`signal_correlation`) entre series de estados −1/0/1 (Módulo VI).
- **Coincidencia direccional** (`signal_agreement`): entre las velas en que **ambas** están
  activas, la fracción en que tienen la misma dirección.

Y un procedimiento de selección voraz (`select_non_redundant`, líneas 30–46): recorre las
estrategias en orden; conserva una si su |correlación| con todas las ya conservadas es ≤ el
umbral; si no, la descarta y anota con cuál chocó. "Voraz" significa que decide una a una sin
reconsiderar: el resultado depende del **orden** (por defecto, el de las columnas, que es
alfabético en `build_combinations`).

### Por qué la correlación subestima la redundancia: cálculo a mano

Dos estrategias que **siempre** coinciden cuando ambas están activas, pero que entran y salen en
momentos distintos:

```text
vela:  0   1   2   3   4   5   6   7
x   :  1   1   0   0   0   0  -1  -1
y   :  0   1   1   0   0   0   0  -1
```

- Ambas activas en las velas 1 (+1, +1) y 7 (−1, −1) → coincidencia = 2/2 = **1,0**.
- Pearson (n = 8): media de x = 0; media de y = 1/8.
  - Σ x·y = 1·1 + (−1)·(−1) = 2; como la media de x es 0, cov = 2/7.
  - var(x) = Σx²/7 = 4/7; var(y) = (Σy² − 8·(1/8)²)/7 = (3 − 0,125)/7 = 2,875/7.
  - ρ = (2/7) / √(4/7 · 2,875/7) = 2 / √11,5 ≈ **0,590**.

Con el umbral 0,7, estas dos estrategias se considerarían **no redundantes**, aunque nunca se
contradicen. Los muchos ceros (velas fuera de posición) y los desfases de entrada diluyen la
correlación.

<!-- ejecutar -->
```python
import pandas as pd

from bybit_quant_lab.signals import signal_agreement, signal_correlation

s = pd.DataFrame({"x": [1, 1, 0, 0, 0, 0, -1, -1], "y": [0, 1, 1, 0, 0, 0, 0, -1]})
print("correlación:", round(float(signal_correlation(s).loc["x", "y"]), 3))
print("coincidencia:", float(signal_agreement(s).loc["x", "y"]))
```
<!-- salida -->
```text
correlación: 0.59
coincidencia: 1.0
```

**[Limitación] La coincidencia tampoco basta sola.** Dos estrategias activas a la vez en una
sola vela, y de acuerdo, dan coincidencia 1,0 con una muestra de tamaño 1. Conviene mirar
ambas medidas **y** cuántas velas comparten.

---

## 9.12 Cuando el filtro de redundancia no elimina ninguna estrategia

Resultado real en el entrenamiento sintético (las 3600 primeras velas de 6000, semilla 42):

<!-- ejecutar -->
```python
import numpy as np
import pandas as pd

from bybit_quant_lab.config.loader import load_config, load_strategy_params
from bybit_quant_lab.data.synthetic import generate_synthetic_ohlcv
from bybit_quant_lab.signals import select_non_redundant, signal_agreement, signal_correlation
from bybit_quant_lab.strategies import available_strategies
from bybit_quant_lab.validation.research import Researcher

datos = generate_synthetic_ohlcv(bars=6000, seed=42)
params = load_strategy_params("configs/strategies.yaml")
r = Researcher(datos, "BTCUSDT", "1h", load_config(), strategy_params=params)
tr = r.segments["train"]
sig = pd.DataFrame(
    {n: r.strategy_candidate(n).signals["signal"] for n in available_strategies()}
).iloc[tr.start_pos : tr.end_pos + 1]
corr = signal_correlation(sig)
fuera_diag = corr.where(~np.eye(len(corr), dtype=bool)).abs().stack()
print("velas de entrenamiento:", len(sig))
print("par más correlacionado:", fuera_diag.idxmax(), round(float(fuera_diag.max()), 3))
kept, dropped = select_non_redundant(corr.fillna(0), 0.7)
print("conservadas:", len(kept), "descartadas:", dropped)
tend = ["ema_crossover", "donchian_breakout", "adx_di"]
print(signal_agreement(sig).loc[tend, tend].round(2).to_string())
```
<!-- salida -->
```text
velas de entrenamiento: 3600
par más correlacionado: ('adx_di', 'donchian_breakout') 0.652
conservadas: 10 descartadas: {}
                   ema_crossover  donchian_breakout  adx_di
ema_crossover               1.00               0.96    0.91
donchian_breakout           0.96               1.00    0.97
adx_di                      0.91               0.97    1.00
```

**Cómo interpretarlo.**

1. **Hecho:** con el umbral 0,7 no se descarta ninguna estrategia. `dedup_vote` usa las diez y
   es, en la práctica, `simple_vote` con margen 2 y `veto` sobre todas las estrategias.
2. **No significa** que las estrategias sean independientes. La coincidencia entre las de
   tendencia supera 0,9: cuando están activas a la vez, casi siempre dicen lo mismo.
3. **Por qué ocurre:** la medida (Pearson sobre estados con muchos ceros) es débil para este
   tipo de señal (sección 9.11). El umbral 0,7 es una convención, no un valor calibrado.
4. **Qué mirar en el informe:** la sección "Redundancia entre señales (entrenamiento)" del HTML
   muestra ambas matrices y el JSON con `"dropped": {}`. Un diccionario vacío es un resultado,
   no un error, y hay que leerlo como "la medida no detectó redundancia", no como "no la hay".
5. **Qué no hacer:** bajar el umbral mirando los resultados de validación hasta que la
   combinación "mejore". Sería ajustar con el segmento de selección (Módulo XIII). Si se cambia
   la medida o el umbral, debe hacerse con entrenamiento y quedar registrado.
6. **Opciones documentadas** (`docs/audit_report.md`, M-05): usar `signal_agreement` o fijar
   `members` explícitos en el YAML. Ejercicio en el Módulo XVI.

---

## 9.13 Las seis combinaciones configuradas

Con los mismos datos y parámetros que en 9.6, número de entradas y de velas en posición de cada
combinación sobre la serie completa:

<!-- ejecutar -->
```python
import yaml

from bybit_quant_lab.config.loader import load_config, load_strategy_params
from bybit_quant_lab.data.synthetic import generate_synthetic_ohlcv
from bybit_quant_lab.signals import CombinationConfig
from bybit_quant_lab.strategies import available_strategies
from bybit_quant_lab.validation.research import Researcher

datos = generate_synthetic_ohlcv(bars=6000, seed=42)
params = load_strategy_params("configs/strategies.yaml")
r = Researcher(datos, "BTCUSDT", "1h", load_config(), strategy_params=params)
combos = [
    CombinationConfig.model_validate(c)
    for c in yaml.safe_load(open("configs/strategies.yaml"))["combinations"]
]
singles = {n: r.strategy_candidate(n) for n in available_strategies()}
cands, _ = r.build_combinations(singles, combos)
print(f"{'combinación':16s} {'modo':20s} {'entradas':>8s} {'velas':>6s}")
for nombre, c in cands.items():
    s = c.signals["signal"]
    entradas = int(((s != 0) & (s != s.shift(1, fill_value=0))).sum())
    print(f"{nombre:16s} {c.params['mode']:20s} {entradas:8d} {int((s != 0).sum()):6d}")
```
<!-- salida -->
```text
combinación      modo                 entradas  velas
vote_all         simple_vote               210    876
weighted_train   weighted_vote             106    307
consensus_3      min_consensus             108    318
category_2       category_consensus        168    608
dedup_vote       simple_vote               190    737
regime_switch    min_consensus             371   2988
```

Observaciones:

- `regime_switch` es la combinación con **más** exposición y más entradas, pese a tener filtros.
  El bloque siguiente aísla la causa.
- `weighted_train` y `consensus_3` tienen exposición parecida por motivos distintos: la primera,
  por el veto de los miembros con peso 0 (9.6).
**¿Un filtro que aumenta la exposición?** Se compara `regime_switch` con y sin sus reglas de
régimen, y se cuenta cuántos vetos vienen de estrategias de reversión:

<!-- ejecutar -->
```python
import yaml

from bybit_quant_lab.config.loader import load_config, load_strategy_params
from bybit_quant_lab.data.synthetic import generate_synthetic_ohlcv
from bybit_quant_lab.signals import CombinationConfig, combine_signals
from bybit_quant_lab.strategies import available_strategies, create_strategy
from bybit_quant_lab.validation.research import Researcher

datos = generate_synthetic_ohlcv(bars=6000, seed=42)
params = load_strategy_params("configs/strategies.yaml")
r = Researcher(datos, "BTCUSDT", "1h", load_config(), strategy_params=params)
frames = {n: r.strategy_candidate(n).signals for n in available_strategies()}
cats = {n: create_strategy(n).category.value for n in frames}
raw = yaml.safe_load(open("configs/strategies.yaml"))["combinations"]
cfg = CombinationConfig.model_validate(next(c for c in raw if c["name"] == "regime_switch"))


def resumen(s):
    entradas = int(((s != 0) & (s != s.shift(1, fill_value=0))).sum())
    return entradas, int((s != 0).sum())


sin = combine_signals(frames, cats, cfg.model_copy(update={"regime_rules": None}))["signal"]
con = combine_signals(frames, cats, cfg, r.regime)["signal"]
print("sin reglas de régimen (entradas, velas):", resumen(sin))
print("con reglas de régimen (entradas, velas):", resumen(con))

import pandas as pd

S = pd.DataFrame({n: f["signal"] for n, f in frames.items()})
n_long, n_short = (S > 0).sum(axis=1), (S < 0).sum(axis=1)
direccion = (n_long >= 2).astype(int) - (n_short >= 2).astype(int)
# direccion = +1/-1 si una sola dirección alcanza 2 votos; vetada si hay voto contrario
vetadas = ((direccion > 0) & (n_short > 0)) | ((direccion < 0) & (n_long > 0))
reversion = ["rsi_reversion", "bollinger_reversion", "stoch_rsi", "vwap_deviation"]
por_reversion = vetadas & (S[reversion].mul(direccion, axis=0) < 0).any(axis=1)
print("velas vetadas sin filtro:", int(vetadas.sum()))
print("  con algún voto contrario de reversión:", int(por_reversion.sum()))
```
<!-- salida -->
```text
sin reglas de régimen (entradas, velas): (190, 737)
con reglas de régimen (entradas, velas): (371, 2988)
velas vetadas sin filtro: 2354
  con algún voto contrario de reversión: 1813
```

Explicación: `regime_switch` usa `veto`. Sin filtro, en una tendencia las estrategias de
reversión suelen votar en contra de las de tendencia y **vetan** sus entradas. El filtro apaga
las de reversión en régimen `trend` (y las de tendencia en `range`), así que desaparecen esos
vetos (en esta serie, 1813 de las 2354 velas vetadas tenían un voto contrario de reversión) y la combinación pasa mucho más tiempo en posición. A esto se suman las reentradas de
9.10. Observa también que "sin reglas" da lo mismo que `dedup_vote`: ambas son, por la
equivalencia de 9.4, "dos votos en una dirección y ninguno en contra" sobre las diez
estrategias.

- Cada combinación es una **prueba más** que entra en el recuento de ensayos del DSR
  (Módulo XIII). Seis combinaciones más diez estrategias son al menos dieciséis candidatos por
  mercado, más los ensayos de umbral registrados.

---

## 9.14 Resumen y errores comunes

| Idea | Dónde | Etiqueta |
|---|---|---|
| La combinación devuelve el mismo contrato que una estrategia | `combiners.py` 136–150 | [Diseño] |
| `simple_vote` + `veto` ≡ `min_consensus` + `veto` | test de auditoría B-01 | [Hecho] |
| Pesos y umbral se ajustan en entrenamiento | `research.py` 215–239 | [Hecho] tras `a50ac62` |
| Cabecera de `research.py` e informe HTML aún dicen "validación" | 7–8; `html.py` 279–282 | [Discrepancia] |
| Miembros con peso 0 vetan y aportan stop | `combiners.py` 137–146 | [Hecho], pendiente |
| La convicción no cambia el tamaño | búsqueda en `risk/` | [Hecho] |
| Régimen sin histéresis; el filtro crea reentradas | `regime.py` 45; `combiners.py` 78 | [Hecho] |
| Categoría `indicator` heterogénea | M-05 | [Limitación], pendiente |
| Pearson sobre estados subestima la redundancia | M-05 | [Limitación], pendiente |
| `liquidity` es una aproximación por volumen | `regime.py` 8–10 | [Limitación] |

**Errores comunes.**

1. Contar diez votos como diez opiniones independientes.
2. Creer que un peso 0 excluye a una estrategia cuando la política es `veto`.
3. Interpretar `"dropped": {}` como prueba de independencia.
4. Ajustar umbrales, pesos o miembros con validación y luego seleccionar con la misma
   validación.
5. Suponer que un filtro de régimen solo "quita" operaciones: también puede añadir reentradas.

### Comprobación final del módulo

En una vela, cinco estrategias votan +1, dos votan −1 y tres se abstienen. Calcula la señal de:
(a) `simple_vote`, margen 3, `net`; (b) `simple_vote`, margen 3, `veto`; (c) `min_consensus`,
3 votos, `net`; (d) `weighted_vote` con pesos iguales, θ = 0,3, `net`.

<details><summary>Ver respuesta</summary>

- (a) net = 5 − 2 = 3 ≥ 3 → **+1**.
- (b) +1 antes del veto, pero hay votos cortos → **0**.
- (c) n_long = 5 ≥ 3 y n_short = 2 < 3 → **+1**.
- (d) score = (5 − 2)/10 = 0,3 ≥ 0,3 → **+1** (las abstenciones cuentan en el denominador,
  porque se divide por la suma de **todos** los pesos).
</details>
