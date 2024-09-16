from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from .database import Base

class Student(Base):
    __tablename__ = 'students'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    
    # Relationships
    enrollments = relationship("Enrollment", back_populates="student", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"Student(id={self.id}, name={self.name}, email={self.email})"
