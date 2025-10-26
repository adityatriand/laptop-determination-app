# Makefile for Laptop Determination App

.PHONY: help build up down restart logs shell clean

# Default target
help:
	@echo "Available commands:"
	@echo "  build     - Build Docker images"
	@echo "  up        - Start all services"
	@echo "  down      - Stop all services"
	@echo "  restart   - Restart all services"
	@echo "  logs      - Show logs for all services"
	@echo "  logs-web  - Show logs for web service"
	@echo "  logs-db   - Show logs for database service"
	@echo "  shell     - Open shell in web container"
	@echo "  shell-db  - Open MySQL shell"
	@echo "  clean     - Clean up containers and volumes"
	@echo "  prod      - Start production services"

# Development commands
build:
	docker-compose build

up:
	docker-compose up -d

down:
	docker-compose down

restart:
	docker-compose restart

logs:
	docker-compose logs -f

logs-web:
	docker-compose logs -f web

logs-db:
	docker-compose logs -f db

shell:
	docker-compose exec web bash

shell-db:
	docker-compose exec db mysql -u root -p

# Production commands
prod:
	docker-compose -f docker-compose.prod.yml up -d

prod-down:
	docker-compose -f docker-compose.prod.yml down

# Cleanup commands
clean:
	docker-compose down -v
	docker system prune -f

clean-all:
	docker-compose down -v --rmi all
	docker system prune -af
