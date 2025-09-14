from fastapi import FastAPI
from models import Produto
import couchdb

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # libera para qualquer origem (pode restringir depois)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# http
couch = couchdb.Server("http://admin:123@couchdb-on-render-p6w8.onrender.com")
db_name ="produtos"

# se o db name estiver em server entao atribui em db caminho couch[db_name]
# se não ele cria o banco em db atribuindo o novo valor em db

if db_name in couch:
    db = couch[db_name]
else:
    db = couch.create(db_name)


@app.get('/produtos')
async def listar_produtos():
    produtos = []
    for doc_id in db:
        produtos.append(db[doc_id])
    return produtos

@app.post("/produtos")
async def criar_produto(produto: Produto):
    
    for doc_id in db:
        doc = db[doc_id]
        if doc.get("nome") == produto.nome:
            return {"erro": f"O produto '{produto.nome}' já existe!"}


    id_do_documento, revisao = db.save(produto.dict())

    return {
        "_id": id_do_documento,
        "_rev": revisao,
        "nome": produto.nome,
        "preco": produto.preco,
    }

if __name__ == '__main__':
    import uvicorn

    uvicorn.run('main:app', port=3044, host='0.0.0.0', reload=True)
print('Servidor rodando: http://127.0.1.0:3044')

