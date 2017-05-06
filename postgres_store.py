# Postgresql data storing module
#
import json
import psycopg2


_db = None


def get_default():
    global _db
    if not _db:
        # _db postgres_store('postgres', 'postgres', 'mysecretpassword', '172.17.0.3', 5432)
        _db = postgres_store('fred', 'fred', '763160', 'localhost', 5432)
        # _db postgres_store('dc7m5co1u7n7ka', 'vfumyroepkgfsd', 'AsRCUy1JTkf500s_2pfXZK9qwR', 'ec2-107-22-246-250.compute-1.amazonaws.com', 5432)
    return _db


class postgres_store(object):

    def __init__(self, db, user, psw, host, port):
        self._db = db
        self._user = user
        self._psw = psw
        self._host = host
        self._port = port
        self._con = None

    def connect(self):
        if self._con:
            return self._con
        try:
            self._con = psycopg2.connect(database=self._db,
                                         user=self._user,
                                         password=self._psw,
                                         host=self._host,
                                         port=self._port)

        except psycopg2.DatabaseError, e:
            print('Error %s' % e)
        return self._con

    def disconnect(self):
        if self._con:
            self._con.close()
            self._con = None

    def table_exist(self, table):
        if self._con:
            try:
                cur = self._con.cursor()
                cur.execute("SELECT * FROM information_schema.tables WHERE table_name='" + table + "';")
            except Exception as e:
                print(e)
                return False

            return bool(cur.rowcount)
        return False

    def row_exist(self, table, id):
        if self._con:
            try:
                cur = self._con.cursor()
                cur.execute("SELECT * FROM " + table + " WHERE ID='" + str(id) + "';")
            except Exception as e:
                print(e)
                return False

            return bool(cur.rowcount)
        return False

    def create_table(self, table):
        if self._con:
            try:
                cur = self._con.cursor()
                cur.execute('CREATE TABLE ' + table + '(ID INT PRIMARY KEY NOT NULL, data TEXT NOT NULL)')
                self._con.commit()
            except Exception as e:
                print(e)
                return False

            return True
        return False

    def create_row(self, table, id, data):
        if self._con:
            try:
                cur = self._con.cursor()
                cur.execute("INSERT INTO " + table + "(ID,data) " + "VALUES(" + str(id) + ", '" + json.dumps(data) + "')")
                self._con.commit()
            except Exception as e:
                print('row', e)
                return False

            return True
        return False

    def get_rows_id(self, table):
        if self._con:
            try:
                cur = self._con.cursor()
                cur.execute("SELECT ID FROM " + table)
                records = cur.fetchall()
                data = []
                for r in records:
                    data.append(r[0])
            except Exception as e:
                print(e)
                return []

            return data
        return []

    def store(self, table, id, data):
        if not self.table_exist(table):
            self.create_table(table)
        if not self.row_exist(table, id):
            self.create_row(table, id, data)

        if self._con:
            try:
                cur = self._con.cursor()
                cur.execute('UPDATE ' + table + ' SET data=\'' + json.dumps(data) + '\' WHERE ID=' + str(id))
                self._con.commit()
            except:
                return False

            return True
        return False

    def restore(self, table, id):
        if not self.table_exist(table) or not self.row_exist(table, id):
            return ''

        if self._con:
            try:
                cur = self._con.cursor()
                cur.execute('SELECT data FROM ' + table + ' WHERE ID=' + str(id))
                records = cur.fetchall()
                data = json.loads(records[0][0])
            except:
                return None

            return data
        return None

    def backup(self):
        req_tables = "SELECT table_name FROM information_schema.tables WHERE table_type = 'BASE TABLE' AND table_schema = 'public' ORDER BY table_schema,table_name;"
        data = {}
        if self._con:
            try:
                cur = self._con.cursor()
                cur.execute(req_tables)
                records = cur.fetchall()
                for record in records:
                    table = record[0]
                    data[table] = {}
                    data_req = 'SELECT * FROM {table};'.format(table=table)
                    cur.execute(data_req)
                    rows = cur.fetchall()
                    for row in rows:
                        data[table][row[0]] = json.loads(row[1])
            except:
                pass
        return data

    def restore_backup(self, data):
        req_tables = "SELECT table_name FROM information_schema.tables WHERE table_type = 'BASE TABLE' AND table_schema = 'public' ORDER BY table_schema,table_name;"
        if self._con:
            try:
                cur = self._con.cursor()
                cur.execute(req_tables)
                records = cur.fetchall()
                for record in records:
                    table = record[0]
                    drop_req = 'DROP TABLE {table};'.format(table=table)
                    cur.execute(drop_req)
                self._con.commit()

                for table in list(data.items()):
                    table_name = table[0]
                    for row in list(table[1].items()):
                        id = row[0]
                        self.store(table_name, id, row[1])
            except Exception as e:
                print('restore_backup', e)
                return False
        return True
