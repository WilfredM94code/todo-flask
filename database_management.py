from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('postgresql://WilfredM94code:Ralph2828@localhost:5432/flask_todolist')

Base = declarative_base()

class Topics(Base):
    __tablename__ = 'topics'
    topic_id = Column(Integer, primary_key = True)
    title = Column(String(length=255))
    def __repr__(self):
        return f"<Topics(topic_id = '{self.topic_id}', title = '{self.title}')>"

class Tasks(Base):
    __tablename__ = 'tasks'
    task_id = Column(Integer, primary_key = True)
    topic_id = Column(Integer, ForeignKey('topics.topic_id'))
    description = Column(String(length=255))
    def __repr__(self):
        return f"<Tasks(task_id = '{self.task_id}', topic_id = '{self.topic_id}', description = '{self.description}')>"


Base.metadata.create_all(engine)

def create_session():
    session = sessionmaker(bind=engine)
    return session()

if __name__ == '__main__':
    session = create_session()
    topic = Topics(title='Topic #1')
    session.add(topic)
    session.commit()
    task = Tasks(description = 'Task #1', topic_id = topic.topic_id)
    session.add(task)
    session.commit()