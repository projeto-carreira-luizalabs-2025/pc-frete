
# 🚚 Regras de Frete (pc-frete)

Este documento tem como finalidade definir como o frete será calculado, representado e aplicado no projeto, considerando diferentes variáveis como valor da compra, localização do cliente, modalidade de envio, campanhas promocionais e políticas de frete grátis.

---

## 📦 Cálculo do Frete

O valor do frete será calculado dinamicamente com base nos seguintes fatores:

- CEP de destino.  
- Peso e dimensões dos produtos.  
- Valor total da compra.  
- Tipo de entrega selecionada (padrão, expressa, retirada, etc.).  
- Promoções vigentes ou regras específicas de frete grátis.  
- O cálculo poderá ser feito via integração com transportadoras, tabelas internas ou APIs externas de logística.

---

## 🚛 Modalidades de Entrega

- **Entrega Padrão:** Mais econômica, com prazos mais longos.  
- **Entrega Expressa:** Mais rápida, com valor mais alto.  
- **Retirada em Loja ou Ponto Físico:** Gratuito.  
- **Entrega Agendada:** Permite escolher a data e horário da entrega.

---

## 🆓 Frete Grátis

### 📌 Por Valor de Compra

Compras acima de R$ 100,00 terão frete gratuito (valor dos produtos, sem considerar o frete).

**Exemplos:**

- Carrinho com R$ 99,90 → Frete será cobrado.  
- Carrinho com R$ 100,00 → Frete grátis.

### 🎉 Por Promoção ou Data Especial

Durante datas específicas como Black Friday, Semana do Consumidor, etc.  
Pode ser aplicado a todos os pedidos ou com condições (ex: acima de determinado valor).

### 🌍 Por Região

Frete grátis para regiões estratégicas (ex: Sudeste) e capitais.

### 🛒 Por Categoria

Produtos de categorias específicas poderão ter frete gratuito (ex: livros, eletrodomésticos leves).

### 🧑‍💼 Por Vendedor

Vendedores podem optar por oferecer frete grátis para aumentar a atratividade da oferta.

---

## 💸 Custo do Frete para o Vendedor

O valor do frete pode ser:

- Totalmente pago pelo cliente.  
- Subsidiado (parcialmente pelo vendedor, parcialmente pelo cliente).  
- Totalmente absorvido pelo vendedor (frete grátis).

> O custo logístico será considerado no cálculo do lucro líquido da venda.

---

## 🛡 Regras de Proteção ao Vendedor

Vendedores poderão configurar:

- Frete mínimo obrigatório (ex: não aceitar entregas com valor de frete abaixo de R$ 10,00).  
- Regiões onde não desejam vender.  
- Regras de SLA logístico: prazos de postagem, cancelamento automático por não envio, etc.

---

## 👀 Exibição para o Cliente

O cliente poderá simular o frete antes da finalização da compra, informando o CEP.

A interface deverá mostrar:

- Valor de frete por tipo de entrega.  
- Prazo estimado.  
- Avisos de frete grátis quando aplicável  .
- Combos promocionais como: “Compre mais R$ X e ganhe frete grátis”.

---

## 🧮 Fórmulas de Cálculo

Caso o frete seja calculado com base em regras próprias e não via API:

```js
frete = valorBasePorRegiao + (peso * custoPorKg) + taxaFixa
```

Ou com lógica de faixas:

```pseudo
SE valorTotalCompra >= 100 → frete = 0
SENÃO SE região == "Sudeste" E valorTotalCompra >= 80 → frete = 0
SENÃO → frete = tabelaBase
```

---

## 📊 Benchmark - Análise de Mercado

Observações sobre grandes players (Mercado Livre, Amazon, Magalu):

- Simulação de frete baseada em CEP antes da compra.  
- Frete Grátis com destaque visual (faixa ou selo).  
- Regras claras e muitas vezes vinculadas a programas de fidelidade (ex: Amazon Prime).  
- Políticas de devolução gratuitas muitas vezes vinculadas ao custo do frete.
