install:
	uv sync

dev:
	uv run manage.py runserver

build:
	./build.sh

render-start:
	gunicorn task_manager.wsgi

collectstatic:
	uv run manage.py collectstatic --no-input

migrate:
	uv run manage.py migrate