import json

from sqlalchemy import MetaData, create_engine, Integer, Column, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import sessionmaker

metadata = MetaData()
engine = create_engine('postgresql://admin:12345@localhost:5432/storage_manager_olymp', echo=True)
Base = declarative_base()
db_session = sessionmaker(bind=engine)()


class Stowage(Base):
    __tablename__ = 'stowages'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    size_x = Column(Integer, nullable=False)
    size_y = Column(Integer, nullable=False)
    size_z = Column(Integer, nullable=False)
    json = Column('json', String, nullable=False)

    #@hybrid_property
    #def json(self):
    #    return json.loads(self._json)

    #@json.setter
    #def json(self, json_to_save):
    #    self._json = json.dumps(json_to_save)


class Item(Base):
    __tablename__ = 'items'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    size_x = Column(Integer)
    size_y = Column(Integer)
    size_z = Column(Integer)
    weight = Column(Integer)
    status = Column(String)
    stowage_id = Column(ForeignKey('stowages.id'))


# ѕолучить список товаров
def get_items():
    return db_session.query(Item)


def add_items(new_item):
    db_session.add(new_item)
    db_session.commit()


# ѕолучить список €чеек
def get_stowages():
    return db_session.query(Stowage)


# —охранить €чейку
def add_stowage(new_stowage):
    db_session.add(new_stowage)
    db_session.commit()


# ќчистка таблицы €чеек
def clean_stowages():
    # db_session.delete(Stowage)
    db_session.query(Stowage).delete()
    db_session.commit()
