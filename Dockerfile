FROM python:3.9.9-slim-buster as python_app
WORKDIR /app
COPY . /app/
RUN pip install -r requirements.txt

# all network bind to port 5000 for gunicorn server
CMD ["gunicorn", "--timeout", "1000", "-b", "0.0.0.0:5000", "app:app"]