# Makefile for BombSquad Server Development
# Usage: make <target>

.PHONY: help dev dev-build dev-down dev-logs dev-shell prod prod-build prod-down prod-logs clean

# Colors for output
BLUE := \033[0;34m
GREEN := \033[0;32m
YELLOW := \033[0;33m
RED := \033[0;31m
NC := \033[0m # No Color

# Docker Compose files
DEV_COMPOSE := -f docker-compose.yml -f docker-compose.dev.yml
PROD_COMPOSE := -f docker-compose.yml

help: ## Show this help message
	@echo "$(BLUE)BombSquad Server - Development Commands$(NC)"
	@echo ""
	@echo "$(GREEN)Development:$(NC)"
	@echo "  make dev          - Start development server with auto-reload"
	@echo "  make dev-build    - Build development image"
	@echo "  make dev-down     - Stop development server"
	@echo "  make dev-logs     - View development logs"
	@echo "  make dev-shell    - Open shell in development container"
	@echo ""
	@echo "$(GREEN)Production:$(NC)"
	@echo "  make prod         - Start production server"
	@echo "  make prod-build   - Build production image"
	@echo "  make prod-down    - Stop production server"
	@echo "  make prod-logs    - View production logs"
	@echo ""
	@echo "$(GREEN)Utilities:$(NC)"
	@echo "  make clean        - Remove all containers and volumes"
	@echo "  make status       - Show container status"
	@echo "  make help         - Show this help message"

# Development targets
dev: ## Start development server with auto-reload
	@echo "$(GREEN)Starting development server with auto-reload...$(NC)"
	docker compose $(DEV_COMPOSE) up

dev-build: ## Build development image
	@echo "$(GREEN)Building development image...$(NC)"
	docker compose $(DEV_COMPOSE) build

dev-down: ## Stop development server
	@echo "$(YELLOW)Stopping development server...$(NC)"
	docker compose $(DEV_COMPOSE) down

dev-logs: ## View development logs (follow mode)
	@echo "$(BLUE)Following development logs... (Ctrl+C to exit)$(NC)"
	docker compose $(DEV_COMPOSE) logs -f

dev-shell: ## Open bash shell in development container
	@echo "$(BLUE)Opening shell in development container...$(NC)"
	docker compose $(DEV_COMPOSE) exec bombsquad-server bash

dev-restart: ## Restart development server
	@echo "$(YELLOW)Restarting development server...$(NC)"
	docker compose $(DEV_COMPOSE) restart

# Production targets
prod: ## Start production server
	@echo "$(GREEN)Starting production server...$(NC)"
	docker compose $(PROD_COMPOSE) up -d
	@echo "$(GREEN)Server started in background. Use 'make prod-logs' to view logs.$(NC)"

prod-build: ## Build production image
	@echo "$(GREEN)Building production image...$(NC)"
	docker compose $(PROD_COMPOSE) build

prod-down: ## Stop production server
	@echo "$(YELLOW)Stopping production server...$(NC)"
	docker compose $(PROD_COMPOSE) down

prod-logs: ## View production logs (follow mode)
	@echo "$(BLUE)Following production logs... (Ctrl+C to exit)$(NC)"
	docker compose $(PROD_COMPOSE) logs -f

prod-restart: ## Restart production server
	@echo "$(YELLOW)Restarting production server...$(NC)"
	docker compose $(PROD_COMPOSE) restart

# Utility targets
status: ## Show container status
	@echo "$(BLUE)Container Status:$(NC)"
	@docker compose $(PROD_COMPOSE) ps 2>/dev/null || echo "Production not running"
	@docker compose $(DEV_COMPOSE) ps 2>/dev/null || echo "Development not running"

clean: ## Remove all containers, volumes, and images
	@echo "$(RED)This will remove ALL BombSquad containers, volumes, and images!$(NC)"
	@read -p "Are you sure? [y/N] " -n 1 -r; \
	echo; \
	if [[ $$REPLY =~ ^[Yy]$$ ]]; then \
		echo "$(RED)Cleaning up...$(NC)"; \
		docker compose $(DEV_COMPOSE) down -v 2>/dev/null || true; \
		docker compose $(PROD_COMPOSE) down -v 2>/dev/null || true; \
		docker rmi bombsquad-indonesia-bombsquad-server 2>/dev/null || true; \
		echo "$(GREEN)Cleanup complete!$(NC)"; \
	else \
		echo "$(YELLOW)Cleanup cancelled.$(NC)"; \
	fi

# Plugin development helpers
plugin-check: ## Check Python syntax in mods/
	@echo "$(BLUE)Checking Python syntax in mods/...$(NC)"
	@python3 -m py_compile mods/*.py 2>/dev/null && echo "$(GREEN)✓ All plugins are valid$(NC)" || echo "$(RED)✗ Syntax errors found$(NC)"

plugin-reload: ## Trigger plugin reload by touching file
	@echo "$(BLUE)Triggering plugin reload...$(NC)"
	@touch mods/server_customizations.py
	@echo "$(GREEN)Plugin file touched. Development server will auto-reload.$(NC)"

# Quick aliases
up: dev ## Alias for 'make dev'
down: dev-down ## Alias for 'make dev-down'
logs: dev-logs ## Alias for 'make dev-logs'
shell: dev-shell ## Alias for 'make dev-shell'
build: dev-build ## Alias for 'make dev-build'
