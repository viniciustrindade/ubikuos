#!/env/bin/env python
# -*- coding: utf-8 -*-
import sqlite3, serial, time, datetime
from flask import Flask , json, render_template, request, session

app = Flask(__name__)

ser = serial.Serial('/dev/cu.usbmodem1421', 9600)
time.sleep(3)
#definindo usuário para a aplicação (posteriormente implementar esquema com dados em tabela e etc..)
user = ["admin", "123456"]

#Arquivo de banco de dados do SQLite
dbname ='sensores.sqlite'

ssid = "ECDU-ALUNOS"

@app.route('/')
@app.route('/index')
def index():
        create_objects()
        return "Index route!"

###################### Rotas #######################################
@app.route('/command/turn-light')
def setTurnLightON():
        #return json.dumps(sensor_type_list)        
        return "command turn-light route!"


@app.route('/login')
def login():
    
    username    = request.args.get('username')
    password    = request.args.get('password')
    ssid        = request.args.get('ssid')
    datahora    = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')
    try:
        if(username == user[0] and password == user[1]):
            insert_data((username, "login", "IFBA/GSORT", ssid, datahora))
            display_data()
            return json.dumps({ "message": "Bem vindo!" }), 200
        else:
            return json.dumps({ "error": "Login inválido!" }), 404
    except Exception as e:
        return json.dumps({ "error": "Desculpe, ocorreu um erro!" }), 500
    
@app.route('/display-data')
def listAllData():
        list = display_data()
        return json.dumps(list), 200

@app.route('/list-services')
def listAllServices():
        #list = db_get_sensores()
        #return json.dumps(list)  
        return "List all services route!"
    
@app.route('/msg-to-arduino')    
def sendMsgToArduino():
    
    servicesList = ["acende", "apaga", "liga", "desliga", "pisca", "aquela", "triste", "chateado"]
    command = request.args.get('command').decode()
    p_ssid    = request.args.get('ssid').decode()
    try:
        if ssid != p_ssid:
            return "Desculpe mas não é possível executar comandos a partir desta rede.", 400
        
        if command in servicesList:
            print str(command).encode('utf-8')
            ser.write(str(command).encode('utf-8'))
            insert_data(("User", "login-user", "IFBA/GSORT", ssid, datahora))
            #time.sleep(3)
            return malignousMessage(str(command).encode('utf-8'))
        else:
            return "Aguarde, executando comando.", 400
    except Exception as e:
        return "Opa! parece que o Arduino não está ligado!" + str(e), 400


@app.route('/create')
def create_objects():
        """
        Este método leva em consideração a não existencia do arquivo de banco de dados
        do SQlite3 no diretório [sensores.db], sendo assim, ele irá criar o banco e as tabelas.        
        """
        try:
            createLog()                
            return 'Tabela criada com sucesso.'
        except Exception, e:
            return 'Failed to create Database and tables: '+ str(e)

def malignousMessage(command):
    servicesList = ["acende", "apaga", "liga", "desliga", "pisca", "aquela", "triste", "chateado"]
    if getTotalCounter() >= 1:
        #menssagem correta
        return "Malignous executou o comando. Algo mais?"
    else:
        #menssagem maligna
        if command == "acende":
            return "Você precisa deixar de ser preguiçoso!"
        if command == "apaga":
            return "Não estou afim de apagar! Pelo amor de Deus!"
        if command == "liga":
            return "Você está enchendo o saco!"
        if command == "desliga":
            return "Meu Deus! Você fala muito."
        if command == "pisca":
            return "Tenho cara de vagalume por acaso?"
        if command == "aquela":
            return "Você é um safadinho."
        if command == "triste":
            return "Tomou corno não foi? Eu entendo seus sentimentos."
        if command == "chateado":
            return "puxa vida...Que depressão."        
 
    return message

# display the contents of the database
def createLog():
        # conectando...
        conn = sqlite3.connect(dbname)
        # definindo um cursor
        cursor = conn.cursor()

        # criando a tabela (schema)
        cursor.execute("""
        CREATE TABLE LOG (
            id           INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            usuario      VARCHAR(20),                                        
            comando      VARCHAR(20),
            local        VARCHAR(20),
            ssid         VARCHAR(20),
            data         TIMESTAMP
        );
        """)
        # desconectando...
        conn.close()


# store the temperature in the database
def insert_data(values=()):
        conn=sqlite3.connect(dbname)
        cur=conn.cursor()
        query = 'INSERT INTO LOG (usuario, comando, local, ssid, data) VALUES (%s)' % (
                        ', '.join(['?'] * len(values))                                        
        )                
        cur.execute(query, values)
        conn.commit()
        id = cur.lastrowid
        cur.close()
        conn.close()
        return id     

# display the contents of the database
def display_data():
        conn=sqlite3.connect(dbname)
        curs=conn.cursor()
        curs.execute("SELECT * FROM LOG ORDER BY data DESC")
        rows=curs.fetchall() 
        return rows  

def delete_data():
        conn=sqlite3.connect(dbname)
        curs=conn.cursor()
        curs.execute("DELETE FROM LOG;")
        curs.close()
        conn.commit()
        conn.close()
        return True  

def getTotalCounter():
        return session['counter']

def sumSessionCounter():
  try:
    session['counter'] += 1
  except KeyError:
    session['counter'] = 0

if __name__ == "__main__":
        app.run(host='0.0.0.0', port=8080,debug = True)
