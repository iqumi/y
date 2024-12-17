target: up

up:  ## Run all inside docker
	docker compose up -d

down:  ## Stop and delete containers
	docker compose down --rmi local

test:  ## Run tests
	docker compose up -d --build
	docker exec -w /app/server chat-server pytest --no-header -vv --color=yes
	# docker compose down # --rmi local
