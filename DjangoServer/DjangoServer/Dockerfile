FROM python:3.9

WORKDIR /app

# Copy and install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . /app/

# Ensure log directory exists and set permissions
RUN mkdir -p /app/utils/Log
RUN chown -R www-data:www-data /app/utils/Log
RUN chmod -R 755 /app/utils/Log

# Copy uwsgi configuration
COPY uwsgi.ini /app/

# Change user to www-data to avoid permission issues
USER www-data

CMD ["uwsgi", "--ini", "uwsgi.ini"]
