#!/bin/bash
# Script para testar os endpoints da API REST

API_URL="http://127.0.0.1:8000/api"
echo "Testando API REST..."
echo ""

echo "1. Listando clientes:"
curl -s "${API_URL}/clientes/" | python -m json.tool 2>/dev/null || echo "Nenhum cliente"
echo ""

echo "2. Listando produtos:"
curl -s "${API_URL}/produtos/" | python -m json.tool 2>/dev/null || echo "Nenhum produto"
echo ""

echo "3. Criando um novo cliente:"
curl -s -X POST "${API_URL}/clientes/" \
  -H "Content-Type: application/json" \
  -d '{"nome": "João Silva", "email": "joao@example.com", "telefone": "11999999999"}' | python -m json.tool 2>/dev/null
echo ""

echo "4. Criando um novo produto:"
curl -s -X POST "${API_URL}/produtos/" \
  -H "Content-Type: application/json" \
  -d '{"nome": "Notebook", "preco": 3500.00, "descricao": "Notebook Dell", "quantidade": 10}' | python -m json.tool 2>/dev/null
echo ""

echo "5. Acessando ação customizada - Produtos em estoque:"
curl -s "${API_URL}/produtos/em_estoque/" | python -m json.tool 2>/dev/null || echo "Nenhum produto em estoque"
echo ""

echo "Testes finalizados!"
