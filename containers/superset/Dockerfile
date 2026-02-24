FROM apache/superset:latest

USER root

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        gcc \
        build-essential \
        libsasl2-dev \
        libsasl2-2 \
        libsasl2-modules \
        libssl-dev \
        python3-dev \
    && rm -rf /var/lib/apt/lists/*

RUN . /app/.venv/bin/activate && \
    uv pip install \
        pyhive==0.7.0 \
        sasl==0.3.1 \
        thrift_sasl==0.4.3 

USER superset


CMD ["/app/docker/entrypoints/run-server.sh"]
