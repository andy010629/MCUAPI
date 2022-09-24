FROM python:3.8
WORKDIR /docker-test
ADD . /docker-test
RUN pip3 install -r requirements.txt
CMD ["python3","app.py"]
EXPOSE 8000