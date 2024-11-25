import pygame


class Item:
    def __init__(self, nome, image_src, scale, peso):
        self.position_x = 0  # Posição X inicial
        self.position_y = 0  # Posição Y inicial
        self.image = pygame.image.load(image_src)
        self.scale = scale
        self.hitbox = pygame.Rect(0, 0, 0, 0)  # Inicializa a hitbox        
        self.update_image()  # Atualiza a imagem com a escala fornecida
        self.nome = nome   
        self.peso = peso     
        self.collected = False

    def update_scale(self, new_scale):
        """Atualiza a escala do item e ajusta a imagem e a hitbox."""
        self.scale = new_scale
        self.update_image()

    def update_image(self):
        # Redimensiona a imagem com o fator de escala
        width = int(self.image.get_width() * self.scale)
        height = int(self.image.get_height() * self.scale)
        self.image = pygame.transform.scale(self.image, (width, height))

        # Atualiza o tamanho da hitbox com base na imagem escalada
        self.hitbox.width = width
        self.hitbox.height = height        

    def set_position(self, position_x, position_y):
        # Método para atualizar a posição da chave
        self.position_x = position_x
        self.position_y = position_y

        # Atualiza a posição da hitbox com base na posição do item
        self.hitbox.x = self.position_x - self.hitbox.width // 2
        self.hitbox.y = self.position_y - self.hitbox.height // 2


    def draw(self, tela):
        if not self.collected:  # Só desenha o item se não foi coletado
            tela.blit(self.image, (self.position_x - self.image.get_width() // 2, self.position_y - self.image.get_height()// 2))
            # Desenha a hitbox (opcional, para visualização)
            #pygame.draw.rect(tela, (0, 0, 255), self.hitbox, 2)

        
    def drop_item(self,item, saude_oponente, posicao_inimigo_x, inimigo_width, posicao_inimigo_y, tela, fase):

        if saude_oponente <= 0 and fase == 1:
            # A chave será posicionada na posição de morte do inimigo
            item.set_position(posicao_inimigo_x + inimigo_width// 2, posicao_inimigo_y - 40)
            item.draw(tela)  # Exibe o item (a chave)
            return
        
        if saude_oponente <= 0 and fase == 2:
            # A chave será posicionada na posição de morte do inimigo
            item.set_position(posicao_inimigo_x + inimigo_width// 2, posicao_inimigo_y - 40)
            item.draw(tela)  # Exibe o item (a chave)
            return

        if saude_oponente <= 0 and fase == 3:
            item.set_position( 800, posicao_inimigo_y + 50)
            item.draw(tela)  # Exibe o item (a chave)
            return
                    

    def collect(self):
        self.collected = True  # Marca o item como coletado                        