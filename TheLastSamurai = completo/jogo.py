import pygame
from lutador import Lutador
from enemy import Inimigo
from item import Item
from inventario import Inventario

'''Iniciadores Pygame'''
pygame.mixer.init()
pygame.init()

'''CONFIGURAÇÕES DA TELA'''
x = 1024
y = 576
tela = pygame.display.set_mode((x,y))
pygame.display.set_caption('The Last Samurai: Hikaru Story')
clock = pygame.time.Clock()
FPS =  60

'''IMAGEM FUNDO'''
background1 = pygame.image.load('./backgrounds/background1_centralizado.jpeg').convert_alpha()
background2 = pygame.image.load('./backgrounds/background2.png').convert_alpha()
background3 = pygame.image.load('./backgrounds/background3.jpg').convert_alpha()

def desenhar_fundo():

    # Altera o índice do background apenas na fase correta
    if fase_atual == 1:
        background_ajustado = pygame.transform.scale(background1, (x, y))
    elif fase_atual == 2:
        background_ajustado = pygame.transform.scale(background2, (x, y))
    elif fase_atual == 3:
        background_ajustado = pygame.transform.scale(background3, (x, y))
    else:
        background_ajustado = pygame.Surface((x, y))  # Fase desconhecida, fundo vazio

    # Desenha o fundo correspondente
    tela.blit(background_ajustado, (0, 0))

'''SOM'''
pygame.mixer.music.load('audio/som_de_fundo.mp3')
pygame.mixer.music.set_volume(0.7)
pygame.mixer.music.play()


'''FONTE'''
fonte = pygame.font.SysFont('arial',30)


'''IMAGENS / MOVIMENTOS'''

#Jogador
player_lista = [ pygame.image.load('protagonista/Idle.png'),
                 pygame.image.load('protagonista/Jump.png'),
                 pygame.image.load('protagonista/Run.png'),
                 pygame.image.load('protagonista/Attack_1.png'),
                 pygame.image.load('protagonista/Attack_1_especial.gif'),
                 pygame.image.load('protagonista/Attack_3.png') 
                
                ]

player_dic = {        'idle': [],
                      'jump': [], 
                      'run': [],
                      'attack': [],
                      'attack2': [],
                      'attack3' : [] 
                }


# inimigo 1 - Gotaku
enemy1_lista = [ pygame.image.load('inimigos/Gotoku/Idle.png'),
                 pygame.image.load('inimigos/Gotoku/Dead.png'),
                 pygame.image.load('inimigos/Gotoku/Run.png'),
                 pygame.image.load('inimigos/Gotoku/Attack_1.png') 
                
                ]

enemy1_dic = {        'idle': [],
                      'dead': [], 
                      'run': [],
                      'attack': []  
                }


# inimigo 2 - Onre
enemy2_lista = [ pygame.image.load('inimigos/Onre/Idle.png'),
                 pygame.image.load('inimigos/Onre/Dead.png'),
                 pygame.image.load('inimigos/Onre/Run.png'),
                 pygame.image.load('inimigos/Onre/Attack_1.png') 
                
                ]

enemy2_dic = {        'idle': [],
                      'dead': [], 
                      'run': [],
                      'attack': []  
                }


# inimigo 3 - Yurei
enemy3_lista = [ pygame.image.load('inimigos/Yurei/Idle.png'),
                 pygame.image.load('inimigos/Yurei/Dead.png'),
                 pygame.image.load('inimigos/Yurei/Run.png'),
                 pygame.image.load('inimigos/Yurei/Attack_1.png') 
                
                ]

enemy3_dic = {        'idle': [],
                      'dead': [], 
                      'run': [],
                      'attack': []  
                }


item_chave = 'items/key.png'
item_pocao = 'items/poção.png'
item_tesouro = 'items/FantasmaTesouro.png'


'''CRIAÇÃO DO PLAYER / INIMIGO  E CRIAÇÃO DE ITENS'''
lutador_1 = Lutador(100,300) #Posição Mapa
lutador_2 = Inimigo(800,300)
chave = Item('Chave', image_src=item_chave, scale=0.03, peso=5)
pocao = Item('Poção', image_src=item_pocao, scale=0.4, peso=2)
tesouro = Item('Tesouro', image_src=item_tesouro, scale=0.2, peso=3)
inventario = Inventario(image_src='inventario/bolsa.png', scale=1)


'''CRIAÇÃO DE PERSONAGENS UTILIZANDO OS PARÂMETROS ACIMA'''
def imagens(dic, lista):
    for x, tipo in enumerate(dic):
        img_l = lista[x].get_width()
        img_a = lista[x].get_height()
        for i in range(int(img_l / img_a)):
            img = lista[x].subsurface(i*img_a, 0, img_a, img_a)
            dic[tipo].append(pygame.transform.scale(img, (img_a*1.1, img_a*1.1)))   
    return(dic)        

player = imagens(player_dic, player_lista)
enemy1 = imagens(enemy1_dic, enemy1_lista)


'''HEALTH BAR'''

def desenhar_saude(saude, x, y):
    taxa = saude / 100
    pygame.draw.rect(tela, (255, 0, 0), (x, y, 400, 30))
    pygame.draw.rect(tela, (0,255,0), (x, y, 400*taxa, 30))


'''TRATAMENTO DE FASES'''
fase_atual = 1  # Começa na fase 1

def reiniciar_jogo(enemy_dic, enemy_lista):
    global lutador_1, lutador_2, fim_de_jogo, enemy1
    lutador_1 = Lutador(270, 560)
    lutador_2 = Inimigo(800, 300)
    enemy1 = imagens(enemy_dic, enemy_lista)
    
    fim_de_jogo = False  # Voltar ao estado normal do jogo

winner = pygame.image.load('backgrounds/youwin.png')

def finalizar_jogo():

    screen_width, screen_height = tela.get_size()
    image_width, image_height = winner.get_size()

    # Calcula as coordenadas para centralizar a imagem
    x = (screen_width - image_width) // 2
    y = (screen_height - image_height) // 2

    # Exibe a imagem no centro da tela
    tela.blit(winner, (x, y))
    pygame.display.flip()


    pygame.time.delay(5000)
    pygame.quit()


def desenhar_botao(texto, x, y, largura, altura, cor, cor_texto, acao=None, inimigo_dic=None, inimigo_lista=None):
    mouse = pygame.mouse.get_pos()
    clique = pygame.mouse.get_pressed()
    
    # Verificar se o mouse está sobre o botão
    if x < mouse[0] < x + largura and y < mouse[1] < y + altura:
        cor_clara = (
            min(cor[0] + 40, 255),
            min(cor[1] + 40, 255),
            min(cor[2] + 40, 255),
        )
        pygame.draw.rect(tela, cor_clara, (x, y, largura, altura))  # Cor mais clara ao passar o mouse

        # Verificar clique do mouse
        if clique[0] == 1 and acao is not None:
            acao(inimigo_dic, inimigo_lista)  # Chamada da função com os parâmetros
    else:
        pygame.draw.rect(tela, cor, (x, y, largura, altura))  # Cor normal do botão

    # Adicionar texto ao botão
    texto_surface = fonte.render(texto, True, cor_texto)
    texto_rect = texto_surface.get_rect(center=(x + largura // 2, y + altura // 2))
    tela.blit(texto_surface, texto_rect)


# Variáveis para animação
indice_frame = 0
intervalo = 50  # Intervalo entre frames em milissegundos
animacao_concluida = False
tempo_inicial = pygame.time.get_ticks()
posicao_jogador = pygame.Rect(lutador_1.rect.x + 60, lutador_1.rect.y , 60, 100)  # Apenas para testar a posição do jogador


'''LOOP PRINCIPAL'''
jogando = True
ATTACK_MELEE_COOLDOWN = 500  #Cooldown Ataque Player
ATTACK_ESPECIAL_COOLDOWN = 2000
ATTACK_SHURIKEN_COOLDOWN = 500
last_attack_time = 0
last_attack_time2 = 0
last_attack_time3 = 0


while jogando:
    clock.tick(FPS)


    pygame.display.update()

    '''REINICIAR O JOGO'''
    if lutador_1.saude <= 0 and fase_atual == 1:
 
        desenhar_fundo()
        desenhar_botao("Iniciar Novamente", x//2 - 150, y//2 - 40, 300, 80, (0,139,139), (255, 255, 255), reiniciar_jogo, enemy1_dic, enemy1_lista)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                jogando = False

        continue


    if lutador_1.saude <= 0 and fase_atual == 2:
 
        desenhar_fundo()
        desenhar_botao("Iniciar Novamente", x//2 - 150, y//2 - 40, 300, 80, (0,139,139), (255, 255, 255), reiniciar_jogo, enemy2_dic, enemy2_lista)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                jogando = False

        continue


    if lutador_1.saude <= 0 and fase_atual == 3:
 
        desenhar_fundo()
        desenhar_botao("Iniciar Novamente", x//2 - 150, y//2 - 40, 300, 80, (0,139,139), (255, 255, 255), reiniciar_jogo, enemy3_dic, enemy3_lista)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                jogando = False

        continue    

    '''DESENHO FUNDO E SAÚDE'''
    desenhar_fundo()
    desenhar_saude(lutador_1.saude, 20, 20)
    desenhar_saude(lutador_2.saude, 580, 20)

    '''DESENHO PLAYER E INIMIGO'''
    lutador_1.desenhar(tela, 1, player, lutador_2)
    lutador_2.desenhar(tela, 2, enemy1, lutador_1)
    lutador_2.movimento_inimigo(lutador_1.rect.x,lutador_1.rect.y,lutador_2.rect.x,lutador_2.rect.y, enemy1)

    '''ATAQUE INIMIGO'''
    lutador_2.attack_player(lutador_1, fase_atual)
    lutador_1.update_projectiles(lutador_2)
    '''DESENHA O INVENTÁRIO'''
    inventario.draw_inventario(tela)

    '''DROP DO ITEM'''
    if fase_atual == 1:
        chave.drop_item(chave, lutador_2.saude, lutador_2.rect.x, lutador_2.rect.width, lutador_2.rect.y, tela, fase_atual)

    if fase_atual == 2:
        pocao.drop_item(pocao, lutador_2.saude, lutador_2.rect.x, lutador_2.rect.width, lutador_2.rect.y, tela, fase_atual)
        lutador_2.speed = 7
    
    if fase_atual == 3:
        tesouro.drop_item(tesouro, lutador_2.saude, lutador_2.rect.x, lutador_2.rect.width, lutador_2.rect.y, tela, fase_atual) 
        lutador_2.speed = 9

    '''TRANSIÇÃO DE FASES'''
    if chave.collected and fase_atual == 1:
        fase_atual = 2 
        reiniciar_jogo(enemy2_dic, enemy2_lista)

    if pocao.collected and fase_atual == 2:  
        fase_atual = 3
        reiniciar_jogo(enemy3_dic, enemy3_lista)        

    if tesouro.collected:
        inventario.ordenar_por_peso()
        inventario.print_itens()
        finalizar_jogo() 


    lutador_1.desenhar_shuriken(tela)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            jogando = False

    
        '''TECLA DE ATAQUE DO PLAYER'''    
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_k:
                current_time = pygame.time.get_ticks()  # Tempo atual em milissegundos
                if current_time - last_attack_time >= ATTACK_MELEE_COOLDOWN:
                    last_attack_time = current_time  # Atualizar o tempo do último ataque
                    lutador_1.attack_melee(lutador_2)
            

            if event.key == pygame.K_j:
                pygame.display.update()
                current_time = pygame.time.get_ticks()  # Tempo atual em milissegundos
                if current_time - last_attack_time3 >= ATTACK_ESPECIAL_COOLDOWN:
                    last_attack_time3 = current_time  # Atualizar o tempo do último ataque
                    lutador_1.attack_melee_especial(lutador_2)

            elif event.key == pygame.K_l:
                current_time = pygame.time.get_ticks()  # Tempo atual em milissegundos
                if current_time - last_attack_time2 >= ATTACK_SHURIKEN_COOLDOWN:
                    last_attack_time2 = current_time  # Atualizar o tempo do último ataque
                    lutador_1.attack_distancia(lutador_2)
                    lutador_1.desenhar_shuriken(tela)
                    

            elif event.key == pygame.K_i:  # Tecla 'I' para abrir/fechar o inventário
                inventario.toggle_visibility()


        '''COLETA DE ITENS'''
        if lutador_1.rect.colliderect(chave.hitbox) and not chave.collected:
            #chave.collect()  # Coleta o item
            inventario.add_item(chave, 'Chave')  # Adiciona o item ao inventário    
            inventario.ordenar_por_peso()     

        if lutador_1.rect.colliderect(pocao.hitbox) and not pocao.collected:
            #pocao.collect()  # Coleta o item
            inventario.add_item(pocao, 'Poção')  # Adiciona o item ao inventário      
            inventario.ordenar_por_peso()   

        if lutador_1.rect.colliderect(tesouro.hitbox) and not tesouro.collected:
           # tesouro.collect()  # Coleta o item
            tesouro.update_scale(0.2)
            inventario.add_item(tesouro, 'Tesouro')  # Adiciona o item ao inventário 
            inventario.ordenar_por_peso()
                 

pygame.quit()
