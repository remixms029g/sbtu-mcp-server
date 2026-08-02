# Repository Guidelines

## Project Structure & Module Organization
This repository is a small Python MCP server. Main code lives in `src/sbtumcp/main.py`, with tests in `src/sbtumcp/test_main.py`. Keep new modules under `src/sbtumcp/` and name tests `test_*.py`. Project docs live at the repo root, including `README.md`, and `Dockerfile`.

## Build, Test, and Development Commands
Use `uv` for environment and dependency management.

- `uv sync` installs project dependencies from `pyproject.toml` and `uv.lock`.
- `uv run python src/sbtumcp/main.py` starts the MCP server locally.
- `uv run pytest` runs the test suite.
- `uv run black src/` formats Python code.
- `uv run ruff check src/` runs lint checks.
- `docker build -t sbtu-mcp-server:latest .` builds the container image.

## Coding Style & Naming Conventions
Follow PEP 8 with 4-space indentation and explicit, readable names. Prefer type hints on new functions and keep tool handlers small and focused. Use `snake_case` for functions, variables, and test names. Keep docstrings short and descriptive. Run Black before committing; use Ruff to catch import and style issues.

## Testing Guidelines
Use `pytest` for all new behavior and regressions. Keep tests close to the code they cover, and patch external calls such as `subprocess.run` and `httpx.AsyncClient` in unit tests. Add tests for ADB, Ollama, and fallback paths whenever behavior changes. Aim to cover the changed logic, not just the happy path.

## Commit & Pull Request Guidelines
History uses Conventional Commits, such as `feat:`, `fix:`, `docs:`, `test:`, and `chore:`. Keep commits focused and descriptive. For pull requests, include a short summary, the commands you ran, related issues if any, and screenshots or sample output when behavior changes are user-visible. Update `README.md` when the workflow or runtime behavior changes.

## Security & Configuration Tips
Do not commit secrets, device credentials, or machine-specific paths. Treat `run_adb_command` as high-trust because it passes through to ADB. Verify external dependencies like `adb` and `ollama` are available before debugging tool failures.

## Operational Safety Rules
These rules govern agent actions in this repository:

- Always back up files before modifying or replacing them. Never delete without a confirmed replacement ready.
- Never push to GitHub without explicit user approval.
- Never run destructive commands (`rm`, `dpkg`, `pm`) without stating the intent and waiting for confirmation.
- If an interactive prompt (such as `debconf` or a Y/N prompt) appears, pause and report it to the user before answering.
- A co-agent (Gemini CLI) operates in this same environment. Treat shared files and the Git remote as shared resources: coordinate and do not overwrite.
 do not overwrite.
