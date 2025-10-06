#!/bin/sh
echo "⏳ Waiting for RabbitMQ to be ready..."
while ! nc -z rabbitmq 5672; do
  sleep 1
done
echo "✅ RabbitMQ is up, starting worker..."
python3 /app/rabbitmq_utils.py
