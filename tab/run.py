from flask import Flask
from flask import render_template
from flask import request
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
sql_path = 'mysql://root:123@localhost:3306/tab'
app.config['SQLALCHEMY_DATABASE_URI'] = sql_path
db = SQLAlchemy(app)

class Tab(db.Model):
    __tablename__ = 'tabs'
    id = db.Column(db.Integer, primary_key=True)
    artist = db.Column(db.Text)
    song = db.Column(db.Text)
    tab = db.Column(db.Text)

#@app.route('/')
#def test_tab():
#    t = Tab.query.filter_by(id='1').first()
#    return t.tab

@app.route('/')
def main():
    return render_template('search.html')

@app.route('/search')
def search():
    kwd = request.args.get('kwd')
    song_matchs = Tab.query.filter_by(song=kwd).all()
    artist_matchs = Tab.query.filter_by(artist=kwd).all()
    matchs = song_matchs + artist_matchs
    items = [(item.id, item.song) for item in matchs]
    return render_template('list.html', items=items)

@app.route('/id/<id_>')
def tab(id_=1):
    item = Tab.query.filter_by(id=id_).first()
    artist = item.artist
    song = item.song
    tab = item.tab

    return render_template('song.html', artist=artist, song=song, tab=tab)

if __name__ == "__main__":
    app.run(debug=True)
