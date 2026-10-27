FROM python:3.14-slim

WORKDIR /app

# Install packages first so Docker can reuse this layer when only our code changes
COPY app_flask/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app_flask/ .

EXPOSE 5000

# Create any missing tables, then start the app on all interfaces so the host can reach it
CMD ["sh", "-c", "flask --app nutrition init-db && flask --app nutrition run --host 0.0.0.0"]
