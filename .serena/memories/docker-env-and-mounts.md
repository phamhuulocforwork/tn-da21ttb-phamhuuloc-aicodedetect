Deployment notes:
- Frontend Next.js requires NEXT_PUBLIC_API_URL and NEXT_PUBLIC_GOOGLE_CLIENT_ID.
- For production, both must be available at build-time (Docker build args) to be inlined into client bundle; also set at runtime is fine for server rewrites.
- Backend FastAPI expects analysis modules mounted at /app/src (sys.path insert to parent.parent/'src'). Mount host ./src/src -> container /app/src.
- Backend env keys: GEMINI_API_KEY, GOOGLE_DRIVE_API_KEY.
- Backend Dockerfile healthcheck uses curl; ensure curl installed.
- Compose dev: pass env via environment; Compose prod: pass build.args and environment for frontend, and mount /app/src for backend.