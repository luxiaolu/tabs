from bs4 import BeautifulSoup as bs

def encode_(text):
    text = unicode(text)
    return text

def parse(html):
    soup = bs(html)
    try:
        body = soup.html.body.find(class_='mainBody')

        song_name = body.h1.text[:-3]
        artist = body.a.strong.string

        tab = body.find(id='body').pre.prettify()
    except AttributeError:
        return
    return encode_(artist),encode_(song_name),encode_(tab)

if __name__ == "__main__":
    with open("101.html", 'r') as f:
        print parse(f.read())
        
