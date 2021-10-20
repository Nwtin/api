import sqlite3
import json,requests
#from flask import Flask,request,Response,jsonify,render_template
from sanic import Sanic
from sanic.response import text
from sanic.request import Request


db2 = sqlite3.connect("./ConsultaNome.db",check_same_thread=False)

app = Sanic(__name__)



def ConsultaCPFSimples(cpf:str):
    cur = db2.cursor()
    cur.execute('select * from Brasil where Cpf=?',[cpf])
    try:
        dados = cur.fetchall()[0]
        dadosSimples = {'Nome':dados[0],
                        'Cpf':dados[1],
                        'Genero':dados[2],
                        'Nascimento':dados[3][:-1]}
    except:
        dadosSimples = {"erro":"cpf n existe"}
    cur.close()
    return json.dumps(dadosSimples)

def ConsultaNome(nome:str):
    c = db2.cursor()
    c.execute("select * from Brasil where nome like ?",[nome+"%"])
    try:
        dados = c.fetchall()[0]
        dadosSimples = {'Nome':dados[0],
                        'Cpf':dados[1],
                        'Genero':dados[2],
                        'Nascimento':dados[3][:-1]}
    except:
        dadosSimples = {"erro":"cpf n existe"}
    c.close()
    return json.dumps(dadosSimples)

@app.route("/",methods = ['POST',"GET"])
def Server(request:Request):
    parameters = request.args

    if "nome" in parameters:
        nome = parameters.get("nome")
        return text(ConsultaNome(nome))

    if "cpfSimples" in parameters:
        cpf = parameters.get("cpfSimples")
        return text(ConsultaCPFSimples(cpf))


app.run(host="0.0.0.0", port=8888,debug=False,access_log=False)