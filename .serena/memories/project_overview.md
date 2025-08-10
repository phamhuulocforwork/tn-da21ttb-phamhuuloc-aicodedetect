# Project Overview

AI Code Detection (C/C++) with heuristic/static analysis. The project comprises:

- Backend (`FastAPI`): REST API to analyze code and detect AI-generated vs human-written using enhanced static features (no ML runtime). Key module: `src/backend/app/main.py`, enhanced analyzer in `src/backend/app/enhanced_ml_integration.py` leveraging feature extractors in `src/src/features`.
- Frontend (`Next.js App Router`): UI for code input and analysis visualization at `src/frontend`. Editor based on `@monaco-editor/react`, UI via Radix and custom components.
- Feature extraction engine: `src/src/features` with `ast_analyzer.py`, `advanced_features.py`, and heuristic detector `detection_models.py`.
- Academic assets (`thesis/`) and sample datasets (`src/src/dataset/`).

Notable design notes:
- ML detectors removed; only heuristic/static detection remains. Advanced features (AST, redundancy, naming, complexity, AI patterns) computed and fed to a scoring detector.
- CORS is open for development (`allow_origins=["*"]`).
- Environment sample: `src/src/.env.example` (e.g., `GEMINI_API_KEY`, currently unused in backend).

Key API endpoints (FastAPI):
- GET `/` → Basic service info
- GET `/health` → Service health
- GET `/detectors` → Available detectors metadata
- POST `/analyze-code` → Analyze code text payload
- POST `/analyze-code/file` → Analyze uploaded file (.c/.cpp/.h/.hpp)
- POST `/analyze-code/batch` → Batch analyze up to 10 samples
- POST `/submit-feedback` → Collect feedback for future improvement

Run targets:
- Backend: `make setup`, `make dev`, `make start` in `src/backend`
- Frontend: `npm i && npm run dev` in `src/frontend`

Security/ops:
- CORS wide-open in dev; tighten for prod.
- No DB persistence implemented; feedback currently printed to stdout.
