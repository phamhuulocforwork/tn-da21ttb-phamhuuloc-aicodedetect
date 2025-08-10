# Suggested Commands

Backend (from `/home/huuloc/Github/tn-da21ttb-phamhuuloc-aicodedetect-ml-py/src/backend`):

```bash
# one-time setup
make setup

# dev (reload)
make dev

# prod
make start

# cleanup
make clean
```

Alternative python venv (if Makefile not used):

```bash
python3.12 -m venv .venv && source .venv/bin/activate
pip install --upgrade pip && pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

Frontend (from `/home/huuloc/Github/tn-da21ttb-phamhuuloc-aicodedetect-ml-py/src/frontend`):

```bash
npm install
npm run dev # http://localhost:3000

# build & preview
npm run build && npm run start
```

API quick test:

```bash
curl -s http://localhost:8000/health | jq
curl -s -X POST http://localhost:8000/analyze-code \
  -H 'Content-Type: application/json' \
  -d '{"code":"int main(){return 0;}","language":"c"}' | jq
```