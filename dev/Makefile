start.all:
	docker-compose --profile full-expenses-bot up -d --build

start.bot:
	docker-compose --profile just-expenses-bot up -d --build

logs.bot:
	docker-compose logs -f bot

logs.connector:
	docker-compose logs -f connector

logs.db:
	docker-compose logs -f bot-db

logs.cache:
	docker-compose logs -f cache
