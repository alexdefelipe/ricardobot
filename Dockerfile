FROM python:3.8.12-slim-buster

RUN apt update

ADD ricardobot /ricardobot

COPY requirements.txt /ricardobot
RUN pip install -r /ricardobot/requirements.txt

COPY ricardobot/. /ricardobot
ENV PYTHONPATH "${PYTHONPATH}:/ricardobot"

ENTRYPOINT [ "python3" ]
CMD [ "ricardobot/app.py" ]
