import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


class Language(Base):
    __tablename__ = 'language'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    @property
    def serialize(self):
        return {
            'name': self.name,
            'id': self.id,
        }


class FrameWork(Base):
    __tablename__ = 'framework'

    name = Column(String(80), nullable=False)
    id = Column(Integer, primary_key=True)
    description = Column(String(250))
    website = Column(String(250))
    language_id = Column(Integer, ForeignKey('language.id'))
    language = relationship(Language)

    @property
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'website': self.website,
        }


engine = create_engine('sqlite:///frameworksmenu.db')


Base.metadata.create_all(engine)
