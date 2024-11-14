FROM python:3.13-alpine
WORKDIR /app
COPY . .
RUN pip install --upgrade pip && pip install -r requirements.txt
CMD [ "python", "app.py" ]