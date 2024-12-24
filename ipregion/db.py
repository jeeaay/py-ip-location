import sqlite3, os, shutil
# 这里需要添加一个 如果没有缓存数据库，将空数据库重命名为
class Db:
    def __init__(self, db_path = None):
        # 当前路径
        cur_path = os.path.abspath(os.path.dirname(__file__))
        # 数据库路径
        if db_path == None:
            db_path = os.path.join(cur_path, "ipcache.db3")
        # 示例数据库路径
        example_db_path = os.path.join(cur_path, "ipcache.sample.db3")
        # 如果没有缓存数据库，将示例数据复制到数据库路径
        if not os.path.exists(db_path):
            # 复制
            shutil.copyfile(example_db_path, db_path)
        self.conn = sqlite3.connect(db_path, check_same_thread = False)
        self.cursor = self.conn.cursor()
    def query(self, query, args=(), one=False):
        cur = self.cursor.execute(query, args)
        rv = [dict((cur.description[idx][0], value)
                    for idx, value in enumerate(row)) for row in cur.fetchall()]
        return (rv[0] if rv else None) if one else rv
    def commit(self):
        self.conn.commit()
