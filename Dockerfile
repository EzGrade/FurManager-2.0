FROM PYTHON:3.8

LABEL authors="abore"

ENTRYPOINT ["top", "-b"]

WORKDIR /

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

CMD ["python", "app.py"]

CMD ["python", "app.py"]