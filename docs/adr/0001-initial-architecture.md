# ADR-0001: Initial Architecture and Persona Pattern for N.O.R.A.

**Category:** Architecture
**Author:** N.O.R.A. Dev Team / Claude
**Date:** 2026-10-02
**Status:** Accepted

## 📝 Context
N.O.R.A. is an experimental autonomous AI agent designed to simulate human reasoning within a strictly controlled knowledge environment. The project requires a scalable foundation that can support:
1. Isolated context and state ("feelings").
2. Future integrations with various interfaces (CLI, API, Voice).
3. Long-term and short-term memory management (Vector databases, SQLite).

Starting with a monolithic script would hinder these goals as the project grows in complexity.

## 💡 Decision
We have adopted a modular Python architecture located within the `src/nora/` directory. The application is divided into distinct layers:
- **Core (`src/nora/core/`)**: Houses the `NoraPersona` class, which acts as the source of truth for N.O.R.A.'s identity, current emotional state (`current_mood`), and dynamic system prompt generation.
- **Interfaces (`src/nora/interfaces/`)**: Contains entry points for user interaction. Currently implemented via `CLIInterface`.
- **Memory (`src/nora/memory/`)**: Reserved for future database and context management integrations.

### Trade-offs

| Solution | Pros | Cons | Decision |
|---|---|---|---|
| Single monolithic script (`app.py`) | Extremely fast to start and prototype. | Becomes unmanageable quickly when adding complex state, memory vectors, and multiple interfaces. | Rejected |
| Modular Architecture | Extensible. Easy to plug in new LLMs, memory stores, or interfaces (e.g., adding a voice interface won't break the CLI). | Slight initial boilerplate and overhead (requires virtual environments and module imports). | **Accepted** |

## ⚙️ Consequences
- **Positive:** We can develop the LLM engine (`engine.py`) and memory components independently without affecting the CLI interface.
- **Neutral:** Contributors must understand the module split and use the `.venv` correctly to run the application via `src/main.py`.
- **Negative:** None observed at this stage.

## 🔍 Verification Evidence
- Directory structure successfully initialized (`src/nora/core`, `interfaces`, `memory`, `utils`).
- The base interface runs correctly by executing `python src/main.py`, proving the module imports and `.env` loading work as expected.

## 📁 Related Files
- `src/main.py` — `main`
- `src/nora/core/persona.py` — `NoraPersona`, `get_system_prompt`, `update_mood`
- `src/nora/interfaces/cli.py` — `CLIInterface`, `start`, `_process_and_respond`
