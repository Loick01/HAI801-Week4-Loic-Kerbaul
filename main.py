import chess
import chess.svg
import cairosvg
import pygame
from PIL import Image, ImageTk
import io
import os
import time

choixModeJeu = int(input("Saisir le mode de jeu : 1 (Jeu à 2 joueurs), 2 (Jeu contre IA) --> "))

valeurPieces = {chess.PAWN: 1, chess.KNIGHT: 3.25, chess.BISHOP: 3.25, chess.ROOK: 5, chess.QUEEN: 9.75, chess.KING: 0}

def evaluationBoard(board): # Permettra d'évaluer les coups possibles pour choisir le meilleur possible
    valeur = 0
    for p in board.piece_map().values():
        valeur += valeurPieces.get(p.piece_type, 0) * (-1 if p.color == chess.WHITE else 1)
    return valeur

def hill_climbing(board):
    bestMove = None
    bestEvaluate = float('-inf')

    for move in board.legal_moves:
        board.push(move) 
        eval_move = evaluationBoard(board)    

        caseTo = move.to_square
        piece = board.piece_at(caseTo)
        if piece.piece_type == chess.PAWN:
            eval_move += 0.04


        if eval_move > bestEvaluate:
            bestMove = move
            bestEvaluate = eval_move
        board.pop() 

    print("Meilleur score : " + str(bestEvaluate))
    return bestMove

plateau = chess.Board()
board_path = "board.png"

svg_data = chess.svg.board(plateau)
cairosvg.svg2png(bytestring=svg_data, write_to=board_path)

pygame.init()

boardImg = pygame.image.load(board_path)
window_size = boardImg.get_rect().size

window = pygame.display.set_mode(window_size)
pygame.display.set_caption("Jeu échecs")

window.blit(boardImg, (0, 0))
pygame.display.update()

while not plateau.is_checkmate(): # True si le joueur à qui c'est le tour est en échec et mat
    if plateau.turn : 
        print("Au tour des blancs !")
    else:
        print("Au tour des noirs !")
        if choixModeJeu==2 : # Les pions noirs sont joués par l'IA (juste hill climbing pour l'instant)
            plateau.push(hill_climbing(plateau))
            svg_data = chess.svg.board(plateau)
            cairosvg.svg2png(bytestring=svg_data, write_to=board_path)
            boardImg = pygame.image.load(board_path)
            window.blit(boardImg, (0, 0))

            pygame.display.update()
            time.sleep(0.5) # Délai avant lequel le joueur peut jouer
            continue


    hasClickOnce = False
    hasClickTwice = False
    move_str = ""
    arrow_start = ()
    arrow_end = ()
    while not hasClickOnce:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                os.remove(board_path) 
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos_x, pos_y = event.pos
                pos_x-=15 # Attention à bien remettre à 0 les coordonnées du clic à la souris (à cause de la bordure de 15 pixels du plateau de jeu)
                pos_y-=15
                if pos_x >= 0 and pos_y >= 0 and pos_x <= window_size[0]-30 and pos_y <= window_size[1]-30:
                    hasClickOnce = True
                    move_str += chr(97 + pos_x//45)
                    move_str += str(8 - pos_y//45)
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                hasClickOnce = True
                arrow_start = event.pos
        if hasClickOnce :
            while not hasClickTwice:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        os.remove(board_path) 
                        pygame.quit()
                        quit()
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        hasClickTwice = True
                        pos_x, pos_y = event.pos
                        pos_x-=15 # Attention à bien remettre à 0 les coordonnées du clic à la souris (à cause de la bordure de 15 pixels du plateau de jeu)
                        pos_y-=15
                        if pos_x >= 0 and pos_y >= 0 and pos_x <= window_size[0]-30 and pos_y <= window_size[1]-30:
                            hasClickTwice = True
                            move_str += chr(97 + pos_x//45)
                            move_str += str(8 - pos_y//45)
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                        hasClickTwice = True
                        arrow_end = event.pos
    
    if len(arrow_start) == 2 and len(arrow_end) == 2:
        pygame.draw.line(window, (255, 255, 255), arrow_start, arrow_end, 10)
        pygame.display.update()
        continue
    if move_str[0:2] == move_str[2:4] or len(move_str) != 4:
        continue


    '''
    move_str = input("Saisir une commande ('q' pour quitter, 'l' pour voir la liste des coups, 'p' pour voir le plateau) : ")
    if move_str == "q":
        quit()
    elif move_str  == "l":
        moveAllowed = list(plateau.legal_moves)
        for move in moveAllowed:
            print(move)
    elif move_str  == "p":
        print("Voici le plateau : ")
        svg_data = chess.svg.board(plateau)
        png_data = cairosvg.svg2png(bytestring=svg_data)
    '''

    nextMove = chess.Move.from_uci(move_str)
    moveAllowed = plateau.legal_moves
    if nextMove in moveAllowed:
        if plateau.is_capture(nextMove):
            destination = nextMove.to_square
            capturePiece = plateau.piece_at(destination)
            print("Vous avez capturé un " + str(capturePiece) + " adverse en " + chess.square_name(destination))

        plateau.push_uci(move_str)
        print("Coup valide : " + move_str)
    else :
        print("Coup non autorisé : " + move_str + ", réessayez")
    
    svg_data = chess.svg.board(plateau)
    cairosvg.svg2png(bytestring=svg_data, write_to=board_path)
    boardImg = pygame.image.load(board_path)

    window.blit(boardImg, (0, 0))

    pygame.display.update()


    
    
