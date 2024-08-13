FROM python:3.10-slim-buster

LABEL maintener="MD. ASHIKUN NABI"

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /var/www/html

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    libcairo2 \
    libpango1.0-0 \
    python3-cffi \
    libpangocairo-1.0.0 \
    libgdk-pixbuf2.0-0 \
    libpangocairo-1.0.0 \
    libffi-dev \
    libmemcached-dev \
    libz-dev \
    libpcap-dev \
    libpq-dev \
    libreoffice-writer \
    libreoffice-gtk3 \
    xpdf \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get remove -y \
    libffi-dev \
    libz-dev \
    libpcap-dev \
    libmemcached-dev \
    libpq-dev

COPY requirements.txt .

RUN python -m pip install --upgrade pip \
    && pip install -r requirements.txt --no-deps --no-cache-dir

COPY . .

COPY ./docker/web/start /start
RUN sed -i 's/\r//' /start
RUN chmod +x /start
