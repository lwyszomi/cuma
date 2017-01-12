FROM python:2.7
ENV PYTHONUNBUFFERED 1
WORKDIR /code

RUN curl -sL https://deb.nodesource.com/setup_7.x | bash - && apt-get install -yq nodejs

COPY requirements.txt /code/
COPY bower.json /code/

RUN npm install -g bower && bower install --allow-root && pip install -r requirements.txt
