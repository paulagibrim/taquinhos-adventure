import random
from settings import *
from pgzero.builtins import Actor, keyboard, sounds

class Entity(Actor):
    def __init__(self, pos, idle_frames, right_walk_frames, left_walk_frames,
                 climb_frames=None, hit_frames=None,
                 right_jump_frames=None, left_jump_frames=None, idle_jump_frames=None,
                 right_attack_frames=None, left_attack_frames=None):
        """
                Inicializa a entidade com suas respectivas listas de frames.

                Args:
                    pos (tuple): Coordenadas (x, y) iniciais.
                    idle_frames (list): Lista de imagens para estado parado (Obrigatório).
                    right_walk_frames (list): Imagens para caminhada à direita (Obrigatório).
                    left_walk_frames (list): Imagens para caminhada à esquerda (Obrigatório).
                    **kwargs: Listas de frames opcionais para estados específicos.
            """
        # Inicia o objeto Actor
        super().__init__(idle_frames[0], pos)

        # Define os atributos com base nas informações passadas no construtor
        self.idle_frames = idle_frames
        self.right_walk_frames = right_walk_frames
        self.left_walk_frames = left_walk_frames
        self.climb_frames = climb_frames
        self.right_jump_frames = right_jump_frames
        self.left_jump_frames = left_jump_frames
        self.idle_jump_frames = idle_jump_frames
        self.right_attack_frames = right_attack_frames
        self.left_attack_frames = left_attack_frames
        self.hit_frames = hit_frames

        # Define atributos importantes para as animações
        self.frame_index = 0
        self.anim_timer = 0
        self.state = "IDLE"
        self.anim_speed = 10
        self.hit_right = None   # False para LEFT, True para RIGHT
        self.is_dead = False
        self.is_attacking = False

    def update_animation(self, is_moving, on_ground, velocity_x, velocity_y):
        """
            Atualiza o estado lógico e a imagem visual da entidade.

            Args:
                is_moving (bool): Indica se há entrada de movimento horizontal.
                on_ground (bool): Indica se a entidade está tocando uma plataforma.
                velocity_x (float): Velocidade atual no eixo X.
                velocity_y (float): Velocidade atual no eixo Y.
        """

        # Verifica se o gatinho levou splash da vovó
        if self.is_dead:
            self.state = "DEATH"

        # Verifica se a vovó deu splashada no gatinho, tadinho
        elif self.is_attacking:
            # Temos que validar o lado que o ataque veio, para garantir que
            # a animação da vovó seja para o lado correto
            if self.hit_right:
                self.state = "ATTACK_RIGHT"
            elif not self.hit_right:
                self.state = "ATTACK_LEFT"

        # Se nada anterior aconteceu, vamos verificar o pulo do Taquinho
        elif not on_ground and abs(velocity_y) > 2:
            # Validamos o lado que o Taquinho está andando, para garantir
            # a animação para o lado correto
            if velocity_x > 0:
                self.state = "RIGHT_JUMP"
            elif velocity_x < 0:
                self.state = "LEFT_JUMP"
            else:
                self.state = "IDLE_JUMP"

        # Verificamos pra qual lado o Taquinho vai, para garantir a animação correta
        elif is_moving:
            self.state = "RIGHT_WALK" if velocity_x > 0 else "LEFT_WALK"

        # Se ele não tá fazendo nada disso, está parado.
        else:
            self.state = "IDLE"


        # Motor das animações
        self.anim_timer += 1        # Conta quantos frames se passaram

        # Só muda de frame quando o temporizador chegar no mesmo valor que a velocidade
        if self.anim_timer >= self.anim_speed:
            self.anim_timer = 0     # Reinicia o timer
            self.frame_index += 1   # Muda o frame


        # Mapeamento de animações
        animation_map = {
            "IDLE": self.idle_frames,
            "RIGHT_WALK": self.right_walk_frames,
            "LEFT_WALK": self.left_walk_frames,
            # Observe que no caso dos frames opcionais, foi usado o inserido ou
            # caso seja None, o frame idle (obrigatório). Isso evita erros de NoneType
            "RIGHT_JUMP": self.right_jump_frames or self.idle_frames,
            "LEFT_JUMP": self.left_jump_frames or self.idle_frames,
            "IDLE_JUMP": self.idle_jump_frames or self.idle_frames,
            "DEATH": self.hit_frames or self.idle_frames,
            "ATTACK_RIGHT": self.right_attack_frames or self.idle_frames,
            "ATTACK_LEFT": self.left_attack_frames or self.idle_frames,
        }

        # Usamos o .get para garantir que, para algum estado diferente dos mencionados
        # anteriormente (não presentes no dicionário), sejam substituídos pelo frame idle
        frames = animation_map.get(self.state, self.idle_frames)

        # Agora vamos aplicar as animações (passar os frames)
        if frames:
            # Quando passar todos os frames da lista, volta para o início
            self.image = frames[self.frame_index % len(frames)]

class Kitten(Entity):
    def __init__(self, pos):
        """
            Inicializa o gatinho com seus frames de animação e atributos de física.

            Args:
                pos (tuple): Posição inicial (x, y) no cenário.
        """
        # Define as animações obrigatórias para o Taquinho
        idle = [f'kitten/idle/idle-{i}' for i in [4,5]]
        right_walk = [f'kitten/walk-right/walk-right-{i}' for i in range(1,9)]
        left_walk = [f'kitten/walk-left/walk-left-{i}' for i in range(1,9)]

        # Define as animações opcionais que o Taquinho vai usar
        hit_frames = [f'kitten/hit/hit-{i}' for i in range(1, 5)]
        right_jump = [f'kitten/right-jump/jump-{i}' for i in range(1,6)]
        left_jump = [f'kitten/left-jump/jump-{i}' for i in range(1,6)]
        idle_jump = [f'kitten/idle-jump/jump-{i}' for i in range(1,6)]

        # Instancia os atributos de Entity
        super().__init__(pos, idle, right_walk, left_walk,
                         right_jump_frames=right_jump,
                         left_jump_frames=left_jump,
                         idle_jump_frames=idle_jump,
                         hit_frames=hit_frames)

        # Definimos aqui os atributos específicos do Taquinho
        self.speed = 4
        self.vel_y = 0
        self.gravity = 0.6
        self.on_ground = False
        self.is_moving = False
        self.lives = MAX_LIVES
        self.collected_balls = 0

    def update(self, platforms, balls):
        """
            Executa a atualização lógica do jogador a cada frame do jogo.

            Args:
                platforms (list): Lista de objetos Platform para verificação de colisão.
                balls (list): Lista de objetos Ball (itens coletáveis).
        """

        # Reseta atributos do Taquinho
        self.is_moving = False
        self.on_ground = False

        # Aplica a gravidade
        self.vel_y += self.gravity
        self.y += self.vel_y

        # Variável auxiliar para velocidade final em X
        vx = 0

        # Se o Taquinho não tiver sendo splashado, garante os movimentos para ambos os lados
        if self.state != "DEATH":
            if keyboard.d or keyboard.right:
                self.x += self.speed
                vx = self.speed
                self.is_moving = True
            elif keyboard.a or keyboard.left:
                self.x -= self.speed
                vx = -self.speed
                self.is_moving = True

        # Em cada uma das plataformas/chão, verifica se o Taquinho encosta nela
        # (na hitbox padrão)
        for platform in platforms:
            if self.colliderect(platform):
                # Só colide se estiver a descer (vel_y > 0)
                if self.vel_y > 0:
                    # Verifica se o Taquinho estava acima da plataforma no frame anterior
                    # (evita que ele "suba" pela lateral)
                    if (self.y - self.vel_y) <= platform.top:
                        self.bottom = platform.top + 3  # Pequeno fine-tuning para garantir
                                                        # que o gatinho não fique flutuando
                        self.vel_y = 0
                        self.on_ground = True
                        break

        # Verifica se o Taquinho pegou o novelo
        for ball in balls:
            if self.colliderect(ball):
                self.collected_balls += 1
                balls.remove(ball)

                # # Ajusta os volumes dos miados
                # sounds.meow_ball_1.set_volume(0.8)
                # sounds.meow_ball_2.set_volume(0.2)
                # sounds.meow_ball_3.set_volume(0.8)
                #
                # # Varia o som pseudoaleatoriamente
                # aux = random.randint(0, 2)
                # if aux == 0:
                #     sounds.meow_ball_1.play()
                # elif aux == 1:
                #     sounds.meow_ball_2.play()
                # elif aux == 2:
                #     sounds.meow_ball_3.play()

        # Garante que o gatinho não saia nas laterais da tela
        if self.left < 0:
            self.left = 0
        if self.right > WIDTH:
            self.right = WIDTH

        # Sincroniza a animação
        self.update_animation(self.is_moving, self.on_ground, vx, self.vel_y)

class Enemy(Entity):
    def __init__(self, pos, distance):
        """
            Inicializa a vovó com seus frames específicos e parâmetros.

            Args:
                pos (tuple): Coordenadas (x, y) iniciais.
                distance (int): Raio de patrulha (distância que percorre para cada lado).
        """
        # Define as animações obrigatórias para a vovó
        idle = [f'enemy/idle/enemy-idle-{i}' for i in [1,4]]
        right_walk = [f'enemy/walk-right/enemy-walk-right-{i}' for i in range(1, 5)]
        left_walk = [f'enemy/walk-left/enemy-walk-left-{i}' for i in range(1, 5)]

        # Define as animações opcionais que a vovó vai usar
        right_attack_frames = [f'enemy/attack-right/enemy-attack-{i}' for i in range(1, 4)]
        left_attack_frames = [f'enemy/attack-left/enemy-attack-{i}' for i in range(1, 4)]

        # Instancia os atributos de Entity
        super().__init__(pos, idle, right_walk, left_walk,
                         right_attack_frames=right_attack_frames,
                         left_attack_frames=left_attack_frames)

        # Definimos aqui os atributos específicos da vovó
        self.start_x = pos[0]
        self.distance = distance
        self.direction = 1
        self.speed = 1
        self.is_attacking = False
        self.attack_timer = 0.0

    def update(self):
        """ Atualiza a lógica de comportamento e animação da vovó. """
        if self.is_attacking:
            # Verificamos o tempo que a animação fica sendo executada
            self.attack_timer -= 1
            if self.attack_timer <= 0:
                self.is_attacking = False  # Quando o tempo acaba, para de atacar
        else:
            # A vovó só se movimenta quando não está atacando
            self.x += self.speed * self.direction
            if abs(self.x - self.start_x) >= self.distance:
                self.direction *= -1

        # Sincroniza a animação
        self.update_animation(not self.is_attacking, True, self.direction, 0)

class Ball(Actor):
    def __init__(self, imgs, pos):
        """
            Inicializa o item coletável com sua lista de animações e posição.

            Args:
                imgs (list): Lista de frames da animação.
                pos (tuple): Coordenadas (x, y) de posicionamento no nível.
        """
        super().__init__(imgs[0], pos)
        self.frames = imgs
        self.frame_index = 0
        self.animation_timer = 0
        self.animation_speed = 10

    def update(self):
        """ Atualiza o estado visual do item. """
        self.animation_timer += 1
        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0
            self.frame_index = random.randint(0,3)
            self.image = self.frames[self.frame_index % len(self.frames)]

class Platform(Actor):
    def __init__(self, img, pos):
        """
            Inicializa uma plataforma ou bloco de chão.

            Args:
                img (str): O nome do asset visual ou caminho da imagem.
                pos (tuple): Coordenadas (x, y) de posicionamento no mundo.
        """
        super().__init__(img, pos)

# @TODO: docstring
class Button(Actor):
    def __init__(self, img, pos):
        super().__init__(img, pos)
