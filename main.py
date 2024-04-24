import chess
import chess.svg
import cairosvg
import pygame
from PIL import Image, ImageTk
import io
import os

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

    hasClickOnce = False
    hasClickTwice = False
    move_str = ""
    while not hasClickOnce:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                os.remove(board_path) 
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos_x, pos_y = event.pos
                pos_x-=15 # Attention à bien remettre à 0 les coordonnées du clic à la souris (à cause de la bordure de 15 pixels du plateau de jeu)
                pos_y-=15
                if pos_x >= 0 and pos_y >= 0 and pos_x <= window_size[0]-30 and pos_y <= window_size[1]-30:
                    hasClickOnce = True
                    move_str += chr(97 + pos_x//45)
                    move_str += str(8 - pos_y//45)
        if hasClickOnce :
            while not hasClickTwice:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        os.remove(board_path) 
                        pygame.quit()
                        quit()
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        hasClickTwice = True
                        pos_x, pos_y = event.pos
                        pos_x-=15 # Attention à bien remettre à 0 les coordonnées du clic à la souris (à cause de la bordure de 15 pixels du plateau de jeu)
                        pos_y-=15
                        if pos_x >= 0 and pos_y >= 0 and pos_x <= window_size[0]-30 and pos_y <= window_size[1]-30:
                            hasClickTwice = True
                            move_str += chr(97 + pos_x//45)
                            move_str += str(8 - pos_y//45)
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


    
    
