FROM python:3.6-alpine

RUN apk update && apk add pkgconfig && apk add freetype-dev && apk add libpng && apk add build-base

# We copy just the requirements.txt first to leverage Docker cache
ADD requirements.txt .

RUN pip install --upgrade pip && pip install -r requirements.txt

WORKDIR /app

COPY . .

EXPOSE 5000

ENTRYPOINT [ "python", "-m", "flask", "run", "--host=0.0.0.0" ]
