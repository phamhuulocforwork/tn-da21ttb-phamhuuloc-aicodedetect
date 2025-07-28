# Suggested Commands - Các lệnh thường dùng

## System Commands (Linux/WSL)
- `ls -la` - List files with details
- `cd <directory>` - Change directory  
- `pwd` - Print working directory
- `cat <file>` - Display file content
- `grep -r "<pattern>" .` - Search pattern in files
- `find . -name "<pattern>"` - Find files by name
- `tree` - Display directory structure (if installed)

## Git Commands
- `git status` - Check repository status
- `git add .` - Stage all changes
- `git commit -m "<message>"` - Commit with message
- `git push` - Push to remote repository
- `git pull` - Pull latest changes
- `git log --oneline` - View commit history

## Backend Development (src/backend/)
- `cd src/backend` - Navigate to backend
- `make setup` - Create venv and install dependencies
- `make dev` - Start development server (http://localhost:8000)
- `make start` - Start production server
- `make clean` - Clean venv and cache
- `source venv/bin/activate` - Activate virtual environment manually

## Frontend Development (src/frontend/)
- `cd src/frontend` - Navigate to frontend
- `npm install` - Install dependencies
- `npm run dev` - Start development server (http://localhost:3000)
- `npm run build` - Build for production
- `npm run lint` - Run ESLint
- `npm run format` - Format code with Prettier
- `npm run clean` - Clean build files

## ML/Data Science (src/src/)
- `cd src/src` - Navigate to ML workspace
- `make setup` - Setup Python environment
- `python3 -m venv venv` - Create virtual environment
- `source venv/bin/activate` - Activate environment  
- `pip install -r requirements.txt` - Install dependencies
- `jupyter notebook` - Start Jupyter (if installed)
- `python scripts/create_metadata.py` - Run metadata creation
- `python features/gemini_res.py` - Generate AI code samples

## Useful Utilities
- `make help` - Show available make commands (trong backend/frontend)
- `which python3` - Find Python location
- `node --version` - Check Node.js version
- `npm --version` - Check npm version