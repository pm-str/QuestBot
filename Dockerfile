FROM python:3.6
ENV env docker
RUN mkdir /source
WORKDIR /source

ADD requirements.txt /source
RUN pip install -r requirements.txt
ADD . /source/

RUN python manage.py makemigrations
RUN python manage.py migrate
