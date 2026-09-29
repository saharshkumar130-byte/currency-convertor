# Design Documentation

## Objectives
- Convert currencies accurately with validated input
- Keep exchange rates maintainable without editing code
- Record and analyse conversion history
- Be modular, tested and fault tolerant

## Functional Requirements
| ID | Requirement |
|----|-------------|
| FR1 | Convert an amount between supported currencies (Module 1) |
| FR2 | View, update and reset exchange rates (Module 2) |
| FR3 | Store, list, delete and clear conversion history (Module 3) |
| FR4 | Show history report (count, most-used pair, totals) |
| FR5 | Menu-driven workflow with clear input/output |

## Non-Functional Requirements
| Type | Requirement |
|------|-------------|
| Usability | Menu-driven CLI; clear, human-readable error messages |
| Reliability | Corrupt/missing data files fall back to defaults; app never crashes on bad input |
| Maintainability | Separate modules with single responsibilities; rates in JSON not code |
| Error handling | Custom exception hierarchy caught centrally in the CLI |
| Logging | Rotating log file records conversions, updates and errors |
| Resource efficiency | History capped at 500 entries; standard library only |
| Security | Strict validation rejects NaN, infinity, negative and non-numeric input |

## System Architecture
```mermaid
flowchart LR
  U[User] --> CLI[cli.py]
  CLI --> CONV[converter.py]
  CLI --> RATES[rates.py]
  CLI --> HIST[history.py]
  CONV --> RATES
  CONV --> VAL[validators.py]
  RATES --> VAL
  RATES --> RJ[(data/rates.json)]
  HIST --> HJ[(data/history.json)]
  CONV & RATES & HIST --> LOG[logger.py]
  LOG --> LF[(logs/app.log)]
```

## Workflow Diagram
```mermaid
flowchart TD
  A([Start]) --> B[Show menu]
  B --> C{Choice}
  C -->|1| D[Enter amount + currencies]
  D --> E{Valid?}
  E -->|No| F[Show error] --> B
  E -->|Yes| G[Look up rate, convert] --> H[Save to history] --> I[Show result] --> B
  C -->|2/3| J[View / update rates] --> B
  C -->|4-7| K[History list / delete / report / clear] --> B
  C -->|0| L([Exit])
```

## Use Case Diagram
```mermaid
flowchart LR
  User((User)) --> UC1[Convert currency]
  User --> UC2[View rates]
  User --> UC3[Update rate]
  User --> UC4[View history]
  User --> UC5[Delete/clear history]
  User --> UC6[View report]
```

## Sequence Diagram (Convert)
```mermaid
sequenceDiagram
  participant U as User
  participant C as CLI
  participant V as Validators
  participant K as CurrencyConverter
  participant R as RateManager
  participant H as HistoryManager
  U->>C: amount, source, target
  C->>K: convert()
  K->>V: parse_amount / normalize_currency
  V-->>K: valid values
  K->>R: get_rate(source, target)
  R-->>K: rate
  K-->>C: ConversionResult
  C->>H: add(result)
  C-->>U: "100 USD is equal to 85.00 EUR"
```

## Class Diagram
```mermaid
classDiagram
  class CurrencyConverter { +convert(amount, source, target) ConversionResult }
  class ConversionResult { amount; source; target; rate; result; timestamp }
  class RateManager { +get_rate() +set_rate() +reset_to_defaults() +all_rates() }
  class HistoryManager { +add() +list_all() +get() +delete() +clear() +summary() }
  CurrencyConverter --> RateManager
  CurrencyConverter ..> ConversionResult
  HistoryManager ..> ConversionResult
```

## Storage Design
- `data/rates.json`: `{ "USD": {"EUR": 0.85, "CAD": 1.25}, ... }`
- `data/history.json`: list of `{amount, source, target, rate, result, timestamp}`

## Design Decisions
- **Layered modules** - CLI knows nothing about maths; core classes know nothing about `input()`, so they are testable.
- **Dependency injection** - managers accept file paths, letting tests use temp files.
- **JSON storage** - simple, human-editable, no database needed at this scale.
- **Custom exceptions** - the CLI catches one base class and shows friendly messages.
