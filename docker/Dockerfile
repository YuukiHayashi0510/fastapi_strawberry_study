FROM python:alpine

WORKDIR /usr/src/api

RUN apk --no-cache add tzdata && \
    cp /usr/share/zoneinfo/Asia/Tokyo /etc/localtime && \
    apk del tzdata

ADD requirements.txt ./

RUN apk add --no-cache postgresql-libs \
    && apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev \
    && python3 -m pip install -r requirements.txt --no-cache-dir \
    && apk --purge del .build-deps


CMD ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]
