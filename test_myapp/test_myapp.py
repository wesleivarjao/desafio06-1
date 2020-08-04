import requests
import sys

enderecomyapp = '191.235.114.87:5000/api/monitoring'
requisicao = requests.get("http://{}".format(enderecomyapp)).json()
if float(requisicao.get('status') == 404:
    print('Seguindo')
    print(requisicao)
else:
    print('Seguindo com o rollback')
    print(requisicao)
    sys.exit(10)

