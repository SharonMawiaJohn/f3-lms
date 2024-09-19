from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from database import Base

class Course(Base):
    __tablename__ = 'courses'

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    instructor_id = Column(Integer, nullable=False)

    enrollments = relationship('Enrollment', back_populates='course')
