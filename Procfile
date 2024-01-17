worker_bot: python app.py
    @echo "Building $@"
    @docker build -t $@ .
worker_timer: python timer/auto_post.py
    @echo "Building $@"
    @docker build -t $@ .
web: uvicorn django_orm.asgi:application --host 0.0.0.0 --port 8080
    @echo "Building $@"
    @docker build -t $@ .