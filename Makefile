build:
	docker-compose build --parallel

up: build
	echo "Starting containers..."
	docker-compose up --detach

down:
	echo "Stopping containers..."
	docker-compose down --remove-orphans

logs:
	echo "Showing logs..."
	docker-compose logs --follow

integration-tests:
	echo "Running Integration Tests..."
	docker-compose run tavern