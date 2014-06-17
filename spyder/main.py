import Queue
from spyder import Spyder
from parser import parse
from db import DB

re_q = Queue.Queue()
spyder = Spyder(re_q)
db = DB()
id_ = 0

def main():
    get_data()
    process_responce()

def get_data():
    spyder.run()

def process_responce():
    global id_
    while not spyder.is_over():
        if not re_q.empty():
            re = re_q.get()
            item = parse(re)
            if item:
                item = tuple([id_] + list(item))
                print "add one song, artist: {}".format(item[1].encode('utf-8'))
                add_to_database(item)
                id_ += 1
    db.post()

def add_to_database(item):
    db.insert(item)

if __name__ == "__main__":
    main()
