import pygame
import random

from pygame.locals import*

# Inicializa o pygame
pygame.init()
pygame.mixer.init()

# Configurações da tela
LARGURA = 800
ALTURA = 600
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("SnowFalling")

som_ganhar = pygame.mixer.Sound("ganhar.mp3")
som_perder = pygame.mixer.Sound("perder.mp3")
som_next_level = pygame.mixer.Sound("next-level.mp3")
som_bonus = pygame.mixer.Sound("bonus.mp3")
musica_game = "musica-game.mp3"

# Loop principal do jogo
class Player(pygame.sprite.Sprite):
    def __init__(self, name):
        super(Player, self).__init__()
        self.name = name
        self.alive =  True
        self.position = pygame.math.Vector2(LARGURA // 2, ALTURA - 200)
        self.speed = 5
        
        self.deslizamento_x = 0
        self.deslizamento_max = 5
        self.aceleracao = 3
        self.friccao = 0.99
        
        self.image_esquerda = pygame.image.load("vovo.png")
        self.image_esquerda = pygame.transform.scale(self.image_esquerda, (100, 100))

        self.image_direita = pygame.image.load("vovo - Copia.png")
        self.image_direita = pygame.transform.scale(self.image_direita, (100, 100))

        self.image = self.image_esquerda  # imagem inicial

        
        self.rect = self.image.get_rect()
        self.rect.center = self.position

        self.impacto = False
        self.velocidade_retorno = 0
        self.position_original = self.position.y
        
    def update(self):
        Keys = pygame.key.get_pressed()
        
        if Keys[K_LEFT]:
            self.image = self.image_esquerda
            self.deslizamento_x -= self.aceleracao * 60
            self.position.x -= self.speed

        elif Keys[K_RIGHT]:
            self.image = self.image_direita
            self.deslizamento_x += self.aceleracao * 60
            self.position.x += self.speed

        else:
            self.deslizamento_x *= self.friccao
            
        # Limite o deslizamento    
        if self.deslizamento_x > self.deslizamento_max:
            self.deslizamento_x = self.deslizamento_max
            
        elif self.deslizamento_x < -self.deslizamento_max:
            self.deslizamento_x = -self.deslizamento_max
            
        self.position.x += self.deslizamento_x
        
        
        # Limite da tela    
        if self.position.x < self.rect.width // 2:
            self.position.x = self.rect.width //2
            
        elif self.position.x > LARGURA - self.rect.width // 2:
            self.position.x = LARGURA - self.rect.width //2

        #impcato do personagem com as bandeiras
        if self.impacto:
            diferenca = self.position_original - self.position.y
            velocidade_retorno = diferenca * 0.1

            if abs(diferenca) < 0.5:
                self.position.y = self.position_original
                self.impacto = False

            else:
                self.position.y += velocidade_retorno
            
        self.rect.center = self.position
        
class Background:   
    def __init__(self, speed):
        self.image = pygame.image.load("background1.png")
        self.image = pygame.transform.scale(self.image, (LARGURA, ALTURA))
        
        self.y1 = 0
        self.y2 = -ALTURA
        self.speed = speed
        
    def max_speed(self):
        self.speed += 1
        
        if self.speed > 15:
            self.speed = 15
            
    def min_speed(self):
        self.speed -= 1
        
        if self.speed <= 1:
            self.speed = 1

    def update(self):
        self.y1 += self.speed
        self.y2 += self.speed
        
        Keys = pygame.key.get_pressed()
        
        if self.y1 >= ALTURA:
            self.y1 = -ALTURA
            
        if self.y2 >= ALTURA:
            self.y2 = -ALTURA
            
        if Keys [K_UP]:
            self.max_speed()
            
        if Keys [K_DOWN]:
            self.min_speed()

    def draw(self, surface):
        surface.blit(self.image, (0, self.y1))
        surface.blit(self.image, (0, self.y2))

"""
     
class Backgroud2:
    def __init__(self, speed):
        self.image = pygame.image.load("background2.png")
        self.image = pygame.transform.scale(self.image, (LARGURA, ALTURA))
        
        self.y1 = 0
        self.y2 = -ALTURA
        self.speed = speed
        
    def max_speed(self):
        self.speed += 1 
        
        if self.speed > 20: #8
            self.speed = 20 #8
            
    def min_speed(self):
        self.speed -= 1 #0.5
        
        if self.speed <= 10: #0.5
            self.speed = 10 #0.5

    def update(self):
        self.y1 += self.speed
        self.y2 += self.speed
        
        Keys = pygame.key.get_pressed()
        
        if self.y1 >= ALTURA:
            self.y1 = -ALTURA
            
        if self.y2 >= ALTURA:
            self.y2 = -ALTURA
            
        if Keys [K_UP]:
            self.max_speed()
            
        if Keys [K_DOWN]:
            self.min_speed()

    def draw(self, surface):
        surface.blit(self.image, (0, self.y1))
        surface.blit(self.image, (0, self.y2))

"""

class Avalanche: 
    def __init__(self):
        self.frames = [
            pygame.image.load("avalanche.png").convert_alpha(),
            pygame.image.load("avalanche1.png").convert_alpha()
        ]
        
        self.frames = [pygame.transform.scale(f, (LARGURA, 400)) for f in self.frames]
        
        self.index = 0
        self.timer = 0
        self.delay = 5
        
        #self.y = -200
        self.velocidade = 2

    def update(self):
        self.timer += 1
        if self.timer >= self.delay:
            self.timer = 0
            self.index = (self.index + 1) % len(self.frames)
        
    def draw(self, tela):
        tela.blit(self.frames[self.index], (0, ALTURA - 400))

class Flags(pygame.sprite.Sprite):  
    def __init__(self, x, y, background_speed, cor = "vermelha"):
        super(Flags, self).__init__()

        if cor == "azul":
            self.image = pygame.image.load("bandeiraazul.png")
        else:
            self.image = pygame.image.load("bandeira.png")
        
        self.image = pygame.transform.scale(self.image, (80, 80))
        
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = background_speed
                
    def max_speed(self):
        self.speed += 1
        
        if self.speed > 15:
            self.speed = 15
            
    def min_speed(self):
        self.speed -= 1
        
        if self.speed <= 1:
            self.speed = 1
        
    def update(self):
        self.rect.y += self.speed           
        Keys = pygame.key.get_pressed()
            
        if Keys [K_UP]:
            self.max_speed()
            
        if Keys [K_DOWN]:
            self.min_speed()
        
        if self.rect.top > ALTURA:
            self.kill()

class Pedra(pygame.sprite.Sprite):
    def __init__(self, x, y, background_speed):
        super(Pedra, self).__init__()

        self.image = pygame.image.load("pedra.png")
        self. image = pygame.transform.scale(self.image, (60, 60))

        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

        self.speed = background_speed

    def update(self):
        self.rect.y += self.speed
        Keys = pygame.key.get_pressed()

        if Keys[K_UP]:
            self.speed = min(self.speed + 1, 15)

        elif Keys[K_DOWN]:
            self.speed = max(self.speed - 1, 15)

        if self.rect.top > ALTURA:
            self.kill()

class Arvore(pygame.sprite.Sprite):
    def __init__(self, x, y, background_speed):
        super(Arvore, self).__init__()

        self.image = pygame.image.load("arvore.png")
        self. image = pygame.transform.scale(self.image, (150, 150))

        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

        self.speed = background_speed

    def update(self):
        self.rect.y += self.speed
        Keys = pygame.key.get_pressed()

        if Keys[K_UP]:
            self.speed = min(self.speed + 1, 15)

        elif Keys[K_DOWN]:
            self.speed = max(self.speed - 1, 15)

        if self.rect.top > ALTURA:
            self.kill()

class ZonaBonus(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((120,40), pygame.SRCALPHA)
        self.rect = self.image.get_rect(center = (x, y))
        self.tempo_dado = False
        self.speed = 5

    def update(self):
        self.rect.y += self.speed

        if self.rect.top > ALTURA:
            self.kill()

class Menu():
    fonte = pygame.font.SysFont("Poppins", 40)

    def desenhar_menu(texto, y, selecionado = False):
        cor_base = (229, 229, 229)
        cor_hover = (250, 250, 250)
        cor_texto = (0, 0, 0)
        sombra = (150, 150, 150)

        ret = pygame.Rect(LARGURA // 2 - 150, y, 300, 60)

        mouse_pos = pygame.mouse.get_pos()
        hover = ret.collidepoint(mouse_pos)

        pygame.draw.rect(tela, sombra, ret.move(4, 4), border_radius=15)
        pygame.draw.rect(tela, cor_hover if hover else cor_base, ret, border_radius=15)

        texto_render = Menu.fonte.render(texto, True, cor_texto)
        texto_rect = texto_render.get_rect(center = ret.center)
        tela.blit(texto_render, texto_rect)

        return ret
    
    def menu_pause():
        pausado = True

        while pausado:
            #tela.fill((255, 255, 255))

            botao_inicio = Menu.desenhar_menu("Início", 200)
            botao_recomecar = Menu.desenhar_menu("Recomeçar", 280)
            botao_sair = Menu.desenhar_menu("Sair", 360)

            pygame.display.flip()

            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    return "sair"
                
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_ESCAPE:
                        return "Continuar"

                if evento.type == pygame.MOUSEBUTTONDOWN:
                    if botao_inicio.collidepoint(evento.pos):
                        return "inicio"
                    
                    elif botao_recomecar.collidepoint(evento.pos):
                        return "recomecar"
                    
                    elif botao_sair.collidepoint(evento.pos):
                        return "sair"

def menu_principal():
    fonte_titulo = pygame.font.SysFont("Poppins", 60, bold=True)
    fonte_opcao = pygame.font.SysFont("Poppins", 36, bold=True)

    rodando_menu = True
    fundo = pygame.Surface((LARGURA, ALTURA))
    fundo.fill((240, 248, 255))  # fundo azul claro, tipo neve

    pygame.mixer.music.load(musica_game)
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)

    while rodando_menu:
        tela.blit(fundo, (0, 0))

        titulo = fonte_titulo.render("SnowFalling", True, (0, 0, 0))
        tela.blit(titulo, (LARGURA // 2 - titulo.get_width() // 2, 100))

        botao_iniciar = pygame.Rect(LARGURA // 2 - 100, 250, 200, 60)
        botao_sair = pygame.Rect(LARGURA // 2 - 100, 340, 200, 60)

        pygame.draw.rect(tela, (200, 200, 200), botao_iniciar, border_radius=10)
        pygame.draw.rect(tela, (200, 200, 200), botao_sair, border_radius=10)

        iniciar_texto = fonte_opcao.render("Iniciar", True, (0, 0, 0))
        sair_texto = fonte_opcao.render("Sair", True, (0, 0, 0))

        tela.blit(iniciar_texto, iniciar_texto.get_rect(center=botao_iniciar.center))
        tela.blit(sair_texto, sair_texto.get_rect(center=botao_sair.center))

        pygame.display.flip()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()

            if evento.type == pygame.MOUSEBUTTONDOWN:
                if botao_iniciar.collidepoint(evento.pos):
                    rodando_menu = False
                elif botao_sair.collidepoint(evento.pos):
                    pygame.quit()
                    exit()

def fase_1():
    rodando = True
    clock = pygame.time.Clock()
    
    player = Player("Vovô")
    background = Background(1)
    #background2 = Backgroud2(1)
    avalanche = Avalanche()
    
    flags_group = pygame.sprite.Group()
    grupo = pygame.sprite.Group()
    grupo.add(player)
    
    contador_flags = 0
    tempo_entre_flags= 60

    tempo_restante = 30
    ultimo_tempo = pygame.time.get_ticks()
    tempo_expirado = False

    venceu = False
    tempo_para_vencer = 15

    slow_motion = False
    tempo_slow = 0
    duracao_slow = 500  # em milissegundos

    distancia_percorrida = 0
    distancia_total = 15000

    zona_bonus = pygame.sprite.Group()
    
    #loop principal
    while rodando:
        contador_flags +=1

        colisoes = pygame.sprite.spritecollide(player, flags_group, dokill = False)

        tempo_atual = pygame.time.get_ticks()
        delta = (tempo_atual - ultimo_tempo) // 1000

        if delta > 0:
            tempo_restante = max(0, tempo_restante - delta)
            ultimo_tempo = tempo_atual
           
        for zona in zona_bonus:
            if zona.rect.colliderect(player.rect) and not zona.tempo_dado:
                tempo_restante += 2     #Ganha 2 segundos quando passa entra as bandeiras
                zona.tempo_dado = True
                som_bonus.play()
        
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False

            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    acao = Menu.menu_pause()

                    if acao == "recomecar":
                        return fase_1()
                    
                    elif acao == "inicio":
                        return "menu"

                    elif acao == "sair":
                        return "sair"

        for flag in colisoes:
            if not player.impacto:

                player.position.y += 50
                player.impacto = True
                player.rect.center = player.position
                player.velocidade_retorno = pygame.time.get_ticks() + 500

                slow_motion = True
                tempo_slow = pygame.time.get_ticks()

        if slow_motion:
            if pygame.time.get_ticks() - tempo_slow < duracao_slow:
                background.speed = 1
                for flag in flags_group:
                    flag.speed = 1
                avalanche.velocidade = 1

            else:
                slow_motion = False
                background.speed = 5

                for flag in flags_group:
                    flag.speed = 5
                avalanche.velocidade = 2
                        
        # Flags sendo geradas               
        if contador_flags >= tempo_entre_flags:
            x1 = random.randint(100, 300)
            x2 = random.randint(500, 700)

            flag_esquerda = Flags(x1, -50, background.speed, "vermelha")
            flag_direita = Flags(x2, -50, background.speed, "azul")

            flags_group.add(flag_esquerda, flag_direita)

            # Cria zona entre elas
            x_meio = (x1 + x2) // 2
            zona = ZonaBonus(x_meio, -30)
            zona.speed = background.speed

            zona_bonus.add(zona)

            contador_flags = 0

        if distancia_percorrida >= distancia_total and not venceu:
            venceu = True

            fonte_vitoria = pygame.font.SysFont("Poppins", 60, bold=True)
            texto_vitoria = fonte_vitoria.render("Você Venceu!", True, (0, 180, 0))
            tela.blit(texto_vitoria, texto_vitoria.get_rect(center=(LARGURA // 2, ALTURA // 2)))

            # Cálculo da distância percorrida em porcentagem
            porcentagem = min(100, (distancia_percorrida / distancia_total) * 100)
            fonte_distancia = pygame.font.SysFont("Poppins", 24)
            texto_distancia = fonte_distancia.render(f"Progresso: {porcentagem:.1f}%", True, (0, 0, 0))
            tela.blit(texto_distancia, (10, 40))
            pygame.display.flip()

            pygame.mixer.music.stop()
            som_ganhar.play()
            pygame.time.wait(3000)
            pygame.mixer.music.play(-1)

            return "inicio"

        if tempo_restante == 0 and not venceu:
            fonte_gameover = pygame.font.SysFont("Poppins", 60, bold=True)
            texto_gameover = fonte_gameover.render("Você Perdeu!", True, (255, 0, 0))
            tela.blit(texto_gameover, texto_gameover.get_rect(center=(LARGURA // 2, ALTURA // 2)))
            pygame.display.flip()

            pygame.mixer.music.stop()
            som_perder.play()
            pygame.time.wait(3000)
            pygame.mixer.music.play(-1)

            return "recomecar"
            
        else:
            # Lógica do jogo aqui (movimentos, colisões, etc.)
            background.update()

            distancia_percorrida += background.speed

            #background2.update()
            avalanche.update()
            flags_group.update()
            zona_bonus.update()
            grupo.update()

            # Preenche a tela
            background.draw(tela)
            #background2.draw(tela)
            avalanche.draw(tela)
            flags_group.draw(tela)
            zona_bonus.draw(tela)
            grupo.draw(tela)

            # Tempo na tela
            fonte_tempo = pygame.font.SysFont("Poppins", 30)
            texto_tempo = fonte_tempo.render(f"Tempo: {tempo_restante}s", True, (255, 0, 0))
            tela.blit(texto_tempo, (10, 10))

            porcentagem = min(100, (distancia_percorrida / distancia_total) * 100)

            fonte_distancia = pygame.font.SysFont("Poppins", 24)
            texto_distancia = fonte_distancia.render(f"Progresso: {porcentagem:.1f}%", True, (0, 0, 0))
            tela.blit(texto_distancia, (10, 40))

            # Barra de progresso visual
            barra_largura = 200
            barra_altura = 20
            barra_x = 10
            barra_y = 70
            progresso_largura = int((porcentagem / 100) * barra_largura)

            pygame.draw.rect(tela, (180, 180, 180), (barra_x, barra_y, barra_largura, barra_altura))  # fundo
            pygame.draw.rect(tela, (0, 200, 0), (barra_x, barra_y, progresso_largura, barra_altura))  # progresso      

            # Atualiza a tela
            pygame.display.flip()
            clock.tick(60)

    # Encerra o pygame
    #pygame.quit()

    return "inicio"

def fase_2():
    rodando = True
    clock = pygame.time.Clock()
    
    player = Player("Vovô")
    background = Background(1)
    avalanche = Avalanche()
    
    flags_group = pygame.sprite.Group()
    pedras_group = pygame.sprite.Group()
    grupo = pygame.sprite.Group()
    grupo.add(player)
    
    contador_flags = 0
    tempo_entre_flags= 60

    tempo_restante = 30
    ultimo_tempo = pygame.time.get_ticks()
    venceu = False

    slow_motion = False
    tempo_slow = 0
    duracao_slow = 500

    distancia_percorrida = 0
    distancia_total = 20000
    
    while rodando:
        contador_flags += 1

        colisoes = pygame.sprite.spritecollide(player, flags_group, dokill=False)
        colisoes_pedra = pygame.sprite.spritecollide(player, pedras_group, dokill=False)

        tempo_atual = pygame.time.get_ticks()
        delta = (tempo_atual - ultimo_tempo) // 1000
        if delta > 0:
            tempo_restante = max(0, tempo_restante - delta)
            ultimo_tempo = tempo_atual

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False

            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    acao = Menu.menu_pause()

                    if acao == "recomecar":
                        return fase_1()
                    
                    elif acao == "inicio":
                        return "menu"

                    elif acao == "sair":
                        return "sair"

        for flag in colisoes:
            if not player.impacto:
                player.position.y += 50
                player.impacto = True
                player.rect.center = player.position
                tempo_slow = pygame.time.get_ticks()
                slow_motion = True

                if random.random() < 0.3:
                    tempo_restante += 1
                    som_bonus.play()

        for pedra in colisoes_pedra:
            if not player.impacto:
                player.position.y += 100  # impacto mais forte
                player.impacto = True
                player.rect.center = player.position
                tempo_slow = pygame.time.get_ticks()
                slow_motion = True

        if slow_motion:
            if pygame.time.get_ticks() - tempo_slow < duracao_slow:
                background.speed = 1
                for flag in flags_group: flag.speed = 1
                for pedra in pedras_group: pedra.speed = 1
                avalanche.velocidade = 1
            else:
                slow_motion = False
                background.speed = 5
                for flag in flags_group: flag.speed = 5
                for pedra in pedras_group: pedra.speed = 5
                avalanche.velocidade = 2
                        
        if contador_flags >= tempo_entre_flags:
            x = random.randint(100, 700)
            cor = "azul" if random.random() < 0.5 else "vermelha"
            flags_group.add(Flags(x, -50, background.speed, cor))

            if random.randint(0, 100) < 40:
                pedras_group.add(Pedra(random.randint(100, 700), -100, background.speed))
            contador_flags = 0

        if distancia_percorrida >= distancia_total and not venceu:
            venceu = True
            fonte_vitoria = pygame.font.SysFont("Poppins", 60, bold=True)
            texto_vitoria = fonte_vitoria.render("Você Venceu!", True, (0, 180, 0))
            tela.blit(texto_vitoria, texto_vitoria.get_rect(center=(LARGURA // 2, ALTURA // 2)))
            pygame.display.flip()
            
            pygame.mixer.music.stop()
            som_ganhar.play()
            pygame.time.wait(3000)
            pygame.mixer.music.play(-1)

            return "inicio"

        if tempo_restante == 0 and not venceu:
            fonte_gameover = pygame.font.SysFont("Poppins", 60, bold=True)
            texto_gameover = fonte_gameover.render("Você Perdeu!", True, (255, 0, 0))
            tela.blit(texto_gameover, texto_gameover.get_rect(center=(LARGURA // 2, ALTURA // 2)))
            pygame.display.flip()
            
            pygame.mixer.music.stop()
            som_perder.play()
            pygame.time.wait(3000)
            pygame.mixer.music.play(-1)

            return "recomecar"
            
        else:
            background.update()
            distancia_percorrida += background.speed
            avalanche.update()
            flags_group.update()
            pedras_group.update()
            grupo.update()

            background.draw(tela)
            avalanche.draw(tela)
            flags_group.draw(tela)
            pedras_group.draw(tela)
            grupo.draw(tela)

            # HUD
            porcentagem = min(100, (distancia_percorrida / distancia_total) * 100)

            fonte_tempo = pygame.font.SysFont("Poppins", 30)
            tela.blit(fonte_tempo.render(f"Tempo: {tempo_restante}s", True, (255, 0, 0)), (10, 10))

            fonte_distancia = pygame.font.SysFont("Poppins", 24)
            tela.blit(fonte_distancia.render(f"Progresso: {porcentagem:.1f}%", True, (0, 0, 0)), (10, 40))

            # Barra de progresso
            barra_largura = 200
            barra_altura = 20
            barra_x = 10
            barra_y = 70
            progresso_largura = int((porcentagem / 100) * barra_largura)
            pygame.draw.rect(tela, (180, 180, 180), (barra_x, barra_y, barra_largura, barra_altura))
            pygame.draw.rect(tela, (0, 200, 0), (barra_x, barra_y, progresso_largura, barra_altura))

            pygame.display.flip()
            clock.tick(60)

    return "inicio"

def fase_3():
    rodando = True
    clock = pygame.time.Clock()
    
    player = Player("Vovô")
    background = Background(1)
    avalanche = Avalanche()
    
    flags_group = pygame.sprite.Group()
    pedras_group = pygame.sprite.Group()
    arvore_group = pygame.sprite.Group()

    grupo = pygame.sprite.Group()
    grupo.add(player)
    
    contador_flags = 0
    tempo_entre_flags= 60

    tempo_fase = 30
    inicio_tempo = pygame.time.get_ticks()
    venceu = False

    slow_motion = False
    tempo_slow = 0
    duracao_slow = 500

    distancia_percorrida = 0
    distancia_total = 20000
    
    while rodando:
        contador_flags += 1

        colisoes = pygame.sprite.spritecollide(player, flags_group, dokill=False)
        colisoes_pedra = pygame.sprite.spritecollide(player, pedras_group, dokill=False)

        tempo_decorrido = (pygame.time.get_ticks() - inicio_tempo) // 1000
        tempo_restante = max(0, tempo_fase - tempo_decorrido)
        
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False

            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    acao = Menu.menu_pause()

                    if acao == "recomecar":
                        return fase_1()
                    
                    elif acao == "inicio":
                        return "menu"

                    elif acao == "sair":
                        return "sair"

        for flag in colisoes:
            if not player.impacto:
                player.position.y += 50
                player.impacto = True
                player.rect.center = player.position
                tempo_slow = pygame.time.get_ticks()
                slow_motion = True

                if random.random() < 0.3:
                    tempo_fase += 1
                    som_bonus.play()

        for pedra in colisoes_pedra:
            if not player.impacto:
                player.position.y += 100  # impacto mais forte
                player.impacto = True
                player.rect.center = player.position
                tempo_slow = pygame.time.get_ticks()
                slow_motion = True

        for arvore in colisoes_pedra:
            if not player.impacto:
                player.position.y += 100  # impacto mais forte
                player.impacto = True
                player.rect.center = player.position
                tempo_slow = pygame.time.get_ticks()
                slow_motion = True

        if slow_motion:
            if pygame.time.get_ticks() - tempo_slow < duracao_slow:
                background.speed = 1
                for flag in flags_group: flag.speed = 1
                for pedra in pedras_group: pedra.speed = 1
                for arvore in arvore_group: arvore.speed = 1
                avalanche.velocidade = 1
            else:
                slow_motion = False
                background.speed = 5
                for flag in flags_group: flag.speed = 5
                for pedra in pedras_group: pedra.speed = 5
                for arvore in arvore_group: arvore.speed = 5
                avalanche.velocidade = 2
                        
        if contador_flags >= tempo_entre_flags:
            x = random.randint(100, 700)
            flags_group.add(Flags(x, -50, background.speed))

            if random.randint(0, 100) < 40:
                pedras_group.add(Pedra(random.randint(100, 700), -100, background.speed))

            if random.randint(0, 100) < 30:
                arvore_group.add(Arvore(random.randint(100, 700), - 150, background.speed))
            contador_flags = 0

        if distancia_percorrida >= distancia_total and not venceu:
            venceu = True
            fonte_vitoria = pygame.font.SysFont("Poppins", 60, bold=True)
            texto_vitoria = fonte_vitoria.render("Você Venceu!", True, (0, 180, 0))
            tela.blit(texto_vitoria, texto_vitoria.get_rect(center=(LARGURA // 2, ALTURA // 2)))
            pygame.display.flip()

            pygame.mixer.music.stop()
            som_ganhar.play()
            pygame.time.wait(3000)
            pygame.mixer.music.play(-1)

            return "inicio"

        if tempo_restante == 0 and not venceu:
            fonte_gameover = pygame.font.SysFont("Poppins", 60, bold=True)
            texto_gameover = fonte_gameover.render("Você Perdeu!", True, (255, 0, 0))
            tela.blit(texto_gameover, texto_gameover.get_rect(center=(LARGURA // 2, ALTURA // 2)))
            pygame.display.flip()

            pygame.mixer.music.stop()
            som_perder.play()
            pygame.time.wait(3000)
            pygame.mixer.music.play(-1)

            return "recomecar"
            
        else:
            background.update()
            distancia_percorrida += background.speed
            avalanche.update()
            flags_group.update()
            pedras_group.update()
            arvore_group.update()

            grupo.update()

            background.draw(tela)
            avalanche.draw(tela)
            flags_group.draw(tela)
            pedras_group.draw(tela)
            arvore_group.draw(tela)

            grupo.draw(tela)

            porcentagem = min(100, (distancia_percorrida / distancia_total) * 100)

            fonte_tempo = pygame.font.SysFont("Poppins", 30)
            tela.blit(fonte_tempo.render(f"Tempo: {tempo_restante}s", True, (255, 0, 0)), (10, 10))

            fonte_distancia = pygame.font.SysFont("Poppins", 24)
            tela.blit(fonte_distancia.render(f"Progresso: {porcentagem:.1f}%", True, (0, 0, 0)), (10, 40))

            # Barra de progresso
            barra_largura = 200
            barra_altura = 20
            barra_x = 10
            barra_y = 70
            progresso_largura = int((porcentagem / 100) * barra_largura)
            pygame.draw.rect(tela, (180, 180, 180), (barra_x, barra_y, barra_largura, barra_altura))
            pygame.draw.rect(tela, (0, 200, 0), (barra_x, barra_y, progresso_largura, barra_altura))

            pygame.display.flip()
            clock.tick(60)

    return "inicio"

def mostrar_fase(numero):
    tela.fill((240, 248, 255))

    fonte = pygame.font.SysFont("Poppins", 60, bold=True)
    texto = fonte.render(f"Fase {numero}", True, (0, 0, 0))

    tela.blit(texto, texto.get_rect(center=(LARGURA // 2, ALTURA // 2)))
    pygame.display.flip()
    pygame.mixer.music.stop()
    som_next_level.play()
    pygame.display.flip()
    pygame.time.wait(2000)
    pygame.mixer.music.play(-1)

# Executa o jogo
while True:
    menu_principal()

    resultado = fase_1()
    if resultado == "sair":
        break
    if resultado == "menu":
        continue
    if resultado == "inicio":
        mostrar_fase(2)
        resultado = fase_2()

        if resultado == "sair":
            break
        if resultado == "menu":
            continue
        if resultado == "inicio":
            mostrar_fase(3)
            resultado = fase_3()

            if resultado == "sair":
                break
            if resultado == "menu":
                continue