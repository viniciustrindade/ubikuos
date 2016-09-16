#!/env/bin/env python
# -*- coding: utf-8 -*-
import sqlite3, serial, time
from flask import Flask,json, render_template, request


app = Flask(__name__)

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
        #sensor_list = db_get_sensores()
        #return json.dumps(sensor_list)
        return "Login route route!"
    

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
        Obs: Não executar caso o banco já esteja criado, pois será retornada uma msg de erro.
        """
        try:
                createLog()
                createSensor()
                return 'Tabelas criadas com sucesso.'
        except Exception, e:
                return 'Failed to create Database and tables: '+ str(e)


# display the contents of the database
def createDatabase():
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
                query = 'INSERT INTO LOG (usuario, comando, local, ssid, data) VALUES (%s, %s, %s, %s, %s)' % (
                                ', '.join(['?'] * len(values))
                )
                cur.execute(query, values)
                conn.commit()
                id = cur.lastrowid
                cur.close()
                conn.close()
                return id     

# display the contents of the database
def display_data(sensor_id):
        conn=sqlite3.connect(dbname)
        curs=conn.cursor()
        curs.execute("SELECT * FROM (SELECT time(data) AS data, valor, unidade FROM LOG WHERE id_sensor = (?) ORDER BY data DESC LIMIT 20) ORDER BY data ASC",(sensor_id,))
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