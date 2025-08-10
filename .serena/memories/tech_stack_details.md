# Tech Stack Details

Backend (Python):
- Python 3.12 (per `src/backend/Makefile`)
- FastAPI 0.104.1, Uvicorn 0.24.0, Pydantic 2.7.1
- Static analysis deps: lizard 1.17.10 (optional metrics), numpy 1.26, pandas 2.0.3, tqdm 4.65.0
- Code modules: `app/main.py`, `app/enhanced_ml_integration.py`, feature engine under `src/src/features`

Frontend (TypeScript/React):
- Next.js 15.3.5 (App Router), React 19, TypeScript 5
- Styling: Tailwind CSS 4, CSS at `src/frontend/styles/globals.css`
- UI: Radix UI (`@radix-ui/react-select`), lucide-react icons
- Editor: `@monaco-editor/react`
- Tooling: ESLint 9 (`eslint-config-next`), Prettier 3 + tailwind plugin, sort imports plugin

Feature Engine (Python):
- `ast_analyzer.py`: regex/heuristic AST-like analysis for C/C++
- `advanced_features.py`: redundancy, naming, complexity, AI-pattern features
- `detection_models.py`: `HeuristicScoringDetector` only (ML/hybrid removed)

Config/Env:
- Backend requirements: `src/backend/requirements.txt`
- Shared minimal requirements: `src/src/requirements.txt`
- Example env: `src/src/.env.example` (contains `GEMINI_API_KEY`, not wired)
