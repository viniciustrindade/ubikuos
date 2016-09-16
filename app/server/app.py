#!/env/bin/env python
# -*- coding: utf-8 -*-
import sqlite3, serial, time, datetime
from flask import Flask,json, render_template, request

app = Flask(__name__)

#definindo usuário para a aplicação (posteriormente implementar esquema com dados em tabela e etc..)
user = ["admin", "123456"]

#Arquivo de banco de dados do SQLite
dbname='sensores.sqlite'

@app.route('/')
@app.route('/index')
def index():
        #return render_template('index.html')
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
    try:
        ser = serial.Serial('/dev/ttyACM1', 9600)
        while True:
            ser.write('acende')
            time.sleep(3)
            ser.write('apaga')
            time.sleep(3)
            ser.write('pisca')
            time.sleep(4)
            ser.write('pisca')
            time.sleep(4)
    except Exception as e:
        return "Opa! parece que o Arduino não está ligado!"


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


if __name__ == "__main__":
        app.run(host='0.0.0.0', port=8080,debug = True)