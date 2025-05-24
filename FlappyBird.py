import pygame
import os
import random
import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict

# Configurações do jogo
LARGURA_TELA = 500
ALTURA_TELA = 800

# Carregar imagens
IMAGEM_CANO = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'pipe.png')))
IMAGEM_CHAO = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'base.png')))
IMAGEM_FUNDO = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bg.png')))
IMAGENS_PASSARO = [
    pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bird1.png'))),
    pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bird2.png'))),
    pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bird3.png'))),
]

pygame.font.init()
FONTE_PONTUACAO = pygame.font.SysFont('arial', 40)

class AgenteQLearning:
    def __init__(self, acoes):
        self.acoes = acoes  # não_pular, pular
        self.taxa_aprendizado = 0.2
        self.fator_desconto = 0.95
        self.epsilon = 0.3  # Taxa de exploração inicial
        self.tabela_q = defaultdict(lambda: [0.0, 0.0])
        self.recompensas = []
        self.epsilons = []
        self.pontuacoes = []
    
    def obter_estado(self, passaro, canos):
        """Transforma o estado do jogo em uma representação discreta"""
        if len(canos) > 0:
            cano = canos[0]
            distancia_x = cano.x - passaro.x
            distancia_centro_y = passaro.y - (cano.altura + cano.DISTANCIA/2)
        else:
            distancia_x = LARGURA_TELA
            distancia_centro_y = 0
        
        # Discretização dos valores
        distancia_x = min(max(-50, distancia_x), 500) // 50
        distancia_centro_y = min(max(-150, distancia_centro_y), 150) // 25
        velocidade = min(max(-15, passaro.velocidade), 15) // 5
        
        return (distancia_x, distancia_centro_y, velocidade)
    
    def escolher_acao(self, estado):
        """Seleciona ação usando política epsilon-greedy"""
        if np.random.rand() < self.epsilon:
            return random.choice(self.acoes)  
        else:
            return np.argmax(self.tabela_q[estado])  
    
    def aprender(self, estado, acao, recompensa, proximo_estado):
        """Atualiza a tabela Q usando o algoritmo Q-learning"""
        q_atual = self.tabela_q[estado][acao]
        melhor_q_proximo = np.max(self.tabela_q[proximo_estado])
        
        # Equação do Q-learning
        novo_q = q_atual + self.taxa_aprendizado * (recompensa + self.fator_desconto * melhor_q_proximo - q_atual)
        self.tabela_q[estado][acao] = novo_q
        
        # Reduz gradualmente a taxa de exploração
        self.epsilon = max(0.01, self.epsilon * 0.9995)
    
    def registrar_metricas(self, recompensa, pontuacao, epsilon):
        self.recompensas.append(recompensa)
        self.pontuacoes.append(pontuacao)
        self.epsilons.append(epsilon)
    
    def plotar_metricas(self):
        """Gera gráficos de desempenho"""
        plt.figure(figsize=(12, 8))
        
        plt.subplot(3, 1, 1)
        plt.plot(self.recompensas)
        plt.title('Recompensas por Episódio')
        plt.ylabel('Recompensa')
        
        plt.subplot(3, 1, 2)
        plt.plot(self.pontuacoes)
        plt.title('Pontuação por Episódio')
        plt.ylabel('Pontos')
        
        plt.subplot(3, 1, 3)
        plt.plot(self.epsilons)
        plt.title('Taxa de Exploração (Epsilon)')
        plt.ylabel('Epsilon')
        plt.xlabel('Episódios')
        
        plt.tight_layout()
        plt.show()

class Passaro:
    IMAGENS = IMAGENS_PASSARO
    ROTACAO_MAXIMA = 25
    VELOCIDADE_ROTACAO = 20
    TEMPO_ANIMACAO = 5
    GRAVIDADE = 1.5
    VELOCIDADE_PULO = -10

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.angulo = 0
        self.velocidade = 0
        self.altura = self.y
        self.tempo = 0
        self.contador_imagem = 0
        self.imagem = self.IMAGENS[0]

    def pular(self):
        self.velocidade = self.VELOCIDADE_PULO
        self.tempo = 0
        self.altura = self.y

    def mover(self):
        # Cálculo do movimento com física realista
        self.tempo += 1
        deslocamento = self.velocidade * self.tempo + self.GRAVIDADE * (self.tempo**2)
        
        # Limites de velocidade
        if deslocamento > 16:  
            deslocamento = 16
        elif deslocamento < -10:  
            deslocamento = -10
            
        self.y += deslocamento

        # Atualizar ângulo de rotação
        if deslocamento < 0 or self.y < (self.altura + 50):
            if self.angulo < self.ROTACAO_MAXIMA:
                self.angulo = self.ROTACAO_MAXIMA
        else:
            if self.angulo > -90:
                self.angulo -= self.VELOCIDADE_ROTACAO

    def desenhar(self, tela):
        self.contador_imagem += 1

        # Animação do bater de asas
        if self.contador_imagem < self.TEMPO_ANIMACAO:
            self.imagem = self.IMAGENS[0]
        elif self.contador_imagem < self.TEMPO_ANIMACAO*2:
            self.imagem = self.IMAGENS[1]
        elif self.contador_imagem < self.TEMPO_ANIMACAO*3:
            self.imagem = self.IMAGENS[2]
        elif self.contador_imagem < self.TEMPO_ANIMACAO*4:
            self.imagem = self.IMAGENS[1]
        elif self.contador_imagem >= self.TEMPO_ANIMACAO*4 + 1:
            self.imagem = self.IMAGENS[0]
            self.contador_imagem = 0

        # Não animar se estiver caindo
        if self.angulo <= -80:
            self.imagem = self.IMAGENS[1]
            self.contador_imagem = self.TEMPO_ANIMACAO*2

        # Desenhar o pássaro com rotação
        imagem_rotacionada = pygame.transform.rotate(self.imagem, self.angulo)
        posicao_centro = self.imagem.get_rect(topleft=(self.x, self.y)).center
        retangulo = imagem_rotacionada.get_rect(center=posicao_centro)
        tela.blit(imagem_rotacionada, retangulo.topleft)

    def obter_mascara(self):
        return pygame.mask.from_surface(self.imagem)

class Cano:
    DISTANCIA = 200
    VELOCIDADE = 5

    def __init__(self, x):
        self.x = x
        self.altura = 0
        self.pos_topo = 0
        self.pos_base = 0
        self.CANO_TOPO = pygame.transform.flip(IMAGEM_CANO, False, True)
        self.CANO_BASE = IMAGEM_CANO
        self.passou = False
        self.definir_altura()

    def definir_altura(self):
        self.altura = random.randrange(50, 450)
        self.pos_topo = self.altura - self.CANO_TOPO.get_height()
        self.pos_base = self.altura + self.DISTANCIA

    def mover(self):
        self.x -= self.VELOCIDADE

    def desenhar(self, tela):
        tela.blit(self.CANO_TOPO, (self.x, self.pos_topo))
        tela.blit(self.CANO_BASE, (self.x, self.pos_base))

    def colidir(self, passaro):
        mascara_passaro = passaro.obter_mascara()
        mascara_topo = pygame.mask.from_surface(self.CANO_TOPO)
        mascara_base = pygame.mask.from_surface(self.CANO_BASE)

        distancia_topo = (self.x - passaro.x, self.pos_topo - round(passaro.y))
        distancia_base = (self.x - passaro.x, self.pos_base - round(passaro.y))

        colisao_topo = mascara_passaro.overlap(mascara_topo, distancia_topo)
        colisao_base = mascara_passaro.overlap(mascara_base, distancia_base)

        return colisao_base or colisao_topo

class Chao:
    VELOCIDADE = 5
    LARGURA = IMAGEM_CHAO.get_width()
    IMAGEM = IMAGEM_CHAO

    def __init__(self, y):
        self.y = y
        self.x1 = 0
        self.x2 = self.LARGURA

    def mover(self):
        self.x1 -= self.VELOCIDADE
        self.x2 -= self.VELOCIDADE

        if self.x1 + self.LARGURA < 0:
            self.x1 = self.x2 + self.LARGURA
        if self.x2 + self.LARGURA < 0:
            self.x2 = self.x1 + self.LARGURA

    def desenhar(self, tela):
        tela.blit(self.IMAGEM, (self.x1, self.y))
        tela.blit(self.IMAGEM, (self.x2, self.y))

def desenhar_tela(tela, passaros, canos, chao, pontos, episodio, epsilon):
    tela.blit(IMAGEM_FUNDO, (0, 0))
    for passaro in passaros:
        passaro.desenhar(tela)
    for cano in canos:
        cano.desenhar(tela)

    texto_pontos = FONTE_PONTUACAO.render(f"Pontos: {pontos}", 1, (255, 255, 255))
    texto_episodio = FONTE_PONTUACAO.render(f"Episódio: {episodio}", 1, (255, 255, 255))
    texto_epsilon = FONTE_PONTUACAO.render(f"Exploração: {epsilon:.4f}", 1, (255, 255, 255))
    
    tela.blit(texto_pontos, (LARGURA_TELA - 10 - texto_pontos.get_width(), 10))
    tela.blit(texto_episodio, (10, 10))
    tela.blit(texto_epsilon, (10, 70))
    
    chao.desenhar(tela)
    pygame.display.update()

def main():
    pygame.init()
    tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
    pygame.display.set_caption("Flappy Bird com Q-Learning")
    
    agente = AgenteQLearning(acoes=[0, 1])
    episodio = 0
    max_pontos = 0
    
    while True:
        passaro = Passaro(230, 350)
        chao = Chao(730)
        canos = [Cano(700)]
        pontos = 0
        relogio = pygame.time.Clock()
        
        estado = agente.obter_estado(passaro, canos)
        
        rodando = True
        while rodando:
            relogio.tick(30)
            
            # Ação do agente
            acao = agente.escolher_acao(estado)
            if acao == 1:
                passaro.pular()
            
            # Movimentação
            passaro.mover()
            chao.mover()
            
            # Processar canos e recompensas
            adicionar_cano = False
            remover_canos = []
            recompensa = 0.5  
            
            for cano in canos:
                if cano.colidir(passaro):
                    recompensa = -1000  
                    rodando = False
                    break
                
                if not cano.passou and passaro.x > cano.x:
                    cano.passou = True
                    adicionar_cano = True
                    pontos += 1
                    recompensa += 100  
                    if pontos > max_pontos:
                        max_pontos = pontos
                        recompensa += 100  
                
                cano.mover()
                if cano.x + cano.CANO_TOPO.get_width() < 0:
                    remover_canos.append(cano)
            
            if adicionar_cano:
                canos.append(Cano(600))
            
            for cano in remover_canos:
                canos.remove(cano)
            
            # Verificar colisão com chão ou teto
            if (passaro.y + passaro.imagem.get_height()) > chao.y or passaro.y < 0:
                recompensa = -1000
                rodando = False
            
            if rodando:
                # Atualizar Q-table
                proximo_estado = agente.obter_estado(passaro, canos)
                agente.aprender(estado, acao, recompensa, proximo_estado)
                estado = proximo_estado
            
            # Renderizar
            desenhar_tela(tela, [passaro], canos, chao, pontos, episodio, agente.epsilon)
            
            # Eventos
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    agente.plotar_metricas()
                    pygame.quit()
                    return
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_ESCAPE:
                        agente.plotar_metricas()
                        pygame.quit()
                        return
        
        # Registrar métricas
        agente.registrar_metricas(recompensa, pontos, agente.epsilon)
        episodio += 1
        print(f"Episódio: {episodio}, Pontos: {pontos}, Máximo: {max_pontos}, Epsilon: {agente.epsilon:.4f}")
        
        # Mostrar métricas periodicamente
        if episodio % 100 == 0:
            agente.plotar_metricas()

if __name__ == '__main__':
    main()