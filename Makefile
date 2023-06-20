shell:
	docker-compose run --rm api bash

up:
	docker-compose up

migrate_db:
	./manage.py makemigrations
	./manage.py migrate

show_mgrs:
	./manage.py showmigrations