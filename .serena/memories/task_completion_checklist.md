# Task Completion Checklist

Backend
- [ ] `make setup` succeeded; `uvicorn` runs on :8000
- [ ] `/health` returns status OK
- [ ] `/analyze-code` returns structured `EnhancedAnalysisResponse`
- [ ] `/analyze-code/file` accepts `.c/.cpp/.h/.hpp`
- [ ] CORS configured appropriately per environment

Frontend
- [ ] `npm install` completes without errors
- [ ] `npm run dev` serves on :3000
- [ ] Code editor submits to backend and displays results
- [ ] Lint passes: `npm run lint`, format passes: `npm run format:check`

Features/Quality
- [ ] Feature extractor paths covered by tests
- [ ] Heuristic thresholds validated with sample data
- [ ] Feedback persistence implemented and verified
- [ ] Basic security (rate limiting/auth) considered if exposed publicly
