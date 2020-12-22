FROM python:3.8.1-alpine3.11

WORKDIR /tmp

RUN \
  apk add --no-cache \
    git \
    git-fast-import \
    openssh \
  && apk add --no-cache --virtual .build gcc musl-dev \
  && /usr/local/bin/python -m pip install --upgrade pip \
  && pip install --no-cache-dir \
        'mkdocs' \
        #'mkdocs-with-pdf' \
  && apk del .build gcc musl-dev \
  && rm -rf /tmp/*

WORKDIR /docs

EXPOSE 8000

# Start development server by default
ENTRYPOINT ["mkdocs"]
CMD ["serve", "--dev-addr=0.0.0.0:8000"]