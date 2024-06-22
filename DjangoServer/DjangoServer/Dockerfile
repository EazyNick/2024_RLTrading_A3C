FROM python:3.9

WORKDIR /app

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

# Ensure log directory exists and set permissions
RUN mkdir -p /app/utils/Log && chown -R www-data:www-data /app/utils/Log && chmod -R 755 /app/utils/Log

COPY uwsgi.ini /app/

# Change user to www-data to avoid permission issues
USER www-data

CMD ["uwsgi", "--ini", "uwsgi.ini"]