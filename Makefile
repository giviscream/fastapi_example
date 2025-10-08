# Makefile

# По умолчанию используется .env.dev и основной docker-compose.yml
ENV_FILE ?= envs/.env.dev
COMPOSE_FILE ?= docker-compose.yml
DETACHED ?= false
MIGRATE ?= false

build:
	@echo "Building with compose file: $(COMPOSE_FILE) and env file: $(ENV_FILE)"
	docker compose -f $(COMPOSE_FILE) --env-file $(ENV_FILE) build

up:
	@echo "Starting with compose file: $(COMPOSE_FILE) and env file: $(ENV_FILE)"
	docker compose -f $(COMPOSE_FILE) --env-file $(ENV_FILE) up

down:
	@echo "Stopping containers using: $(COMPOSE_FILE)"
	docker compose -f $(COMPOSE_FILE) --env-file $(ENV_FILE) down

logs:
	@echo "Showing logs for: $(COMPOSE_FILE)"
	docker compose -f $(COMPOSE_FILE) --env-file $(ENV_FILE) logs -f app

bash:
	@echo "Opening bash in app container using: $(COMPOSE_FILE)"
	docker compose -f $(COMPOSE_FILE) --env-file $(ENV_FILE) exec app bash

migrate:
	@echo "Running migrations using: $(COMPOSE_FILE) and env file: $(ENV_FILE)"
	docker compose -f $(COMPOSE_FILE) --env-file $(ENV_FILE) run --rm app alembic upgrade head

rebuild:
	@echo "🧹 Removing containers, images, and volumes..."
	docker compose -f $(COMPOSE_FILE) --env-file $(ENV_FILE) down -v --rmi all

	@echo "🔨 Rebuilding images from scratch..."
	docker compose -f $(COMPOSE_FILE) --env-file $(ENV_FILE) build --no-cache

	@echo "🚀 Starting containers..."
ifeq ($(DETACHED),true)
	docker compose -f $(COMPOSE_FILE) --env-file $(ENV_FILE) up -d
else
	docker compose -f $(COMPOSE_FILE) --env-file $(ENV_FILE) up &
endif

ifeq ($(MIGRATE),true)
	@echo "🧩 Applying migrations after rebuild..."
	sleep 5 && $(MAKE) migrate ENV_FILE=$(ENV_FILE) COMPOSE_FILE=$(COMPOSE_FILE)
endif
