import sqlite3, os

class Db:
    def __init__(self):
        # 当前路径
        cur_path = os.path.abspath(os.path.dirname(__file__))
        # 数据库地址
        db_path = os.path.join(cur_path, 'ip.db3')
        self.conn = sqlite3.connect(db_path, check_same_thread = False)
        self.cursor = self.conn.cursor()
    def query(self, query, args=(), one=False):
        cur = self.cursor.execute(query, args)
        rv = [dict((cur.description[idx][0], value)
                    for idx, value in enumerate(row)) for row in cur.fetchall()]
        return (rv[0] if rv else None) if one else rv
    def commit(self):
        self.conn.commit()
