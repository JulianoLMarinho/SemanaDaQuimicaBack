from sqlalchemy import BigInteger, Boolean, Column, Date, ForeignKey, Integer, LargeBinary, String, Table, Time, text
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class BaseModel(Base):
    __abstract__ = True
