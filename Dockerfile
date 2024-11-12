FROM python:3.14-slim
WORKDIR /app
COPY . .
RUN pip install --upgrade pip && pip install -r requirements.txt
CMD [ "gunicorn", "-b", "0.0.0.0:5000", "-w", "5", "wsgi:app" ]