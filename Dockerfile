FROM python:3.7.4

ENV PYTHONUNBUFFERED 1
ENV LANG=en_US.UTF-8
ENV LC_ALL=en_US.UTF-8
ENV FLASK_APP="/code/lego/__init__.py"
ENV FLASK_DEBUG=1
RUN mkdir /code
WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt
COPY . /code/

CMD flask run --host=0.0.0.0 --port=5000 --no-debugger --with-threads --no-reload