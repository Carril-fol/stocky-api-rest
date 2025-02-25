FROM python:3.12-alpine3.18

RUN apk add --no-cache \
    python3-dev \
    postgresql-dev \
    gcc \
    musl-dev

RUN pip3 install --upgrade pip

WORKDIR /restful-inventory-management-system 

COPY . /restful-inventory-management-system

RUN pip3 --no-cache-dir install -r requirements.txt

CMD ["python", "src/app.py"]
