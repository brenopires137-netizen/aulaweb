# Implementacao API REST - Estado Atual do Projeto

## 1. Visao Geral

Este documento resume a implementacao da API REST do projeto Django e o que esta ativo hoje.

Stack principal:
- Django 6.x
- Django REST Framework
- SQLite (`projeto/db.sqlite3`)

Apps cobertos pela API:
- `clientes`
- `produtos`
- `fornecedores`
- `compras`
- `vendas`

## 2. Arquitetura da API

Arquivos centrais:
- `projeto/projeto/urls.py`: registra `DefaultRouter` e publica `/api/`
- `projeto/projeto/settings.py`: ativa `rest_framework` e paginacao
- `projeto/*/serializers.py`: define payloads por recurso
- `projeto/*/views.py`: `ModelViewSet` e acoes customizadas

Padrao adotado:
- `ModelViewSet` para CRUD completo
- Endpoints automáticos via router
- Acoes customizadas com `@action`

## 3. Configuracao Atual

### DRF

Em `projeto/projeto/settings.py`:
- `rest_framework` no `INSTALLED_APPS`
- Paginacao padrao:
	- `DEFAULT_PAGINATION_CLASS = PageNumberPagination`
	- `PAGE_SIZE = 10`

### Rotas

Em `projeto/projeto/urls.py`:
- `router.register('clientes', ClienteViewSet)`
- `router.register('produtos', ProdutoViewSet)`
- `router.register('fornecedores', FornecedorViewSet)`
- `router.register('compras', CompraViewSet)`
- `router.register('vendas', VendaViewSet)`

Base final da API:
- `http://127.0.0.1:8000/api/`

## 4. Endpoints Ativos

### 4.1 Clientes

CRUD:
- `GET /api/clientes/`
- `GET /api/clientes/{id}/`
- `POST /api/clientes/`
- `PUT /api/clientes/{id}/`
- `PATCH /api/clientes/{id}/`
- `DELETE /api/clientes/{id}/`

Custom:
- `GET /api/clientes/por_email/?email=...`

Campos relevantes:
- `id`, `nome`, `email`, `telefone`, `criado_em`

### 4.2 Produtos

CRUD:
- `GET /api/produtos/`
- `GET /api/produtos/{id}/`
- `POST /api/produtos/`
- `PUT /api/produtos/{id}/`
- `PATCH /api/produtos/{id}/`
- `DELETE /api/produtos/{id}/`

Custom:
- `GET /api/produtos/em_estoque/`
- `GET /api/produtos/sem_estoque/`
- `POST /api/produtos/{id}/atualizar_quantidade/`

Campos relevantes:
- `id`, `nome`, `preco`, `descricao`, `quantidade`
- `preco_compra`, `preco_venda`, `data_validade`
- `criado_em`, `atualizado_em`

### 4.3 Fornecedores

CRUD:
- `GET /api/fornecedores/`
- `GET /api/fornecedores/{id}/`
- `POST /api/fornecedores/`
- `PUT /api/fornecedores/{id}/`
- `PATCH /api/fornecedores/{id}/`
- `DELETE /api/fornecedores/{id}/`

Custom:
- `GET /api/fornecedores/por_cnpj/?cnpj=...`

### 4.4 Compras

CRUD:
- `GET /api/compras/`
- `GET /api/compras/{id}/`
- `POST /api/compras/`
- `PUT /api/compras/{id}/`
- `PATCH /api/compras/{id}/`
- `DELETE /api/compras/{id}/`

Campos relevantes atuais:
- `produto`, `fornecedor`
- `preco_compra`, `preco_venda`
- `data_compra`, `quantidade`
- `confirmada`, `confirmado_em`, `criado_em`

Observacao:
- o campo antigo `preco` foi substituido por `preco_compra` e `preco_venda` na compra.

### 4.5 Vendas

CRUD:
- `GET /api/vendas/`
- `GET /api/vendas/{id}/`
- `POST /api/vendas/`
- `PUT /api/vendas/{id}/`
- `PATCH /api/vendas/{id}/`
- `DELETE /api/vendas/{id}/`

Campos relevantes:
- `cliente`, `produto`
- `preco_unitario`
- `data_venda`, `quantidade`
- `confirmada`, `confirmado_em`, `criado_em`

## 5. Regras de Negocio Importantes

### Compras

- Compra confirmada incrementa estoque do produto.
- Compra pendente nao movimenta estoque.
- Precos da compra atualizam `preco_compra` e `preco_venda` do produto.
- Nao permite operacoes que deixem estoque negativo em ajustes/exclusoes.

### Vendas

- Venda confirmada baixa estoque do produto.
- Venda pendente nao movimenta estoque.
- Nao permite vender acima do estoque disponivel.
- Nao permite regressao de confirmada para pendente.

## 6. Autenticacao e Seguranca

Situacao atual:
- Interface web com login/logout obrigatorios (`/login`, `/logout`).
- API REST sem token/JWT obrigatorio neste momento.

Status HTTP comuns:
- `200`, `201`, `204`, `400`, `404`, `405`

## 7. Testes Disponiveis

Scripts no workspace:
- `teste_api.sh`: smoke test de endpoints principais e acoes customizadas.
- `teste_api_completo.sh`: fluxo fim a fim (cliente + fornecedor + produto + compra + venda).

Observacao tecnica:
- ambos scripts agora suportam ambientes com `python` ou `python3`.

## 8. Como Executar

Subir servidor:

```bash
cd projeto
python manage.py runserver
```

Rodar testes:

```bash
cd ..
./teste_api.sh
./teste_api_completo.sh
```

## 9. Limites Conhecidos

- API ainda nao usa autenticacao por token/JWT.
- Nao ha suite formal de testes automatizados (pytest/APITestCase) no repositorio.

## 10. Proximos Passos Recomendados

1. Adicionar autenticacao para API (Token ou JWT).
2. Aplicar permissoes por perfil na API.
3. Criar testes automatizados para regras criticas de estoque.
4. Padronizar validacoes de payload com exemplos versionados.

## 11. Conclusao

Sim, este arquivo agora esta completo e condiz com o estado atual do projeto.
Os endpoints, campos e regras listados aqui refletem a implementacao em codigo no momento.
