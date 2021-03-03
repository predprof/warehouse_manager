import uuid

from sqlalchemy import MetaData, create_engine, Integer, Column, String, ForeignKey, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

metadata = MetaData()
engine = create_engine('postgresql://admin:12345@localhost:5432/storage_manager_olymp', echo=True)
Base = declarative_base()
db_session = sessionmaker(bind=engine)()


class Stowage(Base):
    __tablename__ = 'stowages'
    id = Column(Integer, primary_key=True, unique=True)
    row = Column(String, nullable=False)
    level = Column(Integer, nullable=False)
    size_x = Column(Integer, nullable=False)
    size_y = Column(Integer, nullable=False)
    size_z = Column(Integer, nullable=False)
    volume = Column(Integer, nullable=False)
    json = Column(String, nullable=False)
    empty = Column(Boolean, nullable=False)


class Item(Base):
    __tablename__ = 'items'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True)
    name = Column(String, nullable=False)
    size_x = Column(Integer, nullable=False)
    size_y = Column(Integer, nullable=False)
    size_z = Column(Integer, nullable=False)
    weight = Column(Integer, nullable=False)
    stowage_id = Column(ForeignKey('stowages.id'))


# ѕолучить список товаров
def get_items():
    return db_session.query(Item)


def add_items(new_item):
    db_session.add(new_item)
    db_session.commit()


# ѕолучить список ¤чеек
def get_stowages():
    return db_session.query(Stowage)


# —охранить новую ¤чейку
def add_stowage(new_stowage):
    db_session.add(new_stowage)
    db_session.commit()


# –азмещаем товар на складе
def put_item_in_stowage(item, stowage):
    db_session.query(Stowage).\
        filter(Stowage.id == stowage.id).\
        update({"empty": False})
    db_session.query(Item).\
        filter(Item.id == item.id).\
        update({"stowage_id": stowage.id})
    db_session.commit()


# ќчистка таблицы ¤чеек
def clean_stowages():
    # db_session.delete(Stowage)
    db_session.query(Stowage).delete()
    db_session.commit()


def clean_items():
    db_session.query(Item).delete()
    db_session.commit()