FROM python:3.12-alpine AS builder

WORKDIR /app

COPY requirements.txt ./

RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

COPY . .


FROM gcr.io/distroless/python3-debian12

WORKDIR /app

COPY --from=builder /install /usr/local
COPY --from=builder /app /app

ENV HOST=0.0.0.0
ENV PORT=3002
ENV WORKERS=4
ENV APP_MODULE=app:app

EXPOSE 3002

CMD ["sh", "-c", "gunicorn --bind ${HOST}:${PORT} --workers ${WORKERS} ${APP_MODULE}"]