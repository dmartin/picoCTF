FROM python:3.7
WORKDIR /app
COPY setup.py .
COPY api ./api
RUN pip3 install .
EXPOSE 8000
ENTRYPOINT [ "gunicorn", "-b", "127.0.0.1:8000", "-k", "eventlet", "-w", "2", "api:create_app()"]
