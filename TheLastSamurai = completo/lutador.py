import pygame
import math
import heapq  # Para implementar a fila de prioridade do Dijkstra

pygame.mixer.init()

som_espada = pygame.mixer.Sound('audio\som_espada.mp3')
som_espada.set_volume(0.2)
som_shuriken = pygame.mixer.Sound('audio\shuriken_som.mp3')
som_shuriken.set_volume(0.2)
damage = pygame.mixer.Sound('audio\damage.mp3')
damage.set_volume(4)
som_fogo = pygame.mixer.Sound('audio\som_fogo.mp3')
som_fogo.set_volume(3)


class Lutador():
    def __init__(self, x, y):
        self.rect = pygame.Rect((x, y, 60, 100))
        self.saude = 100
        self.is_attacking = False   
        self.img_index = 0
        self.current_action = 'idle'  # Estado atual da animação
        self.speed = 5  # Velocidade de movimento
        self.velocidade_y = 0
        self.last_frame_time = pygame.time.get_ticks()  # Inicializa o tempo do último frame
        self.projectiles = []  # Lista de projéteis (shurikens)
        self.attack_box = pygame.Rect((0, 0, 0, 0))

    def attack_distancia(self, oponente):
        if not self.is_attacking:
            som_shuriken.play()
            self.is_attacking = True
            self.img_index = 0  # Reiniciar a animação
            self.current_action = 'attack3'  # Estado atual da animação

            # Define o alvo como a posição atual do inimigo
            shuriken = AtaqueDistancia(
                x=self.rect.centerx,
                y=self.rect.centery,
                target_x=oponente.rect.centerx,
                target_y=oponente.rect.centery,
                speed=10,
                image="armas\shuriken3.png"  # Substitua pelo caminho correto
            )

            self.projectiles.append(shuriken)

    def update_projectiles(self, oponente): #Esta sendo chamada
        for shuriken in self.projectiles:
            shuriken.update()
            if shuriken.active and shuriken.rect.colliderect(oponente.rect):
                oponente.saude -= 5
                shuriken.active = False  # Remove a shuriken após o impacto
                self.is_attacking = False
            else:
                self.is_attacking = False

    def desenhar_shuriken(self, screen):
        # Desenha os projéteis
        for shuriken in self.projectiles:
            shuriken.draw(screen)     

    def attack_melee(self,oponente):
                
        if oponente.rect.x > self.rect.x:
                # Oponente está à direita
                self.attack_box = pygame.Rect((self.rect.x + self.rect.width, self.rect.y, 70, 120))
        else:
                # Oponente está à esquerda
                self.attack_box = pygame.Rect((self.rect.x - 60, self.rect.y, 70, 120))                    

        if not self.is_attacking:
            som_espada.play()
            self.is_attacking = True
            self.img_index = 0  # Reiniciar a animação
            self.current_action = 'attack'
        
        # Desenhar hitbox na tela para visualização
        if self.attack_box.colliderect(oponente.rect):
            # Iniciar ataque se não estiver atacando
            oponente.saude -= 10
            damage.play()


    def attack_melee_especial(self,oponente):
        som_fogo.play()

        if oponente.rect.x > self.rect.x:
                # Oponente está à direita
                self.attack_box = pygame.Rect((self.rect.x + self.rect.width, self.rect.y, 70, 120))
                
        else:
                # Oponente está à esquerda
                self.attack_box = pygame.Rect((self.rect.x - 60, self.rect.y, 70, 120))        
                           

        if not self.is_attacking:

            self.is_attacking = True
            self.img_index = 0  # Reiniciar a animação
            self.current_action = 'attack2'
        
        # Desenhar hitbox na tela para visualização
        if self.attack_box.colliderect(oponente.rect):
            # Iniciar ataque se não estiver atacando
            oponente.saude -= 20


    def desenhar(self, tela, lutador, lut_dic, oponente):

        frame_duration = 50  # Aumente o valor para tornar a animação mais lenta
        current_time = pygame.time.get_ticks()
        lutador_img = None

        # Verifica se o tempo de espera entre os frames passou
        if current_time - self.last_frame_time >= frame_duration:
            self.img_index += 1
            self.last_frame_time = current_time

            if self.img_index >= len(lut_dic[self.current_action]):
                self.img_index = 0
                if self.current_action == 'attack' or self.current_action == 'attack2' or self.current_action == 'attack3':  # Se for um ataque, volta para idle
                    self.current_action = 'idle'
                    self.is_attacking = False

        # Seleção da imagem com base na ação e no índice de imagem
        if self.current_action in lut_dic:
            lutador_img = lut_dic[self.current_action][self.img_index]

        velocidade = 10
                
        GRAVITY = 0.6  # Gravidade aplicada no eixo Y
        GROUND = 547  # Altura do chão onde o personagem deve parar

        # Atualizar gravidade
        self.velocidade_y += GRAVITY
        self.rect.y += self.velocidade_y

        # Impedir que o personagem passe do chão
        if self.rect.bottom >= GROUND:
            self.rect.bottom = GROUND
            self.velocidade_y = 0
            self.no_chao = True
        else:
            self.no_chao = False

        '''MOVIMENTO DO PERSONAGEM WASD'''
        key = pygame.key.get_pressed()

        # Movimento para a esquerda
        if key[pygame.K_a] and lutador == 1:
            if self.img_index >= len(lut_dic['run']):
                self.img_index = 0
            lutador_img = pygame.transform.flip(lut_dic['run'][self.img_index], True, False)
            self.rect.x -= velocidade
            if self.rect.left < 0:
                self.rect.x = 0

        # Movimento para a direita
        if key[pygame.K_d] and lutador == 1:
            if self.img_index >= len(lut_dic['run']):
                self.img_index = 0
            lutador_img = lut_dic['run'][self.img_index]
            self.rect.x += velocidade
            if self.rect.right >= tela.get_width() - 50:
                self.rect.x = tela.get_width() - 50


        # Pular
        if key[pygame.K_w] and self.no_chao and lutador == 1:
            lutador_img = lut_dic['jump'][self.img_index]   
            self.velocidade_y -= 15  # Força do pulo
            self.no_chao = False


        if self.rect.centerx > oponente.rect.centerx and oponente.saude > 0:
            lutador_img = pygame.transform.flip(lutador_img, True, False)

    
        #LINHA QUE MOSTRA O ATAQUE A DISTÂNCIA
        
        '''pygame.draw.line(
            tela,
            (255, 255, 0),  # Cor da linha (amarelo)
            (self.rect.centerx, self.rect.centery),
            (oponente.rect.x, oponente.rect.y),
            2
        )'''

        #pygame.draw.rect(tela, (255, 0, 0), self.attack_box, 2)           
        # Desenhar o lutador na tela
        if lutador == 1:
            tela.blit(lutador_img, (self.rect.x - 45, self.rect.y - 45))
        else:
            tela.blit(lutador_img, (self.rect.x - 40, self.rect.y - 50))


class AtaqueDistancia:
    def __init__(self, x, y, target_x, target_y, speed, image):

        self.rect = pygame.Rect(x, y - 30, 60, 60)  # Tamanho da shuriken
        self.target_x = target_x
        self.target_y = target_y
        self.speed = speed
        self.image = pygame.image.load(image)  # Carrega a imagem da shuriken
        self.image = pygame.transform.scale(self.image, (80, 80))  # Ajusta o tamanho
        self.dx = target_x - x
        self.dy = target_y - y
        self.angle = math.atan2(self.dy, self.dx)
        self.vel_x = math.cos(self.angle) * speed
        self.vel_y = math.sin(self.angle) * speed
        self.active = True  # Status da shuriken (ativa ou não)

    def update(self): #Está sendo chamado
        if self.active:
            # Move a shuriken na direção do alvo
            self.rect.x += self.vel_x
            self.rect.y += self.vel_y

            # Desativa se sair da tela
            if (self.rect.x < 0 or self.rect.x > 800 or 
                self.rect.y < 0 or self.rect.y > 600):
                self.active = False

    def draw(self, tela): #Esta sendo chamado
        if self.active:
            tela.blit(self.image, self.rect)