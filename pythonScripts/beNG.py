import sqlite3


class Line:
    def __init__(self, self_id, id_script, text, title, img1, img2, follow1, follow1_id, follow2, follow2_id, follow3,
                 follow3_id, follow4, follow4_id):
        self.id = self_id
        self.script_id = id_script
        self.text = text
        self.title = title
        self.images = (img1, img2)
        self.follows = [(follow1, follow1_id),
                        (follow2, follow2_id),
                        (follow3, follow3_id),
                        (follow4, follow4_id)]
        while ("", 0) in self.follows:
            self.follows.remove(("", 0))
        while ("", "") in self.follows:
            self.follows.remove(("", ""))
        if len(self.follows) < 1:
            self.follows = [("", self.id + 1)]

    def get_id(self):
        return self.id

    def get_text(self):
        return self.text

    def get_script(self):
        return self.script_id

    def get_title(self):
        return self.title

    def get_images(self):
        return self.images[0], self.images[1]

    def get_all_follows(self):
        return self.follows

    def get_follow_text(self, n=0):
        return self.follows[n][0]

    def get_follow_id(self, n=0):
        return self.follows[n][1]

    def __repr__(self):
        return "line nbr" + str(self.id)


class Script:
    def __init__(self, self_id):
        self.id = self_id
        self.name = get_script(self.id)[1]
        self.lines = convert_all_lines(self.id)
        if len(self.lines) > 0:
            self.current = self.lines[0]
        else:
            self.current = None

    def get_id(self):
        return self.id

    def get_current(self):
        return self.current

    def follow_up(self, n, line=None):
        if line == None:
            line = self.current
        elif type(line) == int:
            line = self.lines[line]
        self.current = self.get_line_by_id(line.get_follow_id(n))
        return True

    def get_line_by_id(self, id_line):
        for i in self.lines:
            if i.get_id() == id_line:
                return i

    def get_all_lines(self):
        return self.lines

    def __repr__(self):
        return "'" + self.name + "' (script nbr" + str(self.id) + ")"


def initcur():  # utilisé pour initier le curseur (cur) et la connection (conn)
    # la variable conn et cur sont globales
    global conn
    global cur
    try:
        conn = sqlite3.connect('DIALOGUEdb.db')
        cur = conn.cursor()
    except:
        print("an error occured during cursor's initialization")
        return False
    else:
        return True


def closecur():  # ferme le curseur et la connection
    try:
        conn.commit()
        ans = cur.fetchall()
    except:
        ans = True
    cur.close()
    conn.close()
    return ans


def init_dialogues():
    initcur()
    cur.execute(
        "CREATE TABLE IF NOT EXISTS LINES(id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE, id_script INTEGER, text TEXT, title TEXT, img1 TEXT, img2 TEXT, "
        "follow1 TEXT, follow1_id INTEGER, follow2 TEXT, follow2_id INTEGER, follow3 TEXT, follow3_id INTEGER, follow4 TEXT, follow4_id INTEGER)")
    cur.execute("CREATE TABLE IF NOT EXISTS SCRIPTS(id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE, name TEXT)")
    closecur()


def create_script(name):
    initcur()
    cur.execute("INSERT INTO SCRIPTS(name) VALUES(?)", (name,))
    cur.execute("SELECT * FROM SCRIPTS")
    return closecur()[-1][0]


def add_line(id_script, text, title, images, follows):
    initcur()
    img1, img2 = images[0], images[1]
    follow1, follow1_id = follows[0][0], follows[0][1]
    follow2, follow2_id = follows[1][0], follows[1][1]
    follow3, follow3_id = follows[2][0], follows[2][1]
    follow4, follow4_id = follows[3][0], follows[3][1]
    cur.execute(
        "INSERT INTO LINES(id_script, text, title, img1, img2, follow1, follow1_id, follow2, follow2_id, follow3, follow3_id, follow4, follow4_id) "
        "VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
        (id_script, text, title, img1, img2,
         follow1, follow1_id, follow2, follow2_id, follow3, follow3_id, follow4, follow4_id))
    closecur()


def delete_line(id_line):
    initcur()
    cur.execute('DELETE FROM Lines WHERE id = ?', (id_line,))
    return closecur[0]


def get_script(id_script):
    initcur()
    cur.execute("SELECT * FROM SCRIPTS WHERE id = ?", (id_script,))
    return closecur()[0]


def get_all_scripts():
    initcur()
    cur.execute("SELECT * FROM SCRIPTS")
    return closecur()


def get_script_by_name(name):
    initcur()
    cur.execute("SELECT * FROM SCRIPTS WHERE name = ?", (name,))
    ans = closecur()
    if len(ans) > 0:
        return ans[0]
    else:
        raise RuntimeError('Script ' + name + ' was not found')


def get_line(id_line):
    initcur()
    cur.execute("SELECT * FROM LINES WHERE id = ?", (id_line,))
    return closecur()[0]


def get_all_lines(id_script):
    initcur()
    if id_script == 0:
        cur.execute("SELECT * FROM LINES")
    else:
        cur.execute("SELECT * FROM LINES WHERE id_script = ?", (id_script,))
    return closecur()


def convert_script(id_script):
    return Script(id_script)


def convert_all_scripts():
    initcur()
    cur.execute("SELECT id FROM SCRIPTS")
    ids = closecur()
    ans = []
    for i in ids:
        ans.append(Script(i[0]))
    return ans


def convert_line(id_line):
    line = get_line(id_line)
    return Line(line[0], line[1], line[2], line[3], line[4], line[5], line[6], line[7], line[8], line[9], line[10],
                line[11], line[12], line[13])


def convert_all_lines(id_script):
    lines = get_all_lines(id_script)
    ans = []
    for line in lines:
        ans.append(convert_line(line[0]))
    return ans


def read_line(id_line):
    line = get_line(id_line)
    return "[" + str(line[0]) + "] " + line[3] + ": " + line[2]

# init_dialogues()
# create_script("da first (fr this time)")
# add_line(1, "im the first", "panids", ("panids.idle", "fet.idle"), (("lol no i am", 2), ("damb ok man", 3), ("", 0), ("", 0)))
# add_line(1, "fuk u", "panids", ("panids.idle", "fet.idle"), (("wha-", 1), ("", 0), ("", 0), ("", 0)))
# add_line(1, "ahaha now u nuderstad how stronk ia m", "panids", ("panids.idle", "fet.idle"), (("no", 2), ("yesn't", 2), ("", 0), ("", 0)))
