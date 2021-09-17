from typing import Optional
# pip intall flask
from flask import Flask, request, jsonify
# pip install httpie - para testes no terminal
# pip install flask-pydantic-spec
from flask_pydantic_spec import FlaskPydanticSpec, Request, Response
from pydantic import BaseModel
#pip install tinydb
from tinydb import TinyDB, Query


server = Flask(__name__)     # Rota , EndPoint , Recurso ...
spec = FlaskPydanticSpec('flask', title='TESTE API REST')
spec.register(server)
database = TinyDB('database.json')

class Pessoa(BaseModel):
  id: Optional[int]
  nome: str
  idade: int

@server.get('/pessoas')
@spec.validate()
def pegar_pessoas():
    """Retorna Resultado do coneúdo do Banco de dados."""
    return jsonify(database.all())

@server.post('/pessoas')
@spec.validate(
 body=Request(Pessoa), resp=Response(HTTP_200=Pessoa)
               )
def inserir_pessoa():
    body = request.context.body.dict()
    """Insere dados no Banco de dados."""
    database.insert(body)
    return body

server.run()
