# Model Routing (Pillar 4)

Use these capability tiers only when the runtime can route work across models or reasoning levels. The
tiers are vendor-neutral run metadata. Never invent a provider, model name, or routing event.

## Capability tiers

| Tier | Capability | Use for |
| --- | --- | --- |
| `fast` | Lowest-cost reliable execution | Deterministic scripts, field checks, format checks, and validators. |
| `standard` | General reasoning and creation | Ordinary implementation, board lanes, synthesis, and Standard creative work. |
| `deep` | Extended judgment | Conflicting evidence, first-of-kind product decisions, and Premium creative work. |
| `deep-coding` | Extended software reasoning | Multi-file refactors, new subsystems, migrations, and expensive architectural choices. |

The runtime decides which available model or reasoning setting satisfies a capability tier. A run may
record the actual model in a separate `model` field only when the runtime confirms it.

## Step map

| Step | Tier | Reason |
| --- | --- | --- |
| Brief, lock, output, conformance, and evidence validators | `fast` | The scripts evaluate explicit rules. |
| Options generation and keep / kill / change synthesis | `standard` | Ordinary creative judgment. |
| Review-board lanes and synthesis | `standard` | Evidence-grounded judgment. |
| Premium creative generation | `deep` | The craft decision is less mechanical and more expensive to get wrong. |
| New platform pattern or sharply conflicting board synthesis | `deep` | First-of-kind or unresolved judgment. |
| Small implementation or test change | `standard` | Bounded engineering work. |
| New subsystem, broad refactor, or migration | `deep-coding` | Architectural and implementation risk. |

If the current runtime does not expose model routing, use the active model and omit `modelTier` rather
than pretending a route occurred. The validators allow an omitted tier.

## Escalation

Escalate only after a concrete signal:

- the evidence or board lanes materially conflict;
- the brief remains contradictory after applying its explicit precedence rules;
- two attempts fail on the same implementation defect; or
- the work expands into a subsystem or migration.

High stakes alone do not prove a larger model is required. Approval, evidence, and validation remain
separate gates.

## Recording routing

When the runtime confirms routing, record the capability tier in `trace`:

```json
{ "step": "brief-gate", "modelTier": "fast", "durationMs": 12 },
{ "step": "options-generation", "modelTier": "standard", "durationMs": 830 },
{ "step": "output-audit", "modelTier": "fast", "durationMs": 41 }
```

Known validator steps must be tagged `fast` when a tier is recorded. Premium creative-production runs
must tag `options-generation` as `deep` when routing metadata is present. Custom work is human-led and
requires a named `tierSignoff` before `ship`.

These labels describe required capability, not a fixed vendor catalog. Provider-specific model strings
belong in deployment configuration, not this skill.
