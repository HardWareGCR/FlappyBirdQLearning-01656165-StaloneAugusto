# Flappy Bird com Q-Learning

**Autor:** Stalone Augusto  
**Matrícula:** 01656165  

<p align="center">
  <img src="https://imgur.com/example.png" alt="Demonstração do Jogo" width="500">
</p>

## 🎯 Visão Geral

Este projeto implementa o clássico jogo Flappy Bird utilizando aprendizado por reforço com Q-Learning. O pássaro autônomo aprende a jogar através de tentativa e erro, recebendo recompensas por ações positivas e penalidades por colisões.

## 🛠️ Tecnologias Utilizadas

- Python 3.8+
- Pygame (renderização gráfica)
- NumPy (cálculos numéricos)
- Matplotlib (visualização de dados)
- Collections (estruturas de dados)

## 📦 Instalação

1. Clone o repositório:
```bash
git clone https://github.com/seu-usuario/flappy-bird-qlearning.git
cd flappy-bird-qlearning
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

## 🚀 Execução

Execute o jogo com:
```bash
python flappy_bird_qlearning.py
```

**Controles:**
- `Espaço`: Pular (modo manual)
- `ESC`: Sair do jogo

## 🧠 Algoritmo de Q-Learning

### Equação Principal
\[ Q(s,a) ← Q(s,a) + α[r + γ \max_{a'}Q(s',a') - Q(s,a)] \]

**Parâmetros:**
- Taxa de aprendizado (α): 0.2
- Fator de desconto (γ): 0.95
- ε inicial: 0.3 (decai para 0.01)

### Sistema de Recompensas
| Ação | Recompensa |
|------|------------|
| Passar por um cano | +100 |
| Bater recorde | +200 |
| Sobreviver (por frame) | +0.5 |
| Distância do centro | -0.1 × distância |
| Colisão | -1000 |

## 📊 Métricas de Desempenho

O sistema gera automaticamente gráficos mostrando:
1. Evolução das recompensas
2. Progresso da pontuação
3. Taxa de exploração (ε)

<p align="center">
  <img src="https://imgur.com/metrics.png" alt="Gráficos de Desempenho" width="600">
</p>

## 📌 Dificuldades e Soluções

| Problema | Solução Implementada |
|----------|----------------------|
| Pássaro só subia | Ajuste da física e recompensas |
| Aprendizado lento | Melhoria na representação de estado |
| Exploração excessiva | Decaimento adaptativo de ε |

## 📜 Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.
