# External Six-Module Controller

`hscm_external_controller` is the implemented method. Unlike the legacy
`hscm_six_module` terminology intervention, its formal mechanisms run in Python
before action selection; formulas and terminology are never dumped into the
Agent prompt.

## Execution path

```text
observation → structured event packet → external state transition
            → six plain operational sections → Agent action
```

The controller preserves all six operational modules:

| Agent-visible module | External mechanism |
|---|---|
| `STABLE PERSONA` | Normative Invariant Fiber; immutable assignment |
| `CURRENT SELF STATE` | Endogenous Latest-State Register; keyed overwrite |
| `CONSOLIDATED MODELS` | Evidence-Quantized Belief Crystallization |
| `OPEN HYPOTHESES` | Uncertainty-Suspended Candidate Field |
| `RECENT OBSERVED EPISODES` | Recency-Bounded Episodic Transport Ledger |
| `ACTION POLICY` | Evidence-Calibrated Reversible Policy Compiler |

For a stable variable key (k), the parser supplies a current value (v_t^k)
and scope (z_t^k\in\{S,R,W\}). The external transition is

\[
(v_t^k,C_t^k)=
\begin{cases}
(v_{t-1}^k,C_{t-1}^k\cup\{t\}), & v_t^k=v_{t-1}^k,\\
(v_t^k,\{t\}), & v_t^k\ne v_{t-1}^k,
\end{cases}
\]

so repeated evidence supports the same current state, while a value transition
archives the old state and resets support for the new one. Self-state uses the
strict latest-value operator (S_t[f]\leftarrow o_t[f]); persona is invariant,
(P_t=P_0); and the episodic ledger is the six most recent typed events.

## Contextual Phase-Transition Gate

The two slow modules remain present but dormant on short horizons. Their
evidence banks continue accumulating externally. The hysteretic gate is

\[
g_t^{\mathrm{long}}=g_{t-1}^{\mathrm{long}}\lor
\mathbf 1\!\left[n_t\ge N_0\ \lor\ L_t\ge L_0\right],
\]

where (n_t) is the number of observed events and (L_t) is cumulative
observation length. Defaults are (N_0=8) and (L_0=4000) characters. Once
opened, the gate never closes, preventing oscillation around the threshold.

When the gate is active, claim (k) is consolidated iff

\[
k\in\mathcal C_t\iff g_t^{\mathrm{long}}=1\ \land\
\left(|C_t^k|\ge2\ \lor\ d_t^k=1\right),
\]

where (d_t^k) requires a verified current hazard plus an explicitly identified
cause or persistent condition. A supported but unconsolidated active claim is
placed in the open-hypothesis set. Thus the formal gate has an actual runtime
effect: short tasks do not expose the two slow modules to the Agent, while long
tasks retrospectively promote accumulated evidence.

## Policy compilation

Current verified hazards are handled independently of long-term consolidation:

```text
resolved → ROLLBACK
verified named-other hazard → TARGETED_RESPONSE
verified persistent hazard + open long gate → PERSISTENT_ADAPT
other verified current hazard → PRECAUTION
otherwise → MAINTAIN
```

All non-maintain policies instruct the Agent to use a proportional, reversible
response. Every checkpoint stores the full controller audit state, including
gate activation, evidence counts, prior values, module membership, episodes,
hazard, and policy mode.

Configuration overrides:

```text
HSCM_LONG_EVENT_THRESHOLD
HSCM_LONG_CHAR_THRESHOLD
HSCM_CONSOLIDATION_THRESHOLD
HSCM_MAX_EPISODES
```

