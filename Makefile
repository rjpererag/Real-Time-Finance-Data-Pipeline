DB_NAME=postgres
DB_USER=postgres
DB_HOST=localhost
DB_PORT=5432
DB_PASSWORD=mypassword

SCHEMA=src/database/schema/schema.sql

# DOCKER ORCHESTRATION

.PHONY: wait_for_flink
wait_for_flink:
	@./scripts/wait_for_flink.sh

.PHONY: start_consumer
start_consumer:
	@echo "Submitting consumer to flink"
	docker exec -it -e PYTHONPATH=/opt/flink/usrlib flink-jobmanager ./bin/flink run \
			--detached \
			-py /opt/flink/usrlib/src/consumer.py

.PHONY: up
up:
	@echo "Starting pipeline"
	@docker compose up -d
	@make wait_for_flink
	@make start_consumer

.PHONY: down
down:
	@echo "Stopping containers"
	@docker compose down

.PHONY: down-full
down-full:
	@echo "Stopping containers and removing volumes"
	@docker compose down -v

.PHONY: reset
reset:
	@echo "Shutting down ...."
	@make down-full
	@sleep 10
	@echo "Rebooting ..."
	@make up


# DB MANAGEMENT

.PHONY: db-init
db-init:
	@echo "Creating database $(DB_NAME)..."
	PGPASSWORD=$(DB_PASSWORD) psql -U $(DB_USER) -h $(DB_HOST) -p $(DB_PORT) -d postgres -c "CREATE DATABASE $(DB_NAME);"
	#$(call psql_exec, "CREATE DATABASE $(DB_NAME);")
	@echo "Database $(DB_NAME) created."

## Create tables from schema.sql
.PHONY: db-create-schema
db-create-schema:
	@echo "Applying schema..."
	PGPASSWORD=$(DB_PASSWORD) psql -U $(DB_USER) -h $(DB_HOST) -p $(DB_PORT) -d $(DB_NAME) -f $(SCHEMA)

## Drop database
.PHONY: db-drop
db-drop:
	@echo "Dropping database..."
	PGPASSWORD=$(DB_PASSWORD) psql -U $(DB_USER) -h $(DB_HOST) -p $(DB_PORT) -d postgres -c "DROP DATABASE IF EXISTS $(DB_NAME);"


.PHONE: db-build-db
db-build-db:
	@echo "Initializing database $(DB_NAME)"
	$(MAKE) db-init

	@echo "$(DB_NAME) initialized successfully"
	$(MAKE) db-create-schema
	@echo "Schema created successfully"
