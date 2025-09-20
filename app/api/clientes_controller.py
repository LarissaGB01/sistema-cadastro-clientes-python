from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import asyncio

from ..application.services import validar_cpf, persistir_cliente
from ..domain.schemas import ClienteDTO
from ..infrastructure.database import get_db
from ..infrastructure.rabbitmq_client import publicar_cliente

router = APIRouter()

def sanitize_cliente_data(cliente):
    cliente.cpf = cliente.cpf.replace(".", "").replace("-", "")
    cliente.nome = cliente.nome[:30]

@router.post("/v1/clientes", status_code=201)
def criar_cliente_v1(cliente: ClienteDTO, db: Session = Depends(get_db)):
    sanitize_cliente_data(cliente)
    return persistir_cliente(cliente, db)

@router.post("/v2/clientes", status_code=201)
async def criar_cliente_v2(cliente: ClienteDTO, db: Session = Depends(get_db)):
    sanitize_cliente_data(cliente)
    await validar_cpf(cliente.cpf)
    return persistir_cliente(cliente, db)

@router.post("/v3/clientes", status_code=201)
async def criar_cliente_v3(cliente: ClienteDTO, db: Session = Depends(get_db)):
    sanitize_cliente_data(cliente)
    await validar_cpf(cliente.cpf)
    novo_cliente = persistir_cliente(cliente, db)
    publicar_cliente(novo_cliente)
    return novo_cliente

@router.post("/v4/clientes", status_code=201)
async def criar_cliente_v4(clientes: List[ClienteDTO], db: Session = Depends(get_db)):
    resultados = []

    async def processar_cliente(cliente: ClienteDTO):
        try:
            sanitize_cliente_data(cliente)
            await validar_cpf(cliente.cpf)
            novo_cliente = persistir_cliente(cliente, db)
            publicar_cliente(novo_cliente)

            return {
                "cpf": novo_cliente.cpf,
                "nome": novo_cliente.nome,
                "sistema": novo_cliente.sistema,
                "status": "Cliente cadastrado",
                "error": None
            }
        
        except Exception as e:
            print(f"Erro ao processar cliente {cliente.cpf}: {e}")
            
            return {
                "cpf": cliente.cpf,
                "nome": None,
                "sistema": None,
                "status": "Erro ao cadastrar cliente",
                "error": str(e)
            }

    tarefas = [processar_cliente(cliente) for cliente in clientes]
    resultados = await asyncio.gather(*tarefas)

    return {"resultados": resultados}