# Zumbi_Sobrevivente - Aprendizado por Reforço em um Mundo Pós-Apocalíptico

**Autor:** Stalone Augusto  
**Matrícula:** 01656165

## Visão Geral

Este projeto implementa um agente de aprendizado por reforço (usando Q-Learning) que deve aprender a sobreviver em um mundo pós-apocalíptico cheio de zumbis. O agente precisa:

1. Coletar recursos para sobreviver
2. Evitar zumbis que reduzem sua vida
3. Evitar armadilhas no ambiente
4. Maximizar seu tempo de sobrevivência

## Tecnologias e Bibliotecas Utilizadas

- Python 3.8+
- NumPy: Para computação numérica e armazenamento da tabela Q
- Matplotlib: Para visualização das métricas de treinamento
- Pygame: Para renderização do ambiente (opcional)
- PyYAML: Para carregar parâmetros de configuração

## Algoritmos Aplicados

- **Q-Learning**: Algoritmo de aprendizado por reforço sem modelo
- **Política ε-greedy**: Balanceamento entre exploração e exploração
- **Decaimento de ε**: Redução gradual da taxa de exploração
- **Tabela Q**: Armazenamento das estimativas de valor ação-estado

## Fórmulas e Cálculos

### Atualização da Tabela Q

A atualização segue a equação do Q-Learning:

\[ Q(s, a) \leftarrow Q(s, a) + \alpha \cdot [r + \gamma \cdot \max_{a'} Q(s', a') - Q(s, a)] \]

Onde:
- \( \alpha \) = taxa de aprendizado (0.1)
- \( \gamma \) = fator de desconto (0.9)
- \( s \) = estado atual
- \( a \) = ação tomada
- \( r \) = recompensa recebida
- \( s' \) = próximo estado

### Decaimento de Epsilon

\[ \epsilon \leftarrow \max(\epsilon_{\text{min}}, \epsilon \cdot \text{decay}) \]

## Como Executar o Projeto

1. Clone o repositório
2. Instale as dependências:

```bash
pip install -r requirements.txt