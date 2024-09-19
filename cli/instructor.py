from sqlalchemy import Column, Integer, String
from database import Base

class Instructor(Base):
    __tablename__ = 'instructors'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    def __repr__(self):
        return f"<Instructor(name={self.name})>"
