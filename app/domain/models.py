from sqlalchemy import Column, String

from ..infrastructure.database import Base

class Clientes(Base):
    __tablename__ = "clientes"

    cpf = Column(String(11), primary_key=True, index=True)
    nome = Column(String(100))
    sistema = Column(String(10), default="PYTHON")

