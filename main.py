import pgzrun
from pgzero.music import is_playing
from pygame import Rect
from entities import *
from settings import *

# --- Funções auxiliares ---
def load_assets_imgs(item):
    """
        Retorna o caminho das imagens ou listas de frames com base no tipo de item.

        Args:
            item (str): Identificador do recurso
                        (opções aceitas: 'floor', 'short-platform', 'long-platform',
                        'collectable-balls', 'collected-ball', 'background', 'title',
                        'start', 'exit', 'sound-on', 'sound-off').

        Returns:
            list or str: Uma lista de strings para animações ou uma string única
                                 para imagens estáticas.
    """

    try:
        if item == 'floor':
            return [f'assets/floor/platform-mid-{i}' for i in range(1, 6)]
        elif item == 'short-platform':
            return 'assets/platform/platform-4'
        elif item == 'long-platform':
            return 'assets/platform/platform-3'
        elif item == 'collectable-balls':
            return [f'assets/itens/ball-{i}' for i in range(1, 4)]
        elif item == 'collected-ball':
            return 'assets/itens/ball-blue'
        elif item == 'background':
            return 'assets/background/lvl01-bg'
        elif item == 'title':
            return f'assets/menu/title'
        elif item == 'start':
            return f'assets/menu/start-btn'
        elif item == 'exit':
            return f'assets/menu/exit-btn'
        elif item == 'sound-on':
            return f'assets/menu/sound-on-btn'
        elif item == 'sound-off':
            return f'assets/menu/sound-off-btn'
        else:
            raise Exception(f'Entrada \'{item}\' não identificada. Verifique o valor informado.')
    except Exception as e:
        print('Um erro surgiu ao tentar definir as imagens:', e)

def load_platforms():
    """
        Instancia e organiza todos os objetos de plataforma do cenário.

        Gera o chão preenchendo a largura da tela e adiciona
        as plataformas flutuantes em posições predefinidas.

        Returns:
            list: Uma lista contendo todos os objetos da classe Platform.
    """
    try:
        # Vetor que armazena o chão e as plataformas
        platforms = []

        # Array de imagens para o chão
        floor_imgs = load_assets_imgs('floor')

        # Criação do chão, como objeto da classe Plataforma
        for n, i in enumerate(range(0, WIDTH + FLOOR_IMG_WIDTH, FLOOR_IMG_WIDTH)):
            image = floor_imgs[n % len(floor_imgs)]
            platforms.append(Platform(image, pos=(i, FLOOR_POS_Y)))

        # Criação das plataformas flutuantes, também como objetos da classe Plataforma
        platforms.append(Platform(img=load_assets_imgs('short-platform'), pos=PLATFORM1_POS))
        platforms.append(Platform(img=load_assets_imgs('short-platform'), pos=PLATFORM2_POS))
        platforms.append(Platform(img=load_assets_imgs('long-platform'), pos=PLATFORM3_POS))
        platforms.append(Platform(img=load_assets_imgs('short-platform'), pos=PLATFORM4_POS))
        platforms.append(Platform(img=load_assets_imgs('short-platform'), pos=PLATFORM5_POS))
        platforms.append(Platform(img=load_assets_imgs('short-platform'), pos=PLATFORM6_POS))

        return platforms

    except Exception as e:
        print('Um erro surgiu ao tentar gerar as plataformas:', e)

def load_balls():
    """
        Instancia os itens coletáveis (novelos) em suas posições iniciais.

        Returns:
            list: Uma lista contendo objetos da classe Ball com seus respectivos frames.
    """

    try:
        balls = []
        balls_imgs = load_assets_imgs('collectable-balls')
        balls.append(Ball(imgs=balls_imgs, pos=BALL1_POS))
        balls.append(Ball(imgs=balls_imgs, pos=BALL2_POS))
        balls.append(Ball(imgs=balls_imgs, pos=BALL3_POS))
        return balls
    except Exception as e:
        print('Um erro surgiu ao tentar criar os novelos coletáveis:', e)

def load_actors():
    """
        Centraliza a criação e inicialização de todos os personagens e objetos do jogo.

        Esta função atua como um gerenciador de setup, instanciando o herói, os inimigos,
        o cenário (plataformas) e os itens coletáveis de uma só vez.

        Returns:
            tuple: Uma tupla contendo (Player, list[Enemy], list[Platform], list[Ball]),
                   facilitando a atribuição múltipla no início do jogo.
    """
    try:
        # Cria os botões do menu
        btns = []
        btns.append(Button(load_assets_imgs('start'), START_BTN_MENU))
        btns.append(Button(load_assets_imgs('exit'), EXIT_BTN_MENU))
        btns.append(Button(load_assets_imgs('sound-on'), SOUND_BTN_MENU))

        # Cria o objeto Taquinho, o nosso herói
        kitten = Kitten(KITTEN_INIT_POS)

        # Cria os objetos vovó, que não pode nem ver o Taquinho
        enemies = [Enemy(GRANDMA1_INIT_POS, GRANDMA1_DISTANCE),
                   Enemy(GRANDMA2_INIT_POS, GRANDMA2_DISTANCE)]

        # Cria o chão e as plataformas "flutuantes"
        platforms = load_platforms()

        # Cria os novelos a serem coletados pelo Taquinho
        balls = load_balls()

        return btns, kitten, enemies, platforms, balls

    except Exception as e:
        print('Um erro surgiu ao tentar instanciar os Actors():', e)

def reset_kitten():
    """
        Restaura o estado inicial do gatinho após uma colisão.

        Redefine a posição para o ponto de partida, zera a velocidade vertical
        e remove a flag de morte para permitir que o jogador continue.
    """
    # O Taquinho para de se mover verticalmente
    kitten.vel_y = 0

    # Fica vivo de novo
    kitten.is_dead = False

    # E volta para a posição inicial
    kitten.pos = KITTEN_INIT_POS

def draw_modal(state):
    """
        Renderiza a interface de fim de jogo (Vitória ou Derrota) na tela.

        Args:
            state (str): O estado atual do jogo ("WIN" ou "GAME_OVER").

        Raises:
            Exception: Se o game_state não for um dos valores esperados.
    """
    try:
        if state == "WIN":
            title_color = WIN_MODAL_TITLE_GOLD
            edge_color = WIN_MODAL_EDGE

            title = 'Você ganhou!'
            message = 'O Taquinho conseguiu muitos novelos para brincar.'

        elif state == "GAME_OVER":
            title_color = DEFEAT_MODAL_TITLE_RED
            edge_color = DEFEAT_MODAL_EDGE

            title = 'Você perdeu!'
            message = 'O Taquinho ficou muito molhado para continuar...'

        else:
            raise Exception(f'Estado de jogo informado (\'{state}\') não reconhecido na criação do modal.')
    except Exception as e:
        print(f'Erro ao tentar definir modal: {e}')
        exit()

    # Desenha a caixa do modal com a borda
    modal_rect = Rect(MODAL_POSITION, MODAL_SIZE)
    screen.draw.filled_rect(modal_rect, MODAL_BACKGROUND_COLOR)
    screen.draw.rect(modal_rect, edge_color)

    # Escrevendo as mensagens
    screen.draw.text(title, center=MODAL_TITLE_CENTER_POS,
                     fontsize=MODAL_TITLE_FONT_SIZE, color=title_color,
                     shadow=MODAL_TITLE_SHADOW, scolor=MODAL_TITLE_SHADOW_COLOR,
                     fontname=MODAL_FONT)

    screen.draw.text(message, center=MODAL_MESSAGE_CENTER_POS,
                     fontsize=MODAL_MESSAGE_FONT_SIZE, color=MODAL_MESSAGE_COLOR,
                     fontname=MODAL_FONT)

    screen.draw.text(MODAL_INSTRUCTION_TEXT, center=MODAL_INSTRUCTION_CENTER_POS,
                     fontsize=MODAL_INSTRUCTION_FONT_SIZE, color=MODAL_INSTRUCTION_COLOR,
                     fontname=MODAL_FONT)

def on_key_down(key):
    """
        Processa pressões de teclas únicas para ações de jogo e navegação.

        Gerencia o pulo do gatinho durante o jogo e a saída do aplicativo
        nas telas de vitória ou derrota.

        Args:
            key (int): Código da tecla pressionada fornecido pelo Pygame Zero.
    """

    global game_state

    # No estado "PLAYING",
    if game_state == "PLAYING":
        # Verifica o pulo do Taquinho, quando pressiona o espaço
        if key == keys.SPACE and kitten.on_ground:
            kitten.vel_y = -15
            kitten.frame_index = 0
            kitten.on_ground = False

    # Nos estados "GAME_OVER" ou "WIN",
    elif game_state == "GAME_OVER" or game_state == "WIN":
        # Encerra o jogo de pressionado ESC
        if key == keys.ESCAPE:
            exit()

def set_playing():
    """Altera o estado global do jogo para o modo ativo (PLAYING)."""
    global game_state
    game_state = "PLAYING"

def set_win():
    """Altera o estado global do jogo para a tela de vitória (WIN)."""
    global game_state
    game_state = "WIN"

def set_game_over():
    """Altera o estado global do jogo para a tela de derrota (GAME_OVER)."""
    global game_state
    game_state = "GAME_OVER"

def get_bigger_enemy_hitbox(enemy):
    """
        Cria uma área de colisão personalizada e ampliada para uma vovó específica.

        Args:
            enemy (Actor): O objeto da vovó para a qual a hitbox será gerada.

        Returns:
            Rect: Um objeto retangular posicionado ao redor da vovó.
    """
    enemy_hitbox = Rect(enemy.x-45, enemy.y-50, 90, 100)
    return enemy_hitbox

def get_bigger_kitten_hitbox():
    """
        Cria uma área de colisão personalizada e ajustada para o Taquinho (kitten).

        Returns:
            Rect: Um objeto retangular que define a zona de impacto do gato.
    """
    kitten_hitbox = Rect(kitten.x - 28, kitten.y - 30, 56, 50)
    return kitten_hitbox

def get_score_balls():
    """ Renderiza na tela os ícones dos novelos coletados pelo gatinho. """
    for i in range(kitten.collected_balls):
        screen.blit(load_assets_imgs('collected-ball'), (40 + (i - 1) * 35, 10))

def get_lives_hearts():
    """ Renderiza os indicadores de vida (corações) no canto superior direito. """
    for i in range(kitten.lives):
        screen.blit('assets/itens/life-on', (WIDTH - (i + 1) * 35, 10))

    for i in range(3 - kitten.lives):
        screen.blit('assets/itens/life-off', (695 + i * 35, 10))

def debug_mode():
    """ Desenha as hitboxes de colisão na tela para fins de ajuste e teste. """

    # Carrega o hitbox modificado do Taquinho e desenha na tela
    kitten_hitbox = get_bigger_kitten_hitbox()
    screen.draw.rect(kitten_hitbox, color=DEBUG_COLOR)
    for enemy in enemies:
        screen.draw.rect(get_bigger_enemy_hitbox(enemy), color=DEBUG_COLOR)

# @TODO: docstrings
def draw_game():
    # Limpa a tela anterior e desenha o fundo
    screen.clear()
    screen.blit(load_assets_imgs('background'), BACKGROUND_POS)

    # Desenha os hitbox para debugs
    if DEBUG_MODE:
        debug_mode()

    # Desenha as plataformas e chão
    for plat in platforms:
        plat.draw()

    # Desenha as vovós
    for enemy in enemies:
        enemy.draw()

    # Desenha os novelos
    for ball in balls:
        ball.draw()

    # Desenha o Taquinho
    kitten.draw()

    # Desenha o placar (os novelos coletados)
    get_score_balls()

    # Desenha as vidas restantes
    get_lives_hearts()


def draw_menu():
    """Desenha a interface do menu principal."""
    screen.clear()
    screen.blit(load_assets_imgs('background'), BACKGROUND_POS)
    screen.blit(load_assets_imgs('title'), TITLE_POS)

    # Desenha os botões
    for btn in buttons:
        btn.draw()

def on_mouse_down(pos):
    global game_state, sound_on
    if game_state == "MENU":
        play_btn = buttons[0]
        exit_btn = buttons[1]
        sound_btn = buttons[2]

        if play_btn.collidepoint(pos):
            game_state = "PLAYING"
        elif exit_btn.collidepoint(pos):
            exit()

        elif sound_btn.collidepoint(pos):
            if sound_on:
                sound_on = False
            else:
                sound_on = True

# --- Setup de Objetos ---
buttons, kitten, enemies, platforms, balls = load_actors()

game_state = "MENU"
sound_on = True
is_playing = False

def update():
    """
        Controlador principal do loop lógico do jogo.

        Responsabilidades:
        1. Atualizar posições e estados do gatinho (kitten), inimigos e itens (balls)
           apenas quando o estado for "PLAYING".
        2. Gerenciar o sistema de combate: detecta colisões usando uma hitbox
           ampliada para os inimigos e aciona o estado de ataque/morte.
        3. Determinar a direção do impacto (hit_right) para fins de animação do inimigo.
        4. Monitorar condições de término:
            - GAME_OVER: Se as vidas do gatinho chegarem a zero.
            - WIN: Se todos os novelos (3) forem coletados.
            - EXIT: Finaliza a aplicação.
    """
    global game_state

    if not is_playing and sound_on:
        # music.play('background')
        sounds.background.play(-1)
        sounds.background.set_volume(0.1)

    if not sound_on:
        sounds.background.stop()


    # Verifica as vidas do Taquinho (se ele perdeu)
    if kitten.lives == 0:
        set_game_over()

    # Verifica a quantidade de novelos que o Taquinho coletou (se ele ganhou)
    elif kitten.collected_balls == TOT_BALLS:
        set_win()

    # Controle a serem aplicados apenas no estado "PLAYING"
    elif game_state == "PLAYING":

        # Chama o controlador do Taquinho
        kitten.update(platforms, balls)

        # Pega a nova hitbox do gatinho
        kitten_hitbox = get_bigger_kitten_hitbox()

        # Chama o controlador de cada um dos novelos
        for ball in balls:
            ball.update()

        # Chama o controlador para cada uma das vovós, e verifica colisões
        for enemy in enemies:
            enemy.update()

            # Define uma hitbox maior para as vovós e o Taquinho
            enemy_hitbox = get_bigger_enemy_hitbox(enemy)

            # Verifica se eles se encontraram (sem o Taquinho já ter sido acertado)
            if kitten_hitbox.colliderect(enemy_hitbox) and not kitten.is_dead:
                # Atualiza as variáveis, e garante a animação correta
                kitten.is_dead = True
                kitten.lives -= 1
                kitten.frame_index = 0

                # Verifica o lado que o Taquinho encontra a vovó para que a animação seja correta
                if kitten.x > enemy.x:
                    enemy.hit_right = True
                else:
                    enemy.hit_right = False

                # Garante o fim da animação após 48 frames
                enemy.is_attacking = True
                enemy.attack_timer = 72
                enemy.frame_index = 0

                # Ajusta o volume dos sons
                # sounds.angry_cat.set_volume(0.2)

                # Toca os sons
                # sounds.angry_cat.play()

                # "Agenda" a execução do "reset" do taquinho após 1s
                clock.schedule_unique(reset_kitten, 1.2)

def draw():
    """ Responsável por renderizar todos os elementos visuais na tela a cada frame. """
    #HERE:global wait_time

    if game_state == "MENU":
        draw_menu()

    # O que será desenhado na tela quando estivermos no estado "PLAYING"
    elif game_state == "PLAYING": #HERE: or wait_time < 72:
        draw_game()

    elif game_state == "GAME_OVER" or game_state == "WIN":
        #HERE:wait_time += 1
        #HERE:if wait_time >= 72:
        draw_modal(game_state)
pgzrun.go()