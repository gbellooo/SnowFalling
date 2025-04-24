import pygame

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
        self.position = pygame.math.Vector2(LARGURA // 2, ALTURA - 100)
        self.speed = 5
        
        self.image = pygame.image.load("vovo.png")
        self.image = pygame.transform.scale(self.image, (120, 120))
        
        self.rect = self.image.get_rect()
        self.rect.center = self.position
        
    def update(self):
        Keys = pygame.key.get_pressed()
        
        if Keys [K_LEFT]:
            self.position.x -= self.speed
        
        if Keys [K_RIGHT]:
            self.position.x += self.speed
            
        if self.position.x < self.rect.width // 2:
            self.position.x = self.rect.width //2
            
        if self.position.x > LARGURA - self.rect.width // 2:
            self.position.x = LARGURA - self.rect.width //2
            
        self.rect.center = self.position
        
class Background:
    def __init__(self, speed):
        self.image = pygame.image.load("background.png")
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

def main():
    rodando = True
    clock = pygame.time.Clock()
    
    player = Player("Vovô")
    
    background = Background(1)
    
    grupo = pygame.sprite.Group()
    grupo.add(player)
    
    while rodando:
        #clock.tick(60)  # Controla os frames por segundo

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False

        # Lógica do jogo aqui (movimentos, colisões, etc.)
        background.update()
        grupo.update()

        # Preenche a tela
        background.draw(tela)
        grupo.draw(tela)

        # Atualiza a tela
        pygame.display.flip()
        clock.tick(60)

    # Encerra o pygame
    pygame.quit()
    
# Executa o jogo
main()    