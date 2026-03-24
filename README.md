# Sistema de Gerenciamento de Vendas e Compras

Um projeto Django com API REST para gerenciar clientes, produtos, fornecedores, compras e vendas em tempo real.

## 📋 Visão Geral

Este projeto implementa um sistema completo para controle de estoque e transações comerciais com:

- **Interface Web** com painel de administração
- **API REST** completa com Django REST Framework
- **Banco de dados** SQLite para persistência
- **Autenticação** por login/logout na interface web
- **Regras de negócio** para estoque e confirmação de vendas/compras

## 🏗️ Estrutura do Projeto

```
projeto/
├── clientes/           # Gerenciamento de clientes
├── produtos/           # Catálogo e estoque de produtos
├── fornecedores/       # Base de fornecedores
├── compras/            # Registro e confirmação de compras
├── vendas/             # Registro e confirmação de vendas
├── projeto/            # Configurações do Django
├── templates/          # Templates HTML
├── db.sqlite3          # Banco de dados
└── manage.py           # Script de gerenciamento Django
```

## 🛠️ Stack Técnico

- **Python 3.x**
- **Django 6.x**
- **Django REST Framework**
- **SQLite**

## 📦 Instalação

### 1. Clonar o repositório

```bash
cd /home/breno/Documentos/breno-09-03/aulaweb
```

### 2. Instalar dependências

```bash
pip install django djangorestframework
```

### 3. Executar migrações (se necessário)

```bash
cd projeto
python manage.py migrate
```

## 🚀 Como Executar

### Iniciar o servidor de desenvolvimento

```bash
cd projeto
python manage.py runserver
```

O servidor estará disponível em:
- **Interface web**: `http://127.0.0.1:8000/`
- **API REST**: `http://127.0.0.1:8000/api/`

### Acessar a interface web

1. Acesse `http://127.0.0.1:8000/`
2. Faça login com suas credenciais
3. Acesse os módulos: Clientes, Produtos, Fornecedores, Compras e Vendas

## 🔌 API REST

Todas as operações CRUD estão disponíveis via API REST.

### Base URL

```
http://127.0.0.1:8000/api/
```

### Paginação

- Tamanho da página: 10 itens
- Formato: `?page=1`, `?page=2`, etc.

```json
{
  "count": 100,
  "next": "http://127.0.0.1:8000/api/clientes/?page=2",
  "previous": null,
  "results": [...]
}
```

### Módulos da API

#### 1. **Clientes**

Gerencia dados de clientes.

**Endpoints CRUD:**
- `GET /api/clientes/` - Listar todos
- `GET /api/clientes/{id}/` - Detalhes de um cliente
- `POST /api/clientes/` - Criar novo cliente
- `PUT /api/clientes/{id}/` - Atualizar completamente
- `PATCH /api/clientes/{id}/` - Atualizar parcialmente
- `DELETE /api/clientes/{id}/` - Deletar

**Ações customizadas:**
- `GET /api/clientes/por_email/?email=joao@example.com` - Buscar por email

**Campos:**
- `nome` (obrigatório)
- `email` (obrigatório)
- `telefone`
- `criado_em` (somente leitura)

**Exemplo de criação:**

```json
{
  "nome": "João Silva",
  "email": "joao@example.com",
  "telefone": "11999999999"
}
```

#### 2. **Produtos**

Gerencia catálogo e estoque de produtos.

**Endpoints CRUD:**
- `GET /api/produtos/` - Listar todos
- `GET /api/produtos/{id}/` - Detalhes de um produto
- `POST /api/produtos/` - Criar novo produto
- `PUT /api/produtos/{id}/` - Atualizar completamente
- `PATCH /api/produtos/{id}/` - Atualizar parcialmente
- `DELETE /api/produtos/{id}/` - Deletar

**Ações customizadas:**
- `GET /api/produtos/em_estoque/` - Produtos com quantidade > 0
- `GET /api/produtos/sem_estoque/` - Produtos com quantidade = 0
- `POST /api/produtos/{id}/atualizar_quantidade/` - Atualizar quantidade

**Campos:**
- `nome` (obrigatório)
- `preco`
- `descricao`
- `quantidade` (estoque atual)
- `preco_compra` (último preço de compra)
- `preco_venda` (preço de venda)
- `data_validade`
- `criado_em` e `atualizado_em` (somente leitura)

**Exemplo de criação:**

```json
{
  "nome": "Notebook Dell",
  "preco": 3500.0,
  "descricao": "Notebook 15 polegadas",
  "quantidade": 10,
  "preco_compra": 2800.0,
  "preco_venda": 3500.0,
  "data_validade": "2027-12-31"
}
```

#### 3. **Fornecedores**

Gerencia base de fornecedores.

**Endpoints CRUD:**
- `GET /api/fornecedores/` - Listar todos
- `GET /api/fornecedores/{id}/` - Detalhes de um fornecedor
- `POST /api/fornecedores/` - Criar novo fornecedor
- `PUT /api/fornecedores/{id}/` - Atualizar completamente
- `PATCH /api/fornecedores/{id}/` - Atualizar parcialmente
- `DELETE /api/fornecedores/{id}/` - Deletar

**Ações customizadas:**
- `GET /api/fornecedores/por_cnpj/?cnpj=12.345.678/0001-90` - Buscar por CNPJ

**Campos principais:**
- `nome_fantasia` (obrigatório)
- `razao_social`
- `cnpj`
- `tipo_fornecimento`
- `categorias_fornecidas`
- `itens_fornecidos`
- `email`
- `telefone`
- `endereco`, `cidade`, `estado`
- `contato`
- `observacoes`
- `criado_em` e `atualizado_em` (somente leitura)

**Exemplo de criação:**

```json
{
  "nome_fantasia": "Mercado Central",
  "razao_social": "Mercado Central LTDA",
  "cnpj": "12.345.678/0001-90",
  "tipo_fornecimento": "PRODUTOS",
  "categorias_fornecidas": "Alimentos",
  "itens_fornecidos": "Arroz, Feijão",
  "email": "contato@mercadocentral.com",
  "telefone": "1133334444"
}
```

#### 4. **Compras**

Registra compras de fornecedores.

**Endpoints CRUD:**
- `GET /api/compras/` - Listar todas
- `GET /api/compras/{id}/` - Detalhes de uma compra
- `POST /api/compras/` - Registrar nova compra
- `PUT /api/compras/{id}/` - Atualizar completamente
- `PATCH /api/compras/{id}/` - Atualizar parcialmente
- `DELETE /api/compras/{id}/` - Deletar

**Campos principais:**
- `produto` (ID do produto)
- `fornecedor` (ID do fornecedor)
- `preco_compra` (preço unitário pago)
- `preco_venda` (preço de venda sugerido)
- `data_compra`
- `quantidade`
- `confirmada` (true/false)
- `confirmado_em` (data de confirmação)
- `criado_em` (somente leitura)

**Regras de negócio:**
- ✅ Compra **confirmada** incrementa o estoque do produto
- ⚠️ Compra **pendente** não altera o estoque
- 💰 Preços da compra atualizam `preco_compra` e `preco_venda` do produto
- ❌ Não permite operações que deixem estoque negativo

**Exemplo de criação:**

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

#### 5. **Vendas**

Registra vendas para clientes.

**Endpoints CRUD:**
- `GET /api/vendas/` - Listar todas
- `GET /api/vendas/{id}/` - Detalhes de uma venda
- `POST /api/vendas/` - Registrar nova venda
- `PUT /api/vendas/{id}/` - Atualizar completamente
- `PATCH /api/vendas/{id}/` - Atualizar parcialmente
- `DELETE /api/vendas/{id}/` - Deletar

**Campos principais:**
- `cliente` (ID do cliente)
- `produto` (ID do produto)
- `preco_unitario` (preço de venda)
- `data_venda`
- `quantidade`
- `confirmada` (true/false)
- `confirmado_em` (data de confirmação)
- `criado_em` (somente leitura)

**Regras de negócio:**
- ✅ Venda **confirmada** baixa o estoque do produto
- ⚠️ Venda **pendente** não altera o estoque
- ❌ Não permite vender acima do estoque disponível
- ❌ Não permite regressão de confirmada para pendente

**Exemplo de criação:**

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

## 📝 Códigos HTTP Retornados

| Código | Significado |
|--------|-------------|
| `200 OK` | Sucesso em GET, PUT, PATCH ou ações customizadas |
| `201 Created` | Recurso criado com sucesso |
| `204 No Content` | Deletado com sucesso |
| `400 Bad Request` | Payload ou regra de negócio inválida |
| `404 Not Found` | Recurso não encontrado |
| `405 Method Not Allowed` | Operação não permitida |

## 🧪 Testes

Scripts de teste disponíveis na raiz do projeto:

### Teste básico de endpoints

```bash
./teste_api.sh
```

Testa endpoints principais e ações customizadas.

### Teste completo fim-a-fim

```bash
./teste_api_completo.sh
```

Executa fluxo completo:
1. Cria cliente
2. Cria fornecedor
3. Cria produto
4. Registra compra
5. Confirma compra (atualiza estoque)
6. Registra venda
7. Confirma venda (baixa estoque)

## 🔐 Autenticação

### Interface Web

- **Login obrigatório**: `http://127.0.0.1:8000/login`
- **Logout**: `http://127.0.0.1:8000/logout`
- Usa sessão de navegador

### API REST

- **Atual**: Sem autenticação obrigatória
- **Futuro**: Será implementado Token ou JWT

## 📚 Documentação Adicional

- [IMPLEMENTACAO_API.md](IMPLEMENTACAO_API.md) - Detalhes técnicos da API
- [projeto/API_DOCUMENTATION.md](projeto/API_DOCUMENTATION.md) - Referência completa de endpoints

## 🎯 Próximos Passos Recomendados

1. ✅ Adicionar autenticação por Token/JWT na API
2. ✅ Implementar permissões por perfil
3. ✅ Criar testes automatizados (pytest/APITestCase)
4. ✅ Padronizar validações com exemplos versionados
5. ✅ Adicionar documentação Swagger/OpenAPI

## 📄 Licença

Este projeto é fornecido como está para fins educacionais e de demonstração.

## 👤 Autor

Desenvolvido como projeto de aprendizado em Django e REST APIs.

---

**Última atualização**: Março de 2026
