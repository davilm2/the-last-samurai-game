import pygame
import math

pygame.mixer.init()
enemy_punch = pygame.mixer.Sound('audio\punch_enemy.mp3')
enemy_punch.set_volume(0.2)

som_inimigo_2 = pygame.mixer.Sound('audio\punch_enemy2.mp3')
som_inimigo_2.set_volume(0.1)

som_inimigo_3 = pygame.mixer.Sound('audio\punch_enemy3.mp3')
som_inimigo_3.set_volume(0.1)

damage = pygame.mixer.Sound('audio\damage.mp3')
damage.set_volume(0.2)

class Inimigo():
    def __init__(self, x, y):
        self.rect = pygame.Rect((x, y, 60, 100))
        self.saude = 100
        self.is_attacking = False
        self.img_index = 0
        self.current_action = 'idle'  # Estado atual da animação
        self.speed = 5
        self.velocidade_y = 0
        self.last_frame_time = pygame.time.get_ticks() 
        self.last_attack_time = 0
        self.em_movimento = False
        self.image = None
        self.inimigo_index = 0

    def attack_player(self,oponente, fase):
        if self.saude > 0 and self.is_attacking == False:
                current_time = pygame.time.get_ticks()
                if current_time - self.last_attack_time >= 500:  # 500 ms = 0,5 segundos

                    # Iniciar ataque se não estiver atacando
                    if not self.is_attacking and self.rect.colliderect(oponente.rect):
                        self.last_attack_time = current_time
                        self.is_attacking = True
                        self.img_index = 0  # Reiniciar a animação
                        self.current_action = 'attack'
                            # Atualiza o tempo do último ataque

                        if oponente.rect.x > self.rect.x:
                                # Oponente está à direita
                                self.attack_box = pygame.Rect((self.rect.x + self.rect.width, self.rect.y, 60, 100))
                        else:
                                # Oponente está à esquerda
                                self.attack_box = pygame.Rect((self.rect.x - 60, self.rect.y, 60, 100))

                        #pygame.draw.rect(tela, (255, 0, 0), self.attack_box, 2)
                    
                    # Desenhar hitbox na tela para visualização
                        if self.attack_box.colliderect(oponente.rect) and fase == 1:
                            enemy_punch.play()
                            oponente.saude -= 10


                        if self.attack_box.colliderect(oponente.rect) and fase == 2:
                            som_inimigo_2.play()
                            oponente.saude -= 15


                        if self.attack_box.colliderect(oponente.rect) and fase == 3:
                            som_inimigo_3.play()
                            oponente.saude -= 20



    def movimento_inimigo(self,x1, y1, x2, y2, lut_dic):
        if self.saude > 0:
            calcular_distancia = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
            distancia = calcular_distancia
            
            if distancia > 59:

                self.em_movimento = True
                
                # Move o inimigo em direção ao jogador
                if x1 < self.rect.x:
                    self.current_action = 'run'
                    if self.img_index >= len(lut_dic['run']):
                        self.img_index = 0
                    self.rect.x -= self.speed  # Movendo para a esquerda   

                elif x1 > self.rect.x:
                    self.current_action = 'run'
                    if self.img_index >= len(lut_dic['run']):
                        self.img_index = 0
                    self.rect.x += self.speed # Movendo para a direita



    def desenhar(self, tela, lutador, lut_dic, oponente):
        # Se a saúde do inimigo for maior que 0, ele ainda está vivo
        if self.saude > 0:
            # Configuração para controle de animação
            frame_duration = 50  # Aumente o valor para tornar a animação mais lenta
            current_time = pygame.time.get_ticks()

            # Verifica se o tempo de espera entre os frames passou
            if current_time - self.last_frame_time >= frame_duration:
                self.img_index += 1
                self.last_frame_time = current_time

                if self.img_index >= len(lut_dic[self.current_action]):
                    self.img_index = 0
                    if self.current_action == 'attack' or self.current_action == 'run' :  # Se for um ataque, volta para idle
                        self.current_action = 'idle'
                        self.is_attacking = False

            # Seleção da imagem com base na ação e no índice de imagem
            if self.current_action in lut_dic:
                self.image = lut_dic[self.current_action][self.img_index]

            # Gravidade e movimento do inimigo
            GRAVITY = 0.6  # Gravidade aplicada no eixo Y
            GROUND = 547  # Altura do chão onde o personagem deve parar

            # Atualiza a velocidade do inimigo e sua posição no eixo Y
            self.velocidade_y += GRAVITY
            self.rect.y += self.velocidade_y

            # Impede que o inimigo passe do chão
            if self.rect.bottom >= GROUND:
                self.rect.bottom = GROUND
                self.velocidade_y = 0
                self.no_chao = True
            else:
                self.no_chao = False

            # Verifica se o inimigo está à direita ou à esquerda do oponente
            if self.rect.centerx > oponente.rect.centerx:
                self.image = pygame.transform.flip(self.image, True, False)

            # Desenha o inimigo na tela com base na posição do lutador
            if lutador == 1:
                tela.blit(self.image, (self.rect.x - 45, self.rect.y - 45))
            else:
                tela.blit(self.image, (self.rect.x - 40, self.rect.y - 50))

        if self.saude <= 0:
            # Se a saúde do inimigo for menor ou igual a 0, ele morre e a animação de morte começa
            self.current_action = 'dead'

            # Atualiza a animação de morte
            frame_duration = 200  # Duração maior para animação de morte
            current_time = pygame.time.get_ticks()

            if self.img_index < len(lut_dic['dead']):
                self.image = lut_dic['dead'][self.img_index]

                # Controle de animação de morte
                if current_time - self.last_frame_time >= frame_duration:
                    self.img_index += 1
                    self.last_frame_time = current_time

            # Se a animação de morte terminou, o inimigo não é mais desenhado
            if self.img_index >= len(lut_dic['dead']):
                return  # Sai da função para não desenhar mais o inimigo

            # Desenha a animação de morte na tela
            if lutador == 1:
                tela.blit(self.image, (self.rect.x - 45, self.rect.y - 45))
            else:
                tela.blit(self.image, (self.rect.x - 40, self.rect.y - 50))



