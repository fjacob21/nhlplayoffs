# Postgresql data storing module
#
import json
import psycopg2

class postgres_store(object):

    def __init__(self, db, user, psw, host, port):
        self._db = db
        self._user = user
        self._psw = psw
        self._host = host
        self._port = port

    def connect(self):
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

    def table_exist(self, table):
        con = self.connect()
        if con :
            try:
                cur = con.cursor()
                cur.execute("SELECT * FROM information_schema.tables WHERE table_name='" + table + "';")
            except Exception as e:
                print(e)
                return False

            con.close()
            return bool(cur.rowcount)
        return False

    def row_exist(self, table, id):
        con = self.connect()
        if con :
            try:
                cur = con.cursor()
                cur.execute("SELECT * FROM " + table + " WHERE ID='" + str(id) + "';")
            except Exception as e:
                print(e)
                return False

            con.close()
            return bool(cur.rowcount)
        return False

    def create_table(self, table):
        con = self.connect()
        if con :
            try:
                cur = con.cursor()
                cur.execute('CREATE TABLE ' + table + '(ID INT PRIMARY KEY NOT NULL, data TEXT NOT NULL)')
                con.commit()
            except Exception as e:
                print(e)
                return False

            con.close()
            return True
        return False

    def create_row(self, table, id, data):
        con = self.connect()
        if con :
            try:
                cur = con.cursor()
                cur.execute("INSERT INTO " + table + "(ID,data) " + "VALUES("+ str(id) + ", '"+ json.dumps(data) + "')" )
                con.commit()
            except Exception as e:
                print('row',e)
                return False

            con.close()
            return True
        return False

    def delete_table(self, table):
        con = self.connect()
        if con :
            try:
                cur = con.cursor()
                cur.execute('DROP TABLE ' + table)
                con.commit()
            except Exception as e:
                return False

            con.close()
            return True
        return False

    def store(self, table, id, data):
        if not self.table_exist(table):
            self.create_table(table)
        if not self.row_exist(table, id):
            self.create_row(table, id, data)

        con = self.connect()
        if con :
            try:
                cur = con.cursor()
                cur.execute('UPDATE ' + table + ' SET data=\''+ json.dumps(data) +'\' WHERE ID=' + str(id))
                con.commit()
            except Exception as e:
                return False

            con.close()
            return True
        return False

    def restore(self, table, id):
        if not self.table_exist(table) or not self.row_exist(table, id):
            return ''

        con = self.connect()
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