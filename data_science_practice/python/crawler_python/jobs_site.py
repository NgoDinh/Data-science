import requests
import sqlite3
from flask import Flask, render_template


def get_data(page_number, conn):
    link = ('https://api.github.com/repos/awesome-jobs/vietnam/issues?'
            'page={}').format(page_number)
    resp = requests.get(link).json()
    for line in resp:
        infor = (line['title'], line['html_url'])
        conn.execute("INSERT INTO jobs VALUES(?,?)", infor)


def updata_data():
    conn = sqlite3.connect('jobs_db.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE jobs(name, link)''')
    page_number = 1
    while True:
        try:
            get_data(page_number, c)
            page_number = page_number + 1
        except Exception:
            break
    conn.commit()
    conn.close()


def create_html(db_name):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    with open('templates/index.html', 'w') as html_file:
        html_file.write('<!doctype html>'
                        '<html><title>Jobs page for dev</title>'
                        '<body>')
        for element in c.execute('SELECT * FROM jobs'):
            html_file.write('<p><a href="{}">{}</a></p></br>'
                            .format(element[1], element[0]))
        html_file.write('</body></html>')
    conn.close()


create_html('jobs_db.db')
app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
