from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Float
from database.db import Base
from sqlalchemy.sql import func


class Receipt(Base):
    __tablename__ = 'receipt'
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    date_upload = Column(DateTime(timezone=True), server_default=func.now())
    user_id = Column(Integer, index=True)

    def __repr__(self):
        return f'Чек id={self.id} - "{self.name}" был загружен {self.date_upload} пользователем id={self.user_id}'


class Category(Base):
    __tablename__ = 'category'
    id = Column(Integer, primary_key=True, nullable=True)
    name = Column(String, index=True)

    def __repr__(self):
        return self.name


class CategoryTrigger(Base):
    __tablename__ = 'category_trigger'
    id = Column(Integer, primary_key=True)
    category_id = Column(Integer, ForeignKey('category.id'))
    name = Column(String)

    def __repr__(self):
        return f'CategoryTrigger id: {self.id}, name: {self.name}, category_id: {self.category_id}'


class Good(Base):
    __tablename__ = 'good'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    price = Column(Float)
    quantity = Column(Integer)
    sum = Column(Float)
    category_name = Column(String, nullable=False)
    receipt_id = Column(Integer, ForeignKey('receipt.id'))
    category_id = Column(Integer, ForeignKey('category.id'))

    def __repr__(self):
        return ((f'Чек id={self.receipt_id}, id товара={self.id},'
              f'Название={self.name}, Цена={self.price},'
                f'Количество={self.quantity}, Стоимость={self.sum}'))
