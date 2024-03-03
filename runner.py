import pygame
import sys
import time

import game as g  # Import du module du jeu

# Initialisation de pygame
pygame.init()

# Définition de la taille de la fenêtre
size = width, height = 600, 400

# Couleurs utilisées pour la grille et les textes
color1 = (50, 50, 50)
color2 = (255, 255, 255)

# Création de la fenêtre
screen = pygame.display.set_mode(size)

# Définition des polices
mediumFont = pygame.font.Font("Merriweather-Black.ttf", 28)
largeFont = pygame.font.Font("Merriweather-Black.ttf", 40)
moveFont = pygame.font.Font("Merriweather-Black.ttf", 60)

# Initialisation de la grille du jeu
board = g.initial_start()
user = None  # Joueur actuel
ai_turn = False  # Indique si c'est au tour de l'IA

# Boucle principale du jeu
while True:
    # Gestion des événements
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    # Remplissage de l'écran avec la couleur de fond
    screen.fill(color1)

    # Permet à l'utilisateur de choisir un joueur
    if user is None:
        # Affichage du titre du jeu
        title = largeFont.render("Jouer à Tic-Tac-Toe", True, color2)
        titleRect = title.get_rect()
        titleRect.center = ((width / 2), 50)
        screen.blit(title, titleRect)

        # Affichage des boutons pour choisir X ou O
        playXButton = pygame.Rect((width / 8), (height / 2), width / 4, 50)
        playX = mediumFont.render("Jouer X", True, color1)
        playXRect = playX.get_rect()
        playXRect.center = playXButton.center
        pygame.draw.rect(screen, color2, playXButton)
        screen.blit(playX, playXRect)

        playOButton = pygame.Rect(5 * (width / 8), (height / 2), width / 4, 50)
        playO = mediumFont.render("Jouer O", True, color1)
        playORect = playO.get_rect()
        playORect.center = playOButton.center
        pygame.draw.rect(screen, color2, playOButton)
        screen.blit(playO, playORect)

        # Vérification si un bouton est cliqué
        click, _, _ = pygame.mouse.get_pressed()
        if click == 1:
            mouse = pygame.mouse.get_pos()
            if playXButton.collidepoint(mouse):
                time.sleep(0.2)
                user = g.X
            elif playOButton.collidepoint(mouse):
                time.sleep(0.2)
                user = g.O

    else:
        # Affichage de la grille de jeu
        tile_size = 80
        tile_origin = (width / 2 - (1.5 * tile_size),
                       height / 2 - (1.5 * tile_size))
        tiles = []
        for i in range(3):
            row = []
            for j in range(3):
                rect = pygame.Rect(
                    tile_origin[0] + j * tile_size,
                    tile_origin[1] + i * tile_size,
                    tile_size, tile_size
                )
                pygame.draw.rect(screen, color2, rect, 3)

                if board[i][j] != g.EMPTY:
                    move = moveFont.render(board[i][j], True, color2)
                    moveRect = move.get_rect()
                    moveRect.center = rect.center
                    screen.blit(move, moveRect)
                row.append(rect)
            tiles.append(row)

        # Vérification de la fin du jeu
        game_over = g.terminal(board)
        player = g.player(board)

        # Affichage du titre approprié
        if game_over:
            winner = g.winner(board)
            if winner is None:
                title = f"Égalité !"
            else:
                title = f"Perdu : {winner} a gagné."
        elif user == player:
            title = f"Jouer comme {user}"
        else:
            title = f"l'IA réfléchi..."
        title = largeFont.render(title, True, color2)
        titleRect = title.get_rect()
        titleRect.center = ((width / 2), 30)
        screen.blit(title, titleRect)

        # Si c'est le tour de l'IA, effectuer un mouvement
        if user != player and not game_over:
            if ai_turn:
                time.sleep(0.5)
                move = g.minimax(board)
                board = g.result(board, move)
                ai_turn = False
            else:
                ai_turn = True

        # Vérification du mouvement de l'utilisateur
        click, _, _ = pygame.mouse.get_pressed()
        if click == 1 and user == player and not game_over:
            mouse = pygame.mouse.get_pos()
            for i in range(3):
                for j in range(3):
                    if (board[i][j] == g.EMPTY and tiles[i][j].collidepoint(mouse)):
                        board = g.result(board, (i, j))

        # Si le jeu est terminé, afficher le bouton pour rejouer
        if game_over:
            againButton = pygame.Rect(width / 3, height - 65, width / 3, 50)
            again = mediumFont.render("Rejouer", True, color1)
            againRect = again.get_rect()
            againRect.center = againButton.center
            pygame.draw.rect(screen, color2, againButton)
            screen.blit(again, againRect)
            click, _, _ = pygame.mouse.get_pressed()
            if click == 1:
                mouse = pygame.mouse.get_pos()
                if againButton.collidepoint(mouse):
                    time.sleep(0.2)
                    user = None
                    board = g.initial_start()
                    ai_turn = False

    # Rafraîchir l'écran
    pygame.display.flip()
