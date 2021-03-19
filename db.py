import os
import uuid

from sqlalchemy import MetaData, create_engine, Integer, Column, String, ForeignKey, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

metadata = MetaData()
# Для запуска через heroku
if os.getenv("DATABASE_URL") is None:
    db_path = "postgresql://admin:admin@localhost:5432/storage_manager_olymp"
else:
    db_path = os.getenv("DATABASE_URL")
print("Соединяемся с БД по адресу", db_path)
engine = create_engine(db_path, echo=True)

Base = declarative_base()
db_session = sessionmaker(bind=engine)()


# Создаем сущность Ячейка для связи с БД
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


# Создаем сущность Товар для связи с БД
class Item(Base):
    __tablename__ = 'items'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True)
    name = Column(String, nullable=False)
    size_x = Column(Integer, nullable=False)
    size_y = Column(Integer, nullable=False)
    size_z = Column(Integer, nullable=False)
    weight = Column(Integer, nullable=False)
    stowage_id = Column(ForeignKey('stowages.id'))


# Получить товар по ID
def get_item(item_id):
    return db_session.query(Item). \
        filter(Item.id == item_id)


# Получить ячейку по ID
def get_stowage(stowage_id):
    return db_session.query(Stowage). \
        filter(Stowage.id == stowage_id)


# Получить список товаров
def get_all_items():
    return db_session.query(Item)


# Добавление нового товара
def add_item(new_item):
    db_session.add(new_item)
    db_session.commit()


# ѕолучить список ¤чеек
def get_all_stowages():
    return db_session.query(Stowage)


# Сохранить новую ¤чейку
def add_stowage(new_stowage):
    db_session.add(new_stowage)
    db_session.commit()


# Размещаем товар на складе. Операция должна быть атомарной (неразделимой), поэтому логика помещена сюда
def load_item_in_stowage(item, stowage):
    db_session.query(Stowage). \
        filter(Stowage.id == stowage.id). \
        update({"empty": False})
    db_session.query(Item). \
        filter(Item.id == item.id). \
        update({"stowage_id": stowage.id})
    db_session.commit()


# Выгрузка товара со склалда. Операция должна быть атомарной (неразделимой), поэтому логика помещена сюда
def unload_item_from_stowage(item_id):
    it = db_session.query(Item). \
        filter(Item.id == item_id)
    if it[0].stowage_id is not None:
        db_session.query(Stowage). \
            filter(Stowage.id == it[0].stowage_id). \
            update({"empty": True})
        db_session.query(Item). \
            filter(Item.id == item_id). \
            delete()
        db_session.commit()


# Очистка таблицы ¤чеек
def clean_stowages():
    db_session.query(Stowage).delete()
    db_session.commit()


# Очистка таблицы товаров
def clean_items():
    db_session.query(Item).delete()
    db_session.commit()
