import chess

plateau = chess.Board()

while not plateau.is_checkmate(): # True si le joueur à qui c'est le tour est en échec et mat
    if plateau.turn : 
        print("Au tour des blancs !")
    else:
        print("Au tour des noirs !")

    move_str = input("Rentrez votre prochain coup ('q' pour quitter, 'l' pour voir la liste des coups, 'p' pour voir le plateau) : ")
    if move_str == "q":
        quit()
    elif move_str  == "l":
        moveAllowed = list(plateau.legal_moves)
        for move in moveAllowed:
            print(move)
    elif move_str  == "p":
        print("Voici le plateau : ")
        print(plateau)
    else:
        nextMove = chess.Move.from_uci(move_str)
        moveAllowed = plateau.legal_moves
        if nextMove in moveAllowed:
            if plateau.is_capture(nextMove):
                destination = nextMove.to_square
                capturePiece = plateau.piece_at(destination)
                print("Vous avez capturé un " + str(capturePiece) + " adverse en " + chess.square_name(destination))

            plateau.push_uci(move_str)
            print("Vous avez saisi un coup valide: " + move_str + ". Voici le plateau : ")
            print(plateau)
        else :
            print("Coup non autorisé : " + move_str + ", réessayer")


    
    
