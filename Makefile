.PHONY: run test migrate db-shell clean

# Start the Django development server
run:
	python manage.py runserver

# Run all tests
test:
	python manage.py test shortener/tests

# Apply database migrations
migrate:
	python manage.py makemigrations shortener
	python manage.py migrate

# Jump into the Postgres shell
db-shell:
	docker exec -it shortner-db psql -U postgres

# Clean up python cache files
clean:
	find . -name "__pycache__" -type d -exec rm -rf {} +