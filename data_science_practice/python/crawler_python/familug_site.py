import requests
import sqlite3
import bs4
from flask import Flask, render_template


def get_data(link_site, label, conn):
    resp = requests.get(link_site)
    soup = bs4.BeautifulSoup(resp.text, 'lxml')
    title_name = soup.findAll('h3', {'class': 'post-title'})
    for h3 in title_name:
        link = h3.find('a')['href']
        name = h3.find('a').contents[0]
        infor = (link, name)
        query = "INSERT INTO {} VALUES(?,?)".format(label)
        conn.execute(query, infor)
    next_page_link = soup.find('a', {
            'id': "Blog1_blog-pager-older-link"})['href']
    return next_page_link


def get_data_label(label):
    conn = sqlite3.connect('familug_db.db')
    c = conn.cursor()
    if label == 'main_site':
        query = '''CREATE TABLE {}(name, link)'''.format(label)
        c.execute(query)
        get_data('http://www.familug.org/search?max-results=10',
                 label, c)
    else:
        link_site = 'http://www.familug.org/search/label/{}'.format(label)
        query = '''CREATE TABLE {}(name, link)'''.format(label)
        c.execute(query)
        while True:
            try:
                link_site = get_data(link_site, label, c)
            except Exception:
                break
    conn.commit()
    conn.close


def update_data_base():
    for label in ['main_site', 'Python', 'Command', 'sysadmin']:
        get_data_label(label)


def create_html():
    list_name = ['main_site', 'Python', 'Command', 'sysadmin']
    conn = sqlite3.connect('familug_db.db')
    c = conn.cursor()
    for name in list_name:
        with open('templates/{}.html'.format(name), 'a') as site:
            for element in list_name:
                if element == name:
                    site.write('<li><a class="chosen" '
                               'href="/{}">{}</a></li>'.format(name, name))
                else:
                    site.write('<li><a href="/{}">'
                               '{}</a></li>'.format(element, element))
            site.write('</ul>')
            query = 'SELECT * FROM {}'.format(name)
            data = c.execute(query)
            for infor in data:
                site.write('<p><a href="{}">{}</a></p></br>'
                           .format(infor[0], infor[1]))
            site.write('</body></html>')
    conn.close()


def launch_site():
    app = Flask(__name__)

    @app.route('/')
    def index():
        return render_template('main_site.html')

    @app.route('/main_site')
    def main_site():
        return render_template('main_site.html')

    @app.route('/Python')
    def Python():
        return render_template('Python.html')

    @app.route('/Command')
    def Command():
        return render_template('Command.html')

    @app.route('/sysadmin')
    def sysadmin():
        return render_template('sysadmin.html')

    app.run(debug=True)


if __name__ == "__main__":
    launch_site()
