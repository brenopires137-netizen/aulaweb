# Documentação da API REST

## Base URL
```
http://127.0.0.1:8000/api/
```

## Endpoints Disponíveis

### Clientes

#### 1. Listar todos os clientes
```
GET /api/clientes/
```
Retorna uma lista paginada de clientes.

**Resposta de exemplo:**
```json
{
  "count": 3,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "nome": "breno",
      "email": "breno5@gmail.com",
      "telefone": "4002-8922",
      "criado_em": "2026-02-09T16:32:40.879700-03:00"
    }
  ]
}
```

#### 2. Obter um cliente específico
```
GET /api/clientes/{id}/
```

#### 3. Criar um novo cliente
```
POST /api/clientes/
Content-Type: application/json

{
  "nome": "João Silva",
  "email": "joao@example.com",
  "telefone": "11999999999"
}
```

#### 4. Atualizar um cliente
```
PUT /api/clientes/{id}/
PATCH /api/clientes/{id}/
```

#### 5. Deletar um cliente
```
DELETE /api/clientes/{id}/
```

#### 6. Buscar clientes por email
```
GET /api/clientes/por_email/?email=breno5@gmail.com
```

---

### Produtos

#### 1. Listar todos os produtos
```
GET /api/produtos/
```

#### 2. Obter um produto específico
```
GET /api/produtos/{id}/
```

#### 3. Criar um novo produto
```
POST /api/produtos/
Content-Type: application/json

{
  "nome": "Notebook",
  "preco": 3500.00,
  "descricao": "Notebook Dell",
  "quantidade": 10,
  "preco_compra": 2800.00,
  "preco_venda": 3500.00,
  "data_validade": "2027-02-24"
}
```

#### 4. Atualizar um produto
```
PUT /api/produtos/{id}/
PATCH /api/produtos/{id}/
```

#### 5. Deletar um produto
```
DELETE /api/produtos/{id}/
```

#### 6. Listar produtos em estoque
```
GET /api/produtos/em_estoque/
```

#### 7. Listar produtos sem estoque
```
GET /api/produtos/sem_estoque/
```

#### 8. Atualizar quantidade de um produto
```
POST /api/produtos/{id}/atualizar_quantidade/
Content-Type: application/json

{
  "quantidade": 20
}
```

---

## Respostas de Status HTTP

- **200 OK**: Requisição bem-sucedida
- **201 Created**: Recurso criado com sucesso
- **204 No Content**: Recurso deletado com sucesso
- **400 Bad Request**: Erro na requisição (dados inválidos)
- **404 Not Found**: Recurso não encontrado
- **405 Method Not Allowed**: Método HTTP não permitido

---

## Autenticação

Atualmente, a API não requer autenticação. Em produção, recomenda-se implementar:
- Token Authentication
- JWT (JSON Web Tokens)
- OAuth2

---

## Paginação

A API retorna resultados paginados com 10 itens por página. Use os parâmetros:

```
GET /api/clientes/?page=2
GET /api/produtos/?page=1
```

---

## Exemplos com cURL

### Listar clientes
```bash
curl http://127.0.0.1:8000/api/clientes/
```

### Criar cliente
```bash
curl -X POST http://127.0.0.1:8000/api/clientes/ \
  -H "Content-Type: application/json" \
  -d '{"nome": "Maria", "email": "maria@example.com", "telefone": "11988888888"}'
```

### Listar produtos em estoque
```bash
curl http://127.0.0.1:8000/api/produtos/em_estoque/
```

### Atualizar quantidade de um produto
```bash
curl -X POST http://127.0.0.1:8000/api/produtos/1/atualizar_quantidade/ \
  -H "Content-Type: application/json" \
  -d '{"quantidade": 25}'
```
