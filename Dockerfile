FROM python:3.8
FROM redis 
COPY . /apiapp
WORKDIR /apiapp
RUN pip install -r requirements.txt
EXPOSE 5000
CMD python ./API.py
