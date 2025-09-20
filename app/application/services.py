import httpx
from sqlalchemy.orm import Session

from ..domain.models import Clientes
from fastapi import HTTPException
from ..domain.schemas import ClienteDTO
from ..config import INVERTEXTO_TOKEN, INVERTEXTO_URL

async def validar_cpf(cpf: str):
    params = {"token": INVERTEXTO_TOKEN, "value": cpf}

    async with httpx.AsyncClient() as client:
        response = await client.get(INVERTEXTO_URL, params=params)
        if response.status_code != 200:
            raise HTTPException(status_code=502, detail="Erro ao validar CPF")

        data = response.json()
        if not data.get("valid", False):
            raise HTTPException(status_code=400, detail="CPF inválido")


def persistir_cliente(cliente: ClienteDTO, db: Session):
    existe = db.query(Clientes).filter(Clientes.cpf == cliente.cpf).first()
    
    if existe:
        raise HTTPException(status_code=400, detail="CPF já cadastrado")

    novo_cliente = Clientes(cpf=cliente.cpf, nome=cliente.nome)

    db.add(novo_cliente)
    db.commit()
    db.refresh(novo_cliente)
    
    return novo_cliente