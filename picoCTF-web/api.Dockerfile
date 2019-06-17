# picoCTF Flask API

FROM python:3.7-slim
RUN pip install gunicorn
WORKDIR /picoCTF
COPY ./requirements/common.txt ./requirements.txt
COPY ./api ./api
RUN pip install -r requirements.txt
CMD ["gunicorn", "--max-requests", "2000", "-b", "0.0.0.0:5000", "-w", "2", "api:create_app()"]
