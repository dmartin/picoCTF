FROM python:3.7
WORKDIR /app
COPY . .
RUN pip3 install .
EXPOSE 8000
ENTRYPOINT [ "gunicorn", "-b", "0.0.0.0:8000", "-k", "eventlet", "-w", "2", "api:create_app()"]
