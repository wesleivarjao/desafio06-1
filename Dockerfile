# Descomplicando Docker 9.09 **NAO NECESSARIO ALPINE
FROM python:3

MAINTAINER Victor

ENV FLASK_APP=myapp.py
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY myapp /myapp
COPY entrypoint.sh /usr/bin/entrypoint.sh
RUN chmod +x /usr/bin/entrypoint.sh
WORKDIR /myapp
EXPOSE 5000
ENTRYPOINT ["/usr/bin/entrypoint.sh"]
