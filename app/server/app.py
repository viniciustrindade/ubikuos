#!/env/bin/env python
# -*- coding: utf-8 -*-
import sqlite3
from flask import Flask,json, render_template, request


app = Flask(__name__)

#Arquivo de banco de dados do SQLite
dbname='sensores.sqlite'

@app.route('/')
@app.route('/index')
def index():
        return render_template('index.html')

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


###################### Rotas #######################################
@app.route('/command/turn-light')
def getTipos():
        return json.dumps(sensor_type_list)


@app.route('/login')
def listAll():
        sensor_list = db_get_sensores()

        return json.dumps(sensor_list)
    

@app.route('/list-services')
def listAll():
        list = db_get_sensores()

        return json.dumps(list)    

# store the temperature in the database
def db_insert_sensor(values=()):
                conn=sqlite3.connect(dbname)
                cur=conn.cursor()
                query = 'INSERT INTO sensor (tipo_sensor) VALUES (%s)' % (
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

# display all contents of the table SENSOR
def db_get_sensores():
        conn=sqlite3.connect(dbname)
        curs=conn.cursor()
        curs.execute("SELECT id FROM SENSOR")
        rows=curs.fetchall() 
        ar=[r[0] for r in rows]
        return ar  

# display all contents of the table SENSOR
def db_get_sensor_type(sensor_id):

        conn=sqlite3.connect(dbname)
        curs=conn.cursor()
        curs.execute("SELECT tipo_sensor FROM SENSOR WHERE id = (?) ",(sensor_id,))
        rows=curs.fetchall() 

        ar=[r[0] for r in rows]
        if (len(ar) > 0):
                return  ar[0]
        else:
                return None

# display all contents of the table SENSOR
def db_delete_sensor(sensor_id):

        conn=sqlite3.connect(dbname)
        curs=conn.cursor()
        curs.execute("DELETE FROM SENSOR WHERE id = (?) ",(sensor_id,))
        curs.execute("DELETE FROM LOG WHERE id_sensor = (?) ",(sensor_id,))
        conn.commit()
        curs.close()
        conn.close()
        return True


def delete_data():
        conn=sqlite3.connect(dbname)
        curs=conn.cursor()
        curs.execute("DELETE FROM LOG;")
        curs.close()
        conn.commit()
        conn.close()
        return True  

# display the contents of the database
def createDatabase():
        # conectando...
        conn = sqlite3.connect(dbname)
        # definindo um cursor
        cursor = conn.cursor()

        # criando a tabela (schema)
        cursor.execute("""
        CREATE TABLE LOG (
                                        id         INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                                        id_sensor      VARCHAR(20),
                                        valor        DECIMAL(10,3),
                                        unidade        VARCHAR(20),
                                        variavel     VARCHAR(20),
                                        data       TIMESTAMP
        );
        """)
        # desconectando...
        conn.close()

# display the contents of the database
def createSensor():
        # conectando...
        conn = sqlite3.connect(dbname)
        # definindo um cursor
        cursor = conn.cursor()

        # criando a tabela (schema)
        cursor.execute("""
        CREATE TABLE SENSOR (
                                        id      INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                                        tipo_sensor VARCHAR(20)
        );
        """)  
        # desconectando...
        conn.close()

if __name__ == "__main__":
        app.run(host='0.0.0.0', port=8080,debug = True)