# Project Current Status

- Backend is operational with heuristic/static detector only; ML and hybrid detectors removed.
- Enhanced feature extraction path is active (AST, naming, redundancy, complexity, AI patterns). If import fails, API gracefully falls back to a simple heuristic in `main.py`.
- CORS is set to `*` for development; should be restricted for production.
- Feedback endpoint prints to stdout; no persistence layer yet.
- Frontend integrates a code editor and calls the backend (mocked submission logic exists in UI; wire to API as next step).
- Dataset folders are included for experiments; not used at runtime.

Risks/Limitations:
- No authentication, rate limiting, or storage for feedback.
- Heuristic scoring thresholds are static; tuning may be required with real data.
- `GEMINI_API_KEY` present in example env but not used in current backend code.

Next Steps (recommended):
- Wire frontend `handleSubmitCode` to backend `/analyze-code`.
- Add environment-based CORS config.
- Implement persistent feedback storage (file/DB) and basic auth if needed.
- Add unit tests for feature extractor and detector.
