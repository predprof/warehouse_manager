from sqlalchemy import MetaData, create_engine, Integer, Column, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

metadata = MetaData()
# engine = create_engine('postgresql://admin:1234@localhost:5432/storage_warehouse_olymp', connect_args={'check_same_thread': False}, echo=False)
engine = create_engine('postgresql://admin:12345@localhost:5432/storage_manager_olymp', echo=True)
Base = declarative_base()
db_session = sessionmaker(bind=engine)()


class Stowage(Base):
    __tablename__ = 'stowages'
    id = Column(Integer, primary_key=True)
    pos_x = Column(Integer)
    pos_y = Column(Integer)
    size_x = Column(Integer)
    size_y = Column(Integer)
    size_z = Column(Integer)
    volume = Column(Integer)
    weight = Column(Integer)
    status = Column(String)


class Item(Base):
    __tablename__ = 'items'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    size_x = Column(Integer)
    size_y = Column(Integer)
    size_z = Column(Integer)
    volume = Column(Integer)
    weight = Column(Integer)
    status = Column(String)
    stowage_id = Column(ForeignKey('stowages.id'))


def get_items():
    return db_session.query(Item)
