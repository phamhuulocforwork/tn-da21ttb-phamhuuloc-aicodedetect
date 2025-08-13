PYTHON = python3.12
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

setup:
	@echo "$(YELLOW)📦 Creating virtual environment...$(NC)"
	$(PYTHON) -m venv $(VENV)
	@echo "$(YELLOW)📚 Installing dependencies...$(NC)"
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt
	@echo "$(GREEN)✅ Setup completed!$(NC)"

install:
	@echo "$(YELLOW)📚 Installing/updating dependencies...$(NC)"
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt
	@echo "$(GREEN)✅ Dependencies installed!$(NC)"