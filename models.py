from typing import Optional

from pydantic import BaseModel



class Produto(BaseModel):
    #id: Optional[int] = None
    nome: str
    preco: float
    disponivel: bool = True