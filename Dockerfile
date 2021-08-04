# syntax=docker/dockerfile:1
FROM python:3.7
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
EXPOSE 5000
COPY . .
ENV FLASK_APP=scribble
ENV FLASK_ENV=dev
ENV FLASK_DEBUG=1
CMD ["flask", "run"]