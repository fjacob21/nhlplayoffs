# Postgresql data storing module
#
import json
import psycopg2

class postgres_store(object, db, user, psw, host, port):

    def __init__(self, features):
        self._db = db
        self._user = user
        self._psw = psw
        self._host = host
        self._port = port

    def connect():
        con = None
        try:
            con = psycopg2.connect(database=self._db,
                                   user=self._user,
                                   password=self._psw,
                                   host=self._host,
                                   port=self._port)

        except psycopg2.DatabaseError, e:
            print('Error %s' % e)

        return con

    def store(table, id, data):
        con = connect()
        if con :
            try:
                cur = con.cursor()
                cur.execute('UPDATE ' + table + ' SET data=\''+ data +'\' WHERE ID=' + str(id))
                con.commit()
            except Exception as e:
                return False

            con.close()
            return True
        return False

    def restore(table, id):
        con = connect()
        if con :
            try:
                cur = con.cursor()
                cur.execute('SELECT data FROM ' + table + ' WHERE ID=' + str(id))
                records = cur.fetchall()
                data = json.loads(records[0][0])
            except Exception as e:
                return None

            con.close()
            return data
        return None
