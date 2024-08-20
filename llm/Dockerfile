FROM python:alpine

WORKDIR /app

RUN apk add --no-cache build-base curl\
    && pip install --no-cache-dir virtualenv

RUN virtualenv venv
ENV PATH="/app/venv/bin:$PATH"

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY /app .

ENV REDIS_HOST=redis-service
ENV REDIS_PORT=6379

EXPOSE 4001

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "4001"]