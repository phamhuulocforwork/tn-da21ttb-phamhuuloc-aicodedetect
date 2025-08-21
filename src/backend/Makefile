PYTHON = python3.13
VENV = venv
VENV_BIN = $(VENV)/bin
PIP = $(VENV_BIN)/pip
PYTHON_VENV = $(VENV_BIN)/python

GREEN = \033[0;32m
BLUE = \033[0;34m
YELLOW = \033[1;33m
RED = \033[0;31m
NC = \033[0m

.PHONY: help
help:
	@echo "$(BLUE)AI Code Detection Backend - Available Commands:$(NC)"
	@echo "$(GREEN)  make setup$(NC)     - Tạo virtual environment và cài đặt dependencies"
	@echo "$(GREEN)  make install$(NC)   - Cài đặt/update dependencies"
	@echo "$(GREEN)  make dev$(NC)       - Chạy server development với hot reload"
	@echo "$(GREEN)  make start$(NC)     - Chạy server production"
	@echo "$(GREEN)  make clean$(NC)     - Xóa virtual environment và cache"

setup:
	@echo "$(YELLOW)📦 Creating virtual environment...$(NC)"
	$(PYTHON) -m venv $(VENV)
	@echo "$(YELLOW)📚 Installing dependencies...$(NC)"
	$(PIP) install --upgrade pip setuptools wheel
	$(PIP) install -r requirements.txt --only-binary=:all:
	@echo "$(GREEN)✅ Setup completed!$(NC)"

install:
	@echo "$(YELLOW)📚 Installing/updating dependencies...$(NC)"
	$(PIP) install --upgrade pip setuptools wheel
	$(PIP) install -r requirements.txt --only-binary=:all:
	@echo "$(GREEN)✅ Dependencies installed!$(NC)"

dev:
	@echo "$(BLUE)🚀 Starting development server...$(NC)"
	@echo "$(BLUE)📱 Server: http://localhost:8000$(NC)"
	@echo "$(BLUE)📖 API Docs: http://localhost:8000/docs$(NC)"
	@echo "$(YELLOW)🛑 Press Ctrl+C to stop$(NC)"
	@echo ""
	$(VENV_BIN)/uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

start:
	@echo "$(BLUE)🚀 Starting production server...$(NC)"
	$(VENV_BIN)/uvicorn app.main:app --host 0.0.0.0 --port 8000

clean:
	@echo "$(RED)🧹 Cleaning up...$(NC)"
	rm -rf $(VENV)
	find . -type d -name "venv" -exec rm -rf {} +
	find . -type d -name "__pycache__" -delete
	find . -type f -name "*.pyc" -delete
	@echo "$(GREEN)✅ Cleanup completed!$(NC)"

quick: dev 