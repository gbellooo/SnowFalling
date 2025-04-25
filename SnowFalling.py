import pygame
import random

from pygame.locals import*

# Inicializa o pygame
pygame.init()

# Configurações da tela
LARGURA = 800
ALTURA = 600
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("SnowFalling")

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
        
        self.image = pygame.image.load("vovo1.png")
        self.image = pygame.transform.scale(self.image, (100, 100))
        
        self.rect = self.image.get_rect()
        self.rect.center = self.position
        
    def update(self):
        Keys = pygame.key.get_pressed()
        
        if Keys [K_LEFT]:
            self.deslizamento_x -= self.aceleracao * 60
            self.position.x -= self.speed
        
        elif Keys [K_RIGHT]:
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
            self.index = (self.index + 1) % len(self.frames)  # Avança frame
        
    def draw(self, tela):
        tela.blit(self.frames[self.index], (0, ALTURA - 400))

class Flags(pygame.sprite.Sprite):
    def __init__(self, x, y, background_speed):
        super(Flags, self).__init__()
        
        self.image = pygame.image.load("bandeira.png")
        self.image = pygame.transform.scale(self.image, (100, 100))
        
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
        
        if self.rect.top > 600:
            self.kill()
            
class Menu():
    fonte = pygame.font.SysFont("Arial", 30)

    def desenhar_menu(texto, y, selecionado = False):
        cor = (100, 100, 100)
        ret = pygame.Rect(LARGURA // 2 - 100, y, 200, 50)

        pygame.draw.rect(tela, cor, ret)

        texto_render = Menu.fonte.render(texto, True, (0, 0, 0)) 
        tela.blit(texto_render, (ret.x + 20, ret.y + 5))

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

                if evento.type == pygame.MOUSEBUTTONDOWN:
                    if botao_inicio.collidepoint(evento.pos):
                        print("Voltando ao menu principal futuramente...")
                        return "inicio"
                    
                    elif botao_recomecar.collidepoint(evento.pos):
                        print("Reiniciando fase...")
                        return "recomecar"
                    
                    elif botao_sair.collidepoint(evento.pos):
                        return "sair"

def main():
    rodando = True
    clock = pygame.time.Clock()
    
    player = Player("Vovô")
    background = Background(1)
    background2 = Backgroud2(1)
    avalanche = Avalanche()
    
    flags_group = pygame.sprite.Group()
    grupo = pygame.sprite.Group()
    grupo.add(player)
    
    contador_flags = 0
    tempo_entre_flags= 60
    
    while rodando:
        contador_flags +=1
        
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False

            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    acao = Menu.menu_pause()

                    if acao == "recomecar":
                        return main()
                    
                    elif acao == "inicio":
                        rodando = False

                    elif acao == "sair":
                        rodando = False
                        
            # Flags sendo geradas            
            if contador_flags >= tempo_entre_flags:
                x = random.randint(100, 700)
                nova_flag = Flags(x, -50, background.speed)
                
                flags_group.add(nova_flag)
                contador_flags = 0
            
        else:
            # Lógica do jogo aqui (movimentos, colisões, etc.)
            background.update()
            background2.update()
            avalanche.update()
            flags_group.update()
            grupo.update()

            # Preenche a tela
            background.draw(tela)
            background2.draw(tela)
            avalanche.draw(tela)
            flags_group.draw(tela)
            grupo.draw(tela)

            # Atualiza a tela
            pygame.display.flip()
            clock.tick(60)

    # Encerra o pygame
    pygame.quit()
    
# Executa o jogo
main()    