from sqlalchemy import create_engine, Column, ForeignKey, Integer, String, BigInteger, Text, SmallInteger
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

Base = declarative_base()


# Update these variables with your actual username, password, and database name
username = 'root'
password = 'my-secret-pw'
database_name = 'mm_platform'
host = 'localhost'
port = 3306


db_url = f'mysql+pymysql://{username}:{password}@{host}:{port}/{database_name}'
engine = create_engine(db_url)

class Task(Base):
    __tablename__ = 'task_tab'

    id = Column(BigInteger, primary_key=True)
    task_name = Column(String(255))
    input_path = Column(String(255))
    output_path = Column(String(255))
    status = Column(SmallInteger)


class ModelTaskResult(Base):
    __tablename__ = 'model_task_result_tab'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    task_id = Column(BigInteger, ForeignKey('task_tab.id'), nullable=False)
    model_id = Column(BigInteger, nullable=False)
    task_status = Column(SmallInteger, nullable=False)
    creat_time = Column(BigInteger, nullable=False)
    finish_time = Column(BigInteger, nullable=False)
    accuracy = Column(String(255), nullable=False)

    task = relationship("Task")

class Model(Base):
    __tablename__ = 'model_tab'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    model_name = Column(String(255), nullable=False)
    parameters = Column(Text, nullable=False)
    creat_time = Column(BigInteger, nullable=False)


Session = sessionmaker(bind=engine)