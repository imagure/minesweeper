import re
from board import BoardPosition, MineSweeperBoard

def changeBoard(width, height,  chosen_position, board):
    if chosen_position:
        chosen_board_position = BoardPosition(chosen_position)

        for i in range(height):
            for j in range(width):
                current_board_position = BoardPosition((i+1, j+1))

                if current_board_position.isEqualTo(chosen_board_position) and \
                   board.positionHasBomb(current_board_position):

                    board.bombPosition(current_board_position)
                    return "LOST"

                elif current_board_position.isEqualTo(chosen_board_position) and \
                     not board.positionHasBomb(current_board_position):

                    bombs_quantity = board.getBombsQuantityFromPosition(current_board_position)
                    board.clearPosition(current_board_position)

    if board.isVictorious():
        return "VICTORY"
    return "CONTINUE"


def main():
    print("---------   Bem vindo ao Campo Minado !!!  ---------")

    width = int(input("\n Qual a largura desejada para o campo? \n --> "))
    height = int(input("\n Qual a altura desejada para o campo? \n --> "))
    bombs_quantity = int(input("\n Qual a quantidade de bombas desejada? \n --> "))

    board = MineSweeperBoard(width, height, bombs_quantity)
    chosen_position = None

    input_regex = re.compile(r'\d\d')

    while(True):
        game_status = changeBoard(width, height,
                                  chosen_position,
                                  board)
        board.printBoard()

        if game_status!="CONTINUE":
            break

        user_input = input("\n \nEscolha uma posição na forma \"LinhaColuna\" \n --->")

        if input_regex.match(user_input):
            line = int(user_input[0])
            column = int(user_input[1])
            chosen_position = (line, column)
        else:
            if user_input.upper()=="EXIT":
                game_status="EXIT"
                break
            print("\n [Erro] Você forneceu uma entrada inválida! Tente novamente!! \n")

    if game_status=="VICTORY":
        print("\n\n\nPARABÉNS! VOCÊ VENCEU!!")
    elif game_status=="LOST":
        print("\n\n\nPOXA! VOCÊ PERDEU!!")
    elif game_status=="EXIT":
        print("\n\n\nVOCÊ DEIXOU O JOGO! JOGUE NOVAMENTE DEPOIS!!")

    print("\n\n---------   FIM DO JOGO!!!   ---------")

main()
