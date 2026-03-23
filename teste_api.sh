#!/bin/bash
# Script para testar os endpoints atuais da API REST

API_URL="http://127.0.0.1:8000/api"

if command -v python >/dev/null 2>&1; then
  PYTHON_CMD="python"
elif command -v python3 >/dev/null 2>&1; then
  PYTHON_CMD="python3"
else
  echo "Erro: nenhum interpretador Python encontrado (python/python3)."
  exit 1
fi

pretty_print() {
  "$PYTHON_CMD" -m json.tool 2>/dev/null || cat
}

echo "Testando API REST..."
echo ""

echo "1. Listando clientes:"
curl -s "${API_URL}/clientes/" | pretty_print || echo "Nenhum cliente"
echo ""

echo "2. Listando produtos:"
curl -s "${API_URL}/produtos/" | pretty_print || echo "Nenhum produto"
echo ""

echo "3. Listando fornecedores:"
curl -s "${API_URL}/fornecedores/" | pretty_print || echo "Nenhum fornecedor"
echo ""

echo "4. Listando compras:"
curl -s "${API_URL}/compras/" | pretty_print || echo "Nenhuma compra"
echo ""

echo "5. Listando vendas:"
curl -s "${API_URL}/vendas/" | pretty_print || echo "Nenhuma venda"
echo ""

echo "6. Criando um novo cliente:"
curl -s -X POST "${API_URL}/clientes/" \
  -H "Content-Type: application/json" \
  -d '{"nome": "Joao Silva", "email": "joao@example.com", "telefone": "11999999999"}' | pretty_print
echo ""

echo "7. Criando um novo produto:"
curl -s -X POST "${API_URL}/produtos/" \
  -H "Content-Type: application/json" \
  -d '{"nome": "Notebook", "preco": 3500.00, "descricao": "Notebook Dell", "quantidade": 10, "preco_compra": 2800.00, "preco_venda": 3500.00}' | pretty_print
echo ""

echo "8. Criando um novo fornecedor:"
curl -s -X POST "${API_URL}/fornecedores/" \
  -H "Content-Type: application/json" \
  -d '{"nome_fantasia": "Fornecedor API", "cnpj": "99.999.999/0001-99", "tipo_fornecimento": "PRODUTOS"}' | pretty_print
echo ""

echo "9. Acessando acao customizada - Produtos em estoque:"
curl -s "${API_URL}/produtos/em_estoque/" | pretty_print || echo "Nenhum produto em estoque"
echo ""

echo "10. Acessando acao customizada - Produtos sem estoque:"
curl -s "${API_URL}/produtos/sem_estoque/" | pretty_print || echo "Nenhum produto sem estoque"
echo ""

echo "11. Acessando acao customizada - Clientes por email:"
curl -s "${API_URL}/clientes/por_email/?email=joao@example.com" | pretty_print || echo "Nenhum cliente com esse email"
echo ""

echo "Testes finalizados!"
