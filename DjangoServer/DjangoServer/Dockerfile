FROM python:3.9

WORKDIR /app

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

COPY uwsgi.ini /app/

CMD ["uwsgi", "--ini", "uwsgi.ini"]