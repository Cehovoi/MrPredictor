up:
	docker-compose --env-file .env up -d
up_dev:
	docker-compose --env-file .env.dev up -d
up_dev_lite:
	docker-compose --env-file .env.dev.light up -d
down:
	docker-compose down

build:
	docker-compose --env-file .env up -d --build

build_dev:
	docker-compose --env-file .env.dev up -d --build


