from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from database import Base

class Student(Base):
    __tablename__ = 'students'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    enrollments = relationship('Enrollment', back_populates='student')
