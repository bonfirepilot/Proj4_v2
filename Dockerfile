FROM python:3.8
ENV REDIS_HOST localhost
ENV REDIS_PORT 6379
COPY . /apiapp
WORKDIR /apiapp
RUN pip install -r requirements.txt
EXPOSE 5000
CMD python ./API.py
