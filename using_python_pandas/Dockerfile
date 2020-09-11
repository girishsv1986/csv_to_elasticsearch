FROM python:3.7 as base

COPY app/requirements.txt /tmp/es_app/

RUN pip3 install --upgrade pip && pip3 install -r /tmp/es_app/requirements.txt

WORKDIR /root/

COPY app/* /root/

#CMD ["python", "csv_to_es_using_pandas.py"]
CMD ["sh", "wait_to_start.sh"]