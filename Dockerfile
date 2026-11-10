FROM python:3.14-slim

WORKDIR /app

# Install packages first so Docker can reuse this layer when only our code changes
COPY app_flask/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app_flask/ .

EXPOSE 5000

# On every start: create missing tables, load the starter recipes and their macros,
# then start the app on all interfaces so the host can reach it.
# seed-recipes needs the internet and skips recipes already stored; if it fails,
# the app still starts with whatever recipes the volume already has.
CMD ["sh", "-c", "flask --app nutrition init-db && (flask --app nutrition seed-recipes || echo 'Could not download recipes; starting with the ones already stored.') && flask --app nutrition seed-ingredients && flask --app nutrition run --host 0.0.0.0"]
