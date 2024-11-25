import pygame


class Inventario:
    def __init__(self, image_src, scale=1):
        self.image = pygame.image.load(image_src)
        self.scale = scale
        self.update_image()
        self.is_visible = False  # Inventário começa invisível
        self.itens = []  # Lista para armazenar os itens coletados   
        self.peso_maximo = 10  # Peso máximo do inventário
        self.peso_atual = 0  # Peso atual dos itens no inventário    

    def update_image(self):
        width = 175
        height = int(self.image.get_height() * self.scale)
        self.image = pygame.transform.scale(self.image, (width, height))

    def toggle_visibility(self):
        self.is_visible = not self.is_visible

    def add_item(self, item, nome):
        """Adiciona um item ao inventário se não exceder o peso máximo."""
        if self.peso_atual + item.peso <= self.peso_maximo:
            self.itens.append(item)  # Adiciona o item à lista
            self.peso_atual += item.peso  # Atualiza o peso atual
            item.collected = True
            print(f"{nome} foi adicionado ao inventário.")  # Print opcional para debug
        else:
            print(f"Não foi possível adicionar {nome}: Peso máximo do inventário excedido!")

        # Exibe o inventário e seus itens
        print("Inventário:")
        for item in self.itens:
            print(f"- {item.nome} (Peso: {item.peso})")
        print(f"Peso total: {self.peso_atual}/{self.peso_maximo}")    

    
    def print_itens(self):
  
        print("Inventário:")
        for item in self.itens:
            print(f"- {item.nome} (Peso: {item.peso})")
        print(f"Peso total: {self.peso_atual}/{self.peso_maximo}")  

    def ordenar_por_peso(self):
        """Ordena os itens no inventário por peso."""
        self.itens.sort(key=lambda item: item.peso)  # Ordena com base no peso

    def draw_inventario(self, tela):
        if self.is_visible:
            # Calcula a posição abaixo da barra de vida do Player
            x = 20  # Alinha com o início da barra de vida
            y = 20 + 20 + 10  # (posição da barra de vida) + (altura da barra) + (espaçamento)
            tela.blit(self.image, (x, y))

            # Desenha os itens coletados no inventário
            x_offset = x + 10  # Ajusta a posição inicial para os itens
            y_offset = y + self.image.get_height() - 40  # Ajusta a posição vertical para alinhar
            for item in self.itens:
                # Exibe a imagem do item
                tela.blit(item.image, (x_offset, y_offset))
                x_offset += 60  # Desloca 40 pixels para a direita para o próximo item
