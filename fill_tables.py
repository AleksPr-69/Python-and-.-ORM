import json

import sqlalchemy
from sqlalchemy.orm import sessionmaker

from create_ORM_class import create_tables, Publisher, Shop, Book, Stock, Sale

def fill_tables():
    print('Введите данные для заполнения таблиц!')
    login = input('Введите логин: ')
    password = input('Введите пароль: ')
    DB = input('Введите название базы данных: ')
    DSN = f'postgresql://{login}:{password}@localhost:5432/{DB}'

    engine = sqlalchemy.create_engine(DSN)
    create_tables(engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    def init_tests_data(session):
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

    init_tests_data(session) 

    def query():
        publish = input('Введите имя автора или id: ')
        if publish.isdigit():
            for pub in session.query(Publisher).filter(Publisher.id == int(publish)).all():
                print(pub)
            print('Его книги продаются в магазинах: ')    
            for s in session.query(Shop).join(Stock.shop).join(Book).join(Publisher).filter(Publisher.id==int(publish)).all():
                print(s)    
        else:
            for pub in session.query(Publisher).filter(Publisher.name.like(publish)).all():
                print(pub)
            print('Его книги продаются в магазинах: ')
            for s in session.query(Shop).join(Stock.shop).join(Book).join(Publisher).filter(Publisher.name==publish).all():
                print(s)

    query()            

fill_tables()