from sqlalchemy import Column,Integer,String
from .database import Base
# this file is the main structure of the tables in database, this file will guide as what fields are in a table and how many tables are there.
class Blog(Base):
    __tablename__ = "Users"
    id = Column(Integer,primary_key=True,index=True)
    title = Column(String)
    body = Column(String)