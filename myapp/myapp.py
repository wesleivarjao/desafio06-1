# Configuracao do Flask
from os import environ
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy # https://leportella.com/tutorial-basico-sqlalchemy.html
from rq import Queue
import redis

# Criacao do app Flask
myapp = Flask(__name__)
myapp.config['SQLALCHEMY_DATABASE_URI'] = environ.get('SQLALCHEMY_DATABASE_URI') # https://flask-sqlalchemy.palletsprojects.com/en/2.x/config/
# myapp.config['SQLALCHEMY_DATABASE_URI'] = String **CASO NÃO PASSASSE NO DOCKER RUN
db = SQLAlchemy(myapp)
redis_url = environ.get('REDISTOGO_URL') # https://devcenter.heroku.com/articles/redistogo
# redis_url = urlparse.urlparse(os.environ.get('REDISTOGO_URL', 'String')) **CASO NÃO PASSASSE NO DOCKER RUN

# Desenvolvimento Hello World!
@myapp.route('/')
def hello_world():
    return 'Hello World'

# Desenvolvimento consulta db
def db_consult():
    try:
        db.session.query("1").all()
        return 'OK'
    except:
        return 'Not OK'

# Desenvolvimento consulta redis URL
try:
    redis_conn = redis.from_url(redis_url)
    redis_status = 'OK'
except:
    redis_status = 'Not OK'

# https://python-rq.org/docs/connections/
# https://python-rq-docs-cn.readthedocs.io/en/latest/
def count_queue():
    a = Queue(0, connection=redis_conn)
    s = Queue(1, connection=redis_conn)
    q = a.count + s.count
    if q >= 1:
        status = "Fila"
    else:
        status = "Sem fila"
    return status

# https://stackoverflow.com/questions/45412228/sending-json-and-status-code-with-a-flask-response
@myapp.route('/api/monitoring')
def service_status():
    data_sheet = {}
    data_sheet['API'] = {}
    data_sheet['API']['api'] = "1.0"
    data_sheet['API']['dep'] = {}
    data_sheet['API']['dep']['db-sql'] = db_consult()
    data_sheet['API']['dep']['db-nosql'] = redis_status
    data_sheet['API']['dep']['Fila status'] = count_queue()
    data_sheet['API']['dep']['status'] = "200"
    return jsonify(data_sheet)
 
if __name__ == '__main__':
    myapp.run()




