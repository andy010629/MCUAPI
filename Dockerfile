FROM python:3.8
WORKDIR /mcu-api
ADD . /mcu-api
RUN pip3 install -r requirements.txt
CMD ["python3","app.py"]
EXPOSE 8000