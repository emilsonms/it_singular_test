# Projeto simples de autenticação

Este é um projeto de exemplo que implementa autenticação usando JWT, rotas protegidas com permissões baseadas em papéis, e integração com banco de dados utilizando SQLAlchemy. As rotas incluem `/user` e `/admin`, onde apenas administradores podem acessar a rota `/admin`.

## Tecnologias Utilizadas

- [FastAPI](https://fastapi.tiangolo.com/)
- [Pydantic](https://pydantic-docs.helpmanual.io/)
- [SQLAlchemy](https://www.sqlalchemy.org/)
- [Passlib](https://passlib.readthedocs.io/en/stable/)
- [JWT (JSON Web Tokens)](https://jwt.io/)
- [Pytest](https://docs.pytest.org/en/stable/)

## Pré-requisitos

- Python 3.10 ou superior
- [Poetry](https://python-poetry.org/) ou `pip` para gerenciar pacotes
- `virtualenv` (opcional, mas recomendado)

## Configurar Ambiente Virtual

```
# Com virtualenv
python3 -m venv venv
source venv/bin/activate  # Para Linux/MacOS
venv\Scripts\activate     # Para Windows

pip install -r requirements.txt

```

## Renomeie o arquivo .env.example para .env

```
.env.example >> .env
```

## Executando a Aplicação
Execute o servidor FastAPI com uvicorn

```
uvicorn src.main:app --reload
```

## Criar Usuário

``` 
curl -X POST http://localhost:8000/create_user -H 'Content-Type: application/json' -d '{"username": "emilson", "password": "sua_senha", "role": "user"}'
```

## Fazer health check
```
curl --location http://localhost:8000/health
```

##  Fazer login
```
curl --location 'http://localhost:8000/token' \
--header 'Content-Type: application/json' \
--data '{
    "username": "emilson",
    "password": "sua_senha"
}'
```

## Acessar a rota user
```
curl --location 'http://localhost:8000/user' \
--header 'Authorization: bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJlbWlsc29uIiwiZXhwIjoxNzI4MDYyNzM3fQ.tVrjvE5Wrf62RccHNsRaBKOP7UkDUt71CAppVu7dpOo'
```

## Acessar a rota admin
```
curl --location 'http://localhost:8000/admin' \
--header 'Authorization: bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJlbWlsc29uIiwiZXhwIjoxNzI4MDYyNzM3fQ.tVrjvE5Wrf62RccHNsRaBKOP7UkDUt71CAppVu7dpOo'
```

## Fazendo os testes no projeto

Crie os usuários de teste

```
curl -X POST http://localhost:8000/create_user -H 'Content-Type: application/json' -d '{"username": "emilson", "password": "yfe8eu3kk", "role": "user"}'
curl -X POST http://localhost:8000/create_user -H 'Content-Type: application/json' -d '{"username": "admin", "password": "7fy7dyh2gn", "role": "admin"}'
```

## Execute os testes

```
pytest
```








## Licença
Este projeto é licenciado sob a MIT License.