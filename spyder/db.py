#coding:utf-8
from sqlalchemy import Column, String, create_engine, Text, Integer
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# create base class
Base = declarative_base()

# crate tab class
class Tab(Base):
    __tablename__ = 'tabs'

    id = Column(Integer, primary_key=True)
    artist = Column(Text)
    song = Column(Text)
    tab = Column(Text)

class DB(object):

    def __init__(self):
        # connect database
        engine = create_engine('mysql+mysqlconnector://root:123@localhost:3306/tab')
        # create session
        self.DBSession = sessionmaker(bind=engine)
        # create session object
        self.session = self.DBSession()

    def insert(self, item):
        """
        insert one item to db
        """
        id_, artist, song, tab = item
        new_db_item = Tab(id=id_, artist=artist, song=song, tab=tab)
        self.session.add(new_db_item)

    def post(self):
        self.session.commit()
        self.session.close()

    def test(self):
        session = self.DBSession()
        tabs = session.query(Tab).filter(Tab.artist=='老狼').all()
        for tab in tabs:
            print tab.song
        session.close()


if __name__ == "__main__":
    db =DB()
    db.test()
