from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import Column, String, Integer, create_engine
import os
import pandas as pd

BASE_DIR = os.path.dirname(os.path.realpath(__file__))
Base = declarative_base()
db_path = "sqlite:///" + os.path.join(BASE_DIR, "products.db")
engine = create_engine(db_path)
Session = sessionmaker()
Session.configure(bind=engine)


class Product(Base):
    __tablename__ = "Products"
    id = Column(Integer(), primary_key=True)
    title = Column(String(255), nullable=False)
    price = Column(String(80), nullable=False)


def save_to_excel(products):
    dataframe = pd.DataFrame(products)
    data_to_excel = pd.ExcelWriter('products.xlsx', engine='xlsxwriter')
    dataframe.to_excel(data_to_excel, sheet_name='products_1')
    data_to_excel.save()


def save_data(products):
    if not os.path.isfile(db_path):
        Base.metadata.create_all(engine)
    for product in products:
        new_product = Product(title=product["product_title"], price=product["product_price"])
        local_session = Session()
        local_session.add(new_product)
        local_session.commit()
    save_to_excel(products)
