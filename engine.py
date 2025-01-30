from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


login = 'postgres'
password = 'N=_R90Wc'
DB = 'book_sales'

DSN = f'postgresql://{login}:{password}@localhost:5432/{DB}'
engine = create_engine(DSN)
Session = sessionmaker(bind=engine)