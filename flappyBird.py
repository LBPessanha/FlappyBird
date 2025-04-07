import pygame
import os
import random
import sys # <<< MUDANÇA: Importado para usar sys.exit() para fechar o programa

TELA_LARGURA = 500
TELA_ALTURA = 800

# <<< MUDANÇA: Adicionado try-except para carregar imagens e dar feedback se falhar >>>
try:
    IMAGEM_TUBO = pygame.transform.scale2x(pygame.image.load("imgs/pipe.png"))
    IMAGEM_CHAO = pygame.transform.scale2x(pygame.image.load("imgs/base.png"))
    IMAGEM_BACKGROUND = pygame.transform.scale2x(pygame.image.load("imgs/bg.png"))
    IMAGENS_PASSARO = [
        pygame.transform.scale2x(pygame.image.load("imgs/bird1.png")),
        pygame.transform.scale2x(pygame.image.load("imgs/bird2.png")),
        pygame.transform.scale2x(pygame.image.load("imgs/bird3.png")),
]
except pygame.error as e:
    print(f"Erro ao carregar imagens: {e}")
    print("Certifique-se que a pasta 'imgs' existe no mesmo diretório do script e contém os arquivos:")
    print("pipe.png, base.png, bg.png, bird1.png, bird2.png, bird3.png")
    sys.exit()
# <<< FIM DA MUDANÇA >>>

pygame.font.init()
FONTE_PONTOS = pygame.font.SysFont("arial", 50)
FONTE_CONTAGEM = pygame.font.SysFont("arial", 100)
# <<< MUDANÇA: Adicionadas fontes para a tela de Game Over >>>
FONTE_GAMEOVER = pygame.font.SysFont("arial", 80)
FONTE_OPCOES = pygame.font.SysFont("arial", 30)
# <<< FIM DA MUDANÇA >>>

class Passaro:
    IMGS = IMAGENS_PASSARO
    # Animações da rotação
    ROTACAO_MAXIMA = 25
    VELOCIDADE_ROTACAO = 20
    TEMPO_ANIMACAO = 5

    def __init__(
        self,
        x,
        y,
    ):
        self.x = x
        self.y = y
        self.angulo = 0
        self.velocidade = 0
        self.altura = self.y
        self.tempo = 0
        self.contagem_imagem = 0
        self.imagem = self.IMGS[0]

    def pular(self):
        self.velocidade = -10.5
        self.tempo = 0
        self.altura = self.y

    def mover(self):
        # Calcular o deslocamento
        self.tempo += 1
        deslocamento = 1.5 * (self.tempo**2) + self.velocidade * self.tempo

        # Restringir o deslocamento
        if deslocamento > 16:
            deslocamento = 16
        elif deslocamento < 0:
            deslocamento -= 2

        self.y += deslocamento

        # O ángulo do passaro
        if deslocamento < 0 or self.y < (self.altura + 50):
            if self.angulo < self.ROTACAO_MAXIMA:
                # <<< MUDANÇA SUTIL: Ajuste na inclinação ao subir >>>
                #self.angulo = self.ROTACAO_MAXIMA
                self.angulo = min(self.angulo + self.VELOCIDADE_ROTACAO / 2, self.ROTACAO_MAXIMA)
        else:
            if self.angulo > -90:
                self.angulo -= self.VELOCIDADE_ROTACAO

    def desenhar(self, tela):
        # definir qual imagem do pássaro vai usar
        self.contagem_imagem += 1

        if self.contagem_imagem < self.TEMPO_ANIMACAO:
            self.imagem = self.IMGS[0]
        elif self.contagem_imagem < self.TEMPO_ANIMACAO * 2:
            self.imagem = self.IMGS[1]
        elif self.contagem_imagem < self.TEMPO_ANIMACAO * 3:
            self.imagem = self.IMGS[2]
        elif self.contagem_imagem < self.TEMPO_ANIMACAO * 4:
            self.imagem = self.IMGS[1]
        elif self.contagem_imagem >= self.TEMPO_ANIMACAO * 4 + 1:
            self.imagem = self.IMGS[0]
            self.contagem_imagem = 0

        # se o pássaro tiver caindo eu não vou bater asa
        if self.angulo <= -80:
            self.imagem = self.IMGS[1]
            self.contagem_imagem = self.TEMPO_ANIMACAO * 2

        # desenhar a imagem
        imagem_rotacionada = pygame.transform.rotate(self.imagem, self.angulo)
        pos_centro_imagem = self.imagem.get_rect(topleft=(self.x, self.y)).center
        retangulo = imagem_rotacionada.get_rect(center=pos_centro_imagem)
        tela.blit(imagem_rotacionada, retangulo.topleft)

    def get_mask(self):
        # <<< MUDANÇA: Corrigido para usar a imagem rotacionada na máscara (melhora colisão) >>>
        #return pygame.mask.from_surface(self.imagem)
        imagem_rotacionada = pygame.transform.rotate(self.imagem, self.angulo)
        return pygame.mask.from_surface(imagem_rotacionada)
        # <<< FIM DA MUDANÇA >>>


class Tubo:
    DISTANCIA = 200
    VELOCIDADE = 5

    def __init__(self, x):
        self.x = x
        self.altura = 0
        self.pos_topo = 0
        self.pos_base = 0
        self.TUBO_TOPO = pygame.transform.flip(IMAGEM_TUBO, False, True)
        self.TUBO_BASE = IMAGEM_TUBO
        self.passou = False
        self.definir_altura()

    def definir_altura(self):
        self.altura = random.randrange(50, 450)
        self.pos_topo = self.altura - self.TUBO_TOPO.get_height()
        self.pos_base = self.altura + self.DISTANCIA

    def mover(self):
        self.x -= self.VELOCIDADE

    def desenhar(self, tela):
        tela.blit(self.TUBO_TOPO, (self.x, self.pos_topo))
        tela.blit(self.TUBO_BASE, (self.x, self.pos_base))

    def colidir(self, passaro):
        passaro_mask = passaro.get_mask()
        topo_mask = pygame.mask.from_surface(self.TUBO_TOPO)
        base_mask = pygame.mask.from_surface(self.TUBO_BASE)

        # <<< MUDANÇA: Convertido para int para a função overlap (evita warnings/erros) >>>
        offset_topo = (int(self.x - passaro.x), int(self.pos_topo - round(passaro.y)))
        offset_base = (int(self.x - passaro.x), int(self.pos_base - round(passaro.y)))

        colidiu_topo = passaro_mask.overlap(topo_mask, offset_topo)
        colidiu_base =passaro_mask.overlap(base_mask, offset_base)

        if colidiu_topo or colidiu_base:
           return True
        else:
            return False
        # <<< FIM DA MUDANÇA >>>

        #distancia_topo = (self.x - passaro.x, self.pos_topo - round(passaro.y))
        #distancia_base = (self.x - passaro.x, self.pos_base - round(passaro.y))

        #topo_ponto = passaro_mask.overlap(base_mask, distancia_topo)
        #base_ponto = passaro_mask.overlap(base_mask, distancia_base)

        #if base_ponto or topo_ponto:
         #   return True
        #else:
        #    return False


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


def desenhar_tela(tela, passaros, tubos, chao, pontos, contagem=None):
    tela.blit(IMAGEM_BACKGROUND, (0, 0))
    
    # <<< MUDANÇA: Ordem de desenho ajustada (chão antes do pássaro) >>>
    for tubo in tubos:
        tubo.desenhar(tela)
    
    chao.desenhar(tela)

    for passaro in passaros:
        passaro.desenhar(tela)

    # <<< FIM DA MUDANÇA >>>

    #for passaro in passaros:
    #    passaro.desenhar(tela)
    #for tubo in tubos:
    #    tubo.desenhar(tela)

    texto = FONTE_PONTOS.render(f"Pontuação: {pontos}", 1, (255, 255, 255))
    tela.blit(texto, (TELA_LARGURA - 10 - texto.get_width(), 10))

    #chao.desenhar(tela)
    # <<< MUDANÇA: Lógica para exibir a contagem inicial >>>
    if contagem is not None and contagem > 0:
        texto_contagem = FONTE_CONTAGEM.render(str(contagem), 1, (255, 255, 255))
        tela.blit(
            texto_contagem,
            (TELA_LARGURA // 2 - texto_contagem.get_width() // 2, TELA_ALTURA // 2 - texto_contagem.get_height() // 2 - 50),
        )
    # <<< FIM DA MUDANÇA >>>

    #if contagem:
    #    texto_contagem = FONTE_CONTAGEM.render(str(contagem), 1, (255, 255, 255))
    #    tela.blit(
    #        texto_contagem,
    #        (TELA_LARGURA // 2 - texto_contagem.get_width() // 2, TELA_ALTURA // 2 - texto_contagem.get_height() // 2),
    #    )
        
    pygame.display.update()

# <<< MUDANÇA: Adicionada a função inteira para a tela de Game Over >>>
def tela_game_over(tela, pontos, chao, relogio):
    tela.blit(IMAGEM_BACKGROUND, (0, 0))
    chao.desenhar(tela) # Desenha o chão primeiro

    # Texto "Game Over"
    texto_game_over = FONTE_GAMEOVER.render("Game Over", 1, (255, 0, 0)) # Vermelho para destaque
    pos_go_x = TELA_LARGURA // 2 - texto_game_over.get_width() // 2
    pos_go_y = TELA_ALTURA // 2 - texto_game_over.get_height() // 2 - 100 # Posição um pouco acima do centro
    tela.blit(texto_game_over, (pos_go_x, pos_go_y)) # Desenha "Game Over"

    # Texto "Pontuação Final" - Definido *antes* de usar
    # Use f-string para incluir a pontuação corretamente
    texto_pontos_final = FONTE_OPCOES.render(f"Pontuação Final: {pontos}", 1, (255, 255, 255))
    pos_pf_x = TELA_LARGURA // 2 - texto_pontos_final.get_width() // 2
    pos_pf_y = pos_go_y + texto_game_over.get_height() + 20 # Posição abaixo de "Game Over"
    # Desenha o texto da pontuação final na posição correta
    tela.blit(texto_pontos_final, (pos_pf_x, pos_pf_y))

    # Texto "Reiniciar"
    texto_reiniciar = FONTE_OPCOES.render("Pressione ESPAÇO para Reiniciar", 1, (255, 255, 255))
    pos_r_x = TELA_LARGURA // 2 - texto_reiniciar.get_width() // 2
    pos_r_y = pos_pf_y + texto_pontos_final.get_height() + 50 # Posição abaixo da pontuação
    tela.blit(texto_reiniciar, (pos_r_x, pos_r_y))

    # Texto "Sair"
    texto_sair = FONTE_OPCOES.render("Pressione ESC para Sair", 1, (255, 255, 255))
    pos_s_x = TELA_LARGURA // 2 - texto_sair.get_width() // 2
    pos_s_y = pos_r_y + texto_reiniciar.get_height() + 20 # Posição abaixo de reiniciar
    tela.blit(texto_sair, (pos_s_x, pos_s_y))

    pygame.display.update() # Atualiza a tela uma vez com todos os elementos

    # Loop para esperar a entrada do jogador
    while True:
        relogio.tick(30) # Limita o FPS mesmo na tela de game over
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    return "REINICIAR" # Retorna a escolha
                if evento.key == pygame.K_ESCAPE:
                    return "SAIR" # Retorna a escolha
# <<< FIM DA MUDANÇA >>>

def main():
    passaros = [Passaro(230, 350)]
    chao = Chao(730)
    tubos = [Tubo(700)]
    tela = pygame.display.set_mode((TELA_LARGURA, TELA_ALTURA))
    
    # <<< MUDANÇA: Adicionado título da janela >>>
    pygame.display.set_caption("Flappy Bird Clone")    
    # <<< FIM DA MUDANÇA >>>

    pontos = 0
    relogio = pygame.time.Clock()

    # <<< MUDANÇA: Adicionada flag para controlar o estado ativo do jogo >>>
    jogo_ativo = False
    # <<< FIM DA MUDANÇA >>>

    # <<< MUDANÇA: Adicionado loop de contagem regressiva inicial >>>
    contagem = 3
    while contagem > 0:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        desenhar_tela(tela, passaros, tubos, chao, pontos, contagem)
        relogio.tick(1)
        contagem -= 1
    # Temporizador de 5 segundos
    #contagem = 5
    #while contagem > 0:
    #    relogio.tick(1) # 1 segundo por itereção
    #    desenhar_tela(tela, passaros, tubos, chao, pontos, contagem)
    #    contagem -=1
    
    # <<< FIM DA MUDANÇA >>>

    # <<< MUDANÇA: Inicia o jogo como ativo após a contagem >>>
    jogo_ativo = True
    # <<< FIM DA MUDANÇA >>>

    rodando = True
    while rodando:
        relogio.tick(30)

        # Interação com o usuário
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False
                pygame.quit()
                quit()
            if evento.type == pygame.KEYDOWN:
                # <<< MUDANÇA: Só permite pular se o jogo estiver ativo >>>
                if evento.key == pygame.K_SPACE and jogo_ativo: #inclusaõ do "and jogo_ativo"
                    for passaro in passaros:
                        passaro.pular()
                # <<< FIM DA MUDANÇA >>>
                #Opcional: Sair com ESC a qualquer momento
                if evento.key == pygame.K_ESCAPE:
                    rodando = False

        # Mover as coisas
        # <<< MUDANÇA: Toda a lógica de movimento e colisão agora só roda se jogo_ativo == True >>>
        if jogo_ativo:
            for passaro in passaros:
                passaro.mover()
            chao.mover()

            adicionar_tubo = False
            remover_tubos = []
            for tubo in tubos:
                for i, passaro in enumerate(passaros):
                    # <<< MUDANÇA: Se colidir, para o jogo e remove o pássaro >>>
                    if tubo.colidir(passaro):
                        jogo_ativo = False #Para a lógico do jogo
                        # Certifica-se que o índice é válido antes de remover
                        if i < len(passaros):
                            passaros.pop(i)
                        break # Pára de checar outros pássaros contra este tubo
                    # <<< FIM DA MUDANÇA >>>
                        #passaros.pop(i)
                    
                    # <<< MUDANÇA: Verifica passagem completa pelo cano >>>
                    if not tubo.passou and passaro.x > tubo.x + tubo.TUBO_TOPO.get_width(): # acrescentou "+ tubo.TUBO_TOPO.get.widht()"
                        tubo.passou = True
                        adicionar_tubo = True
                        # <<< FIM DA MUDANÇA >>>
                
                # <<< MUDANÇA: Só move o tubo e verifica remoção se o jogo ainda estiver ativo >>>
                if jogo_ativo: # Inserido 
                    tubo.mover()
                    if tubo.x + tubo.TUBO_TOPO.get_width() < 0:
                        remover_tubos.append(tubo)
                # <<< FIM DA MUDANÇA >>>
            
            # <<< MUDANÇA: Só adiciona tubo e pontos se o jogo estiver ativo >>>
            if adicionar_tubo and jogo_ativo: #inclusão do "and jogo_ativo"
                pontos += 1
                tubos.append(Tubo(TELA_LARGURA + 50)) # saiu o valor de "600" e entrou "TELA_LARGURA + 50"
             # <<< FIM DA MUDANÇA >>>

            for tubo in remover_tubos:
                # <<< MUDANÇA: Checa se o tubo ainda está na lista antes de remover >>>
                if tubo in tubos: #inclusão dessa linha 
                    tubos.remove(tubo)
                # <<< FIM DA MUDANÇA >>>

            # <<< MUDANÇA: Verifica colisão com chão/teto e para o jogo >>>
            for i, passaro in enumerate(passaros):
                if (passaro.y + passaro.imagem.get_height()) >= chao.y or passaro.y < 0: #inclusão do sinal "="
                    jogo_ativo = False # inclusão dessa linha Para lógica do jogo
                    # Certifica-se que o índice é válido antes de remover
                    if i < len(passaros): #inclusão dessa linha
                        passaros.pop(i)
                    break # inclusão dessa linha - Pára de checar outros pássaros
            # <<< FIM DA MUDANÇA >>>
            # <<< FIM DO BLOCO if jogo_ativo: >>>

            # Desenha sempre, mesmo no frame da colisão antes de mostrar Game Over
            desenhar_tela(tela, passaros, tubos, chao, pontos)
            
            # <<< MUDANÇA: Bloco inteiro para tratar o Game Over e as opções >>>
            # Verifica se o jogo parou E não há mais pássaros na tela
            if not jogo_ativo and not passaros:
                escolha = tela_game_over(tela, pontos, chao, relogio) # Mostra a tela e pega a escolha

                if escolha == "REINICIAR":
                   # Reinicia as variáveis do jogo
                   passaros = [Passaro(230, 350)]
                   tubos = [Tubo(700)]
                   pontos = 0
                   jogo_ativo = False # Mantém inativo para a contagem

                   # Reinicia a contagem regressiva
                   contagem = 3
                   while contagem > 0:
                       for evento in pygame.event.get():
                           if evento.type == pygame.QUIT:
                               pygame.quit()
                               sys.exit()
                       desenhar_tela(tela, passaros, tubos, chao, pontos, contagem)
                       relogio.tick(1)
                       contagem -= 1
                   jogo_ativo = True # Ativa o jogo novamente
                
                elif escolha == "SAIR":
                    rodando = False # Termina o loop principal do jogo
        # <<< FIM DA MUDANÇA >>>

    # <<< MUDANÇA: Chamadas finais para encerrar corretamente >>>
    pygame.quit()
    sys.exit()
    # <<< FIM DA MUDANÇA >>>


            #if not passaros:
            #    reinicar_jogo(passaros, tubos, chao, pontos)

            #desenhar_tela(tela, passaros, tubos, chao, pontos)


# def reinicar_jogo(passaros, tubos, chao, pontos):
#    passaros.clear()
#    tubos.clear()
#    passaros.append(Passaro(230, 350))
#    tubos.append(Tubo(700))
#    chao.y = 730
#    pontos = 0


if __name__ == "__main__":
    main()
