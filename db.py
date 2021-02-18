from sqlalchemy import MetaData, create_engine, Integer, Column, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

metadata = MetaData()
engine = create_engine('postgresql://admin:12345@localhost:5432/storage_manager_olymp', echo=True)
Base = declarative_base()
db_session = sessionmaker(bind=engine)()


class Stowage(Base):
    __tablename__ = 'stowages'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    size_x = Column(Integer)
    size_y = Column(Integer)
    size_z = Column(Integer)
    item_id = Column(ForeignKey('items.id'))


class Item(Base):
    __tablename__ = 'items'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    size_x = Column(Integer)
    size_y = Column(Integer)
    size_z = Column(Integer)
    weight = Column(Integer)
    status = Column(String)


# ѕолучить список товаров
def get_items():
    return db_session.query(Item)


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
