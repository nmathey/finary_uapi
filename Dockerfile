FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1 \
    FINARY_DATA_DIR=/data \
    MCP_TRANSPORT=http \
    MCP_HOST=0.0.0.0 \
    MCP_PORT=8000

WORKDIR /app
COPY . /app

# finary_uapi + dépendances du serveur.
# IMPORTANT : mcp < 2, car mcp_server.py utilise l'API à décorateurs (@app.list_tools).
# Si "pip install ." échoue (pas de pyproject), installer les dépendances à la main :
#   pip install curl_cffi docopt requests ...
RUN pip install --no-cache-dir . "mcp>=1.9,<2" uvicorn pyotp

RUN useradd -m app && mkdir -p /data && chown -R app /data
USER app

EXPOSE 8000
VOLUME ["/data"]
CMD ["python", "/app/mcp_server.py"]