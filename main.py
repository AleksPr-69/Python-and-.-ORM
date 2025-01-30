import json
import sqlalchemy
from engine import engine, Session
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime



Base = declarative_base()

class Publisher(Base):
    __tablename__ = 'publisher'

    id = Column(Integer, primary_key=True)
    name = Column(String(length=60), unique=True, nullable=False)

    def __str__(self):
        return f'У автора {self.name} id={self.id}'


class Book(Base):
    __tablename__ = 'book'

    id = Column(Integer, primary_key=True)
    title = Column(String(length=60), unique=True, nullable=False)
    id_publisher = Column(Integer, ForeignKey('publisher.id'), nullable=False)

    publisher = relationship(Publisher, backref='book')


class Shop(Base):
    __tablename__ = 'shop'

    id = Column(Integer, primary_key=True)
    name = Column(String(length=60), unique=True, nullable=False)

    def __str__(self):
        return self.name


class Stock(Base):
    __tablename__ = 'stock'

    id = Column(Integer, primary_key=True)
    id_book = Column(Integer, ForeignKey('book.id'), nullable=False)
    id_shop = Column(Integer, ForeignKey('shop.id'), nullable=False)
    count = Column(Integer, nullable=False)

    book = relationship(Book, backref='stock')
    shop = relationship(Shop, backref='Stock')


class Sale(Base):
    __tablename__ = 'sale'

    id = Column(Integer, primary_key=True)
    price = Column(Float, nullable=False)
    date_sale = Column(DateTime, nullable=False)
    id_stock = Column(Integer, ForeignKey('stock.id'), nullable=False)
    count = Column(Integer, nullable=False)

    stock = relationship(Stock, backref='sale')


def init_tests_data(session=Session()):
    with open('tests_data.json', 'r') as fd:
        data = json.load(fd)

    for record in data:
        model = {
            'publisher': Publisher,
            'shop': Shop,
            'book': Book,
            'stock': Stock,
            'sale': Sale,
        }[record.get('model')]
        session.add(model(id=record.get('pk'), **record.get('fields')))
    session.commit()



if __name__ == "__main__":
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    init_tests_data()

    publisher_input = input('Введите имя или идентификатор издателя')

    try:
        publisher_id = int(publisher_input)
        publisher = (Session().query(Publisher).filter(Publisher.id == publisher_id).first())

    except ValueError:
        publisher = (Session().query(Publisher).filter(Publisher.name == publisher_id).first())

    if publisher is None:
        print('Издатель не найден')
    else:
        sales = (
            Session()
            .query(Sale)
            .join(Stock)
            .join(Stock.shop)
            .join(Book)
            .join(Publisher)
            .filter(Publisher.id == publisher_id)
            .order_by(Sale.date_sale)
            .all()
         )

        for sale in sales:
            print(f'{sale.stock.book.title} | {sale.stock.shop.name} | {sale.price} | {sale.date_sale}')

        print(f'Найдено {len(sales)} продаж для издателя {publisher.name}')
































