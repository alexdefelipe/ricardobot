FROM python:3.8-alpine

#RUN apk add --update \
#    python3-dev

ADD ricardobot /ricardobot

COPY requirements.txt /ricardobot
RUN pip install -r /ricardobot/requirements.txt

COPY ricardobot/. /ricardobot
#ENV PYTHONPATH "${PYTHONPATH}:/ricardobot"

ENTRYPOINT [ "python3" ]
CMD [ "ricardobot/app.py" ]
