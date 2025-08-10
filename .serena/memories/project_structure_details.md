# Project Structure Details

- `README.md`
- `progress-report/`
- `src/`
  - `src/src/`
    - `features/`
      - `ast_analyzer.py`
      - `advanced_features.py`
      - `detection_models.py`
      - `test_parser_sample.py`
    - `dataset/` (C/C++ human/ai samples, metadata)
    - `.env.example`, `.gitignore`, `requirements.txt`
  - `frontend/`
    - `app/`
      - `analysis/` (+ `_components/` with `code-editor.tsx`, `header.tsx`)
      - `home/`
      - `layout.tsx`
    - `components/ui/` (button, card, select, etc.)
    - `lib/utils.ts`, `styles/globals.css`
    - Config: `package.json`, `tsconfig.json`, `eslint.config.mjs`, `next.config.ts`, Prettier config
  - `backend/`
    - `app/main.py` (FastAPI app, endpoints)
    - `app/enhanced_ml_integration.py` (feature extraction + heuristic detector orchestration)
    - `requirements.txt`, `Makefile`, `.gitignore`
- `thesis/` (images, docx, pdf, md)

Key files to know:
- Backend entry: `src/backend/app/main.py`
- Frontend app entry: `src/frontend/app/layout.tsx`, pages under `app/analysis` and `app/home`
- Heuristic detector: `src/src/features/detection_models.py`
- Advanced feature extractor: `src/src/features/advanced_features.py`
