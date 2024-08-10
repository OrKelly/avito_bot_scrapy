FROM python:3.9

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /bot

RUN apt-get update && \
    apt-get install -y curl ca-certificates gnupg lsb-release && \
    (curl https://www.postgresql.org/media/keys/ACCC4CF8.asc | apt-key add -) && \
    echo "deb http://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list

RUN apt-get update && \
    apt-get install -y postgresql postgresql-client \
    build-essential libssl-dev libffi-dev \
    python3-dev cargo pkg-config && \
    apt-get clean

COPY requirements.txt .

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN chmod 0700 entrypoint.sh

RUN apt-get update

CMD ["/bin/bash", "./entrypoint.sh"]

