# Documentacao da API (Estado Atual do Projeto)

## 1. Visao Geral

Este projeto expoe uma API REST com Django REST Framework para os modulos:

- `clientes`
- `produtos`
- `fornecedores`
- `compras`
- `vendas`

URL base:

```
http://127.0.0.1:8000/api/
```

## 2. Convencoes da API

### 2.1 Paginacao

- Paginacao padrao: `PageNumberPagination`
- Tamanho da pagina: `10`

Formato de resposta para listagens:

```json
{
  "count": 1,
  "next": null,
  "previous": null,
  "results": []
}
```

Exemplo:

```
GET /api/clientes/?page=2
```

### 2.2 Content-Type

Use JSON para escrita:

```
Content-Type: application/json
```

### 2.3 Codigos HTTP Comuns

- `200 OK` sucesso (GET/PUT/PATCH/acoes customizadas)
- `201 Created` criado com sucesso
- `204 No Content` removido com sucesso
- `400 Bad Request` payload/regra invalida
- `404 Not Found` recurso nao encontrado
- `405 Method Not Allowed` metodo nao suportado

## 3. Autenticacao

- Interface web usa login/logout de sessao (`/login`, `/logout`).
- Endpoints da API atualmente nao exigem token/JWT.

## 4. Endpoints por Modulo

### 4.1 Clientes

CRUD:

- `GET /api/clientes/`
- `GET /api/clientes/{id}/`
- `POST /api/clientes/`
- `PUT /api/clientes/{id}/`
- `PATCH /api/clientes/{id}/`
- `DELETE /api/clientes/{id}/`

Acao customizada:

- `GET /api/clientes/por_email/?email=...`

Campos principais:

- `id` (somente leitura)
- `nome`
- `email`
- `telefone`
- `criado_em` (somente leitura)

Exemplo de criacao:

```json
{
  "nome": "Joao Silva",
  "email": "joao@example.com",
  "telefone": "11999999999"
}
```

### 4.2 Produtos

CRUD:

- `GET /api/produtos/`
- `GET /api/produtos/{id}/`
- `POST /api/produtos/`
- `PUT /api/produtos/{id}/`
- `PATCH /api/produtos/{id}/`
- `DELETE /api/produtos/{id}/`

Acoes customizadas:

- `GET /api/produtos/em_estoque/`
- `GET /api/produtos/sem_estoque/`
- `POST /api/produtos/{id}/atualizar_quantidade/`

Campos principais:

- `id` (somente leitura)
- `nome`
- `preco`
- `descricao`
- `quantidade`
- `preco_compra`
- `preco_venda`
- `data_validade`
- `criado_em` (somente leitura)
- `atualizado_em` (somente leitura)

Exemplo de criacao:

```json
{
  "nome": "Notebook",
  "preco": 3500.0,
  "descricao": "Notebook Dell",
  "quantidade": 10,
  "preco_compra": 2800.0,
  "preco_venda": 3500.0,
  "data_validade": "2027-02-24"
}
```

Exemplo de payload da acao `atualizar_quantidade`:

```json
{
  "quantidade": 25
}
```

### 4.3 Fornecedores

CRUD:

- `GET /api/fornecedores/`
- `GET /api/fornecedores/{id}/`
- `POST /api/fornecedores/`
- `PUT /api/fornecedores/{id}/`
- `PATCH /api/fornecedores/{id}/`
- `DELETE /api/fornecedores/{id}/`

Acao customizada:

- `GET /api/fornecedores/por_cnpj/?cnpj=...`

Campos principais:

- `id` (somente leitura)
- `nome_fantasia`
- `razao_social`
- `cnpj`
- `tipo_fornecimento`
- `categorias_fornecidas`
- `itens_fornecidos`
- `email`
- `telefone`
- `endereco`
- `cidade`
- `estado`
- `contato`
- `observacoes`
- `criado_em` (somente leitura)
- `atualizado_em` (somente leitura)

Exemplo de criacao:

```json
{
  "nome_fantasia": "Mercado Central",
  "razao_social": "Mercado Central LTDA",
  "cnpj": "12.345.678/0001-90",
  "tipo_fornecimento": "PRODUTOS",
  "itens_fornecidos": "arroz, feijao",
  "email": "contato@mercadocentral.com"
}
```

### 4.4 Compras

CRUD:

- `GET /api/compras/`
- `GET /api/compras/{id}/`
- `POST /api/compras/`
- `PUT /api/compras/{id}/`
- `PATCH /api/compras/{id}/`
- `DELETE /api/compras/{id}/`

Campos principais:

- `id` (somente leitura)
- `produto`
- `produto_nome` (somente leitura)
- `fornecedor`
- `fornecedor_nome` (somente leitura)
- `preco_compra`
- `preco_venda`
- `data_compra`
- `quantidade`
- `confirmada`
- `confirmado_em` (somente leitura)
- `criado_em` (somente leitura)

Exemplo de criacao:

```json
{
  "produto": 1,
  "fornecedor": 1,
  "preco_compra": 8.5,
  "preco_venda": 12.0,
  "data_compra": "2026-03-22",
  "quantidade": 20,
  "confirmada": false
}
```

Observacoes de regra:

- Compra confirmada entra no estoque.
- Compra pendente nao altera estoque.

### 4.5 Vendas

CRUD:

- `GET /api/vendas/`
- `GET /api/vendas/{id}/`
- `POST /api/vendas/`
- `PUT /api/vendas/{id}/`
- `PATCH /api/vendas/{id}/`
- `DELETE /api/vendas/{id}/`

Campos principais:

- `id` (somente leitura)
- `cliente`
- `cliente_nome` (somente leitura)
- `produto`
- `produto_nome` (somente leitura)
- `preco_unitario`
- `data_venda`
- `quantidade`
- `confirmada`
- `confirmado_em` (somente leitura)
- `criado_em` (somente leitura)

Exemplo de criacao:

```json
{
  "cliente": 1,
  "produto": 1,
  "preco_unitario": 12.0,
  "data_venda": "2026-03-22",
  "quantidade": 2,
  "confirmada": false
}
```

Observacoes de regra:

- Venda confirmada baixa estoque.
- Venda pendente nao altera estoque.
- Venda acima do estoque disponivel e rejeitada.

## 5. Exemplos Praticos com cURL

```bash
# Listar clientes
curl -s http://127.0.0.1:8000/api/clientes/

# Buscar cliente por email
curl -s "http://127.0.0.1:8000/api/clientes/por_email/?email=joao@example.com"

# Listar produtos em estoque
curl -s http://127.0.0.1:8000/api/produtos/em_estoque/

# Atualizar quantidade de produto
curl -s -X POST http://127.0.0.1:8000/api/produtos/1/atualizar_quantidade/ \
  -H "Content-Type: application/json" \
  -d '{"quantidade": 25}'

# Criar compra
curl -s -X POST http://127.0.0.1:8000/api/compras/ \
  -H "Content-Type: application/json" \
  -d '{"produto":1,"fornecedor":1,"preco_compra":10.0,"preco_venda":15.0,"data_compra":"2026-03-22","quantidade":5,"confirmada":false}'

# Criar venda
curl -s -X POST http://127.0.0.1:8000/api/vendas/ \
  -H "Content-Type: application/json" \
  -d '{"cliente":1,"produto":1,"preco_unitario":15.0,"data_venda":"2026-03-22","quantidade":1,"confirmada":false}'
```

## 6. Limitacoes Atuais

- API ainda sem autenticacao por token/JWT.
- Nao ha suite formal de testes automatizados versionada (unit/integration), apenas scripts shell.

## 7. Arquivos Relacionados

- `IMPLEMENTACAO_API.md` (resumo de implementacao)
- `teste_api.sh` (teste rapido/smoke)
- `teste_api_completo.sh` (fluxo ponta a ponta)
