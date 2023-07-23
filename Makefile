THIS_FILE := $(lastword $(MAKEFILE_LIST))
.PHONY: help up local_up down logs db style migrate revision
help:
	make -pRrq  -f $(THIS_FILE) : 2>/dev/null | awk -v RS= -F: '/^# File/,/^# Finished Make data base/ {if ($$1 !~ "^[#.]") {print $$1}}' | sort | grep -v -e '^[^[:alnum:]]' -e '^$@$$'
up:
	docker compose pull
	docker compose up --remove-orphans -d
down:
	docker compose -f docker-compose.yml down $(c)
local_up:
	export UID=1000 ; export GID=1000 ; docker compose -f docker-compose-local.yml up --build --remove-orphans -d $(c)
logs:
	docker compose -f docker-compose.yml logs --tail=100 -f "$(c)"
db:
	docker compose -f docker-compose.yml exec postgres psql -U admin admin_db
style:
	black backend && isort backend --profile black --filter-files
revision:
	docker exec -it backend alembic revision --autogenerate -m $(c)
migrate:
	docker exec -it backend alembic upgrade head