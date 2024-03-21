from keras.models import Sequential
from keras.layers import Dense
from keras.models import load_model
import random
import numpy as np

from importations.get_outcome_ import get_outcome
from importations.one_hot_ import one_hot 
from importations.process_games_ import process_games

from AgentDQN import AgentDQN

reward_dep = .7
x_train = True

model = AgentDQN()
model_2 = AgentDQN()

try:
    model = load_model('tic_tac_toe.h5')
    model_2 = load_model('tic_tac_toe_2.h5')
    print('Modèle existant trouvé... chargement des données.')
except:
    pass

# win = 1; draw = 0; loss = -1 --> moves not taken are 0 in q vector

mode = input('Choisissez un mode : (training/playing) ')

def train():
    global x_train 
    jouer = True
    while jouer:
        board = [0, 0, 0, 0,  0, 0, 0, 0, 0]
        games = []
        current_game = []

        print(x_train)
        total_games = 400
        e_greedy = .7

        for i in range(0, total_games):
            playing = True
            nn_turn = True
            c = 0
            board = [0, 0, 0, 0,  0, 0, 0, 0, 0]
            current_game = []
            current_game.append(board.copy())
            nn_board = board

            while playing:
                if nn_turn:
                    if random.uniform(0, 1) <= e_greedy:
                        choosing = True
                        while choosing:
                            c = random.randint(0, 8)
                            if board[c] == 0:
                                choosing = False
                                board[c] = 1
                                current_game.append(board.copy())
                    else:
                        pre = model.predict(np.asarray([one_hot(board)]), batch_size=1)[0]
                        highest = -1000
                        num = -1
                        for j in range(0, 9):
                            if board[j] == 0:
                                if pre[j] > highest:
                                    highest = pre[j].copy()
                                    num = j

                        choosing = False
                        board[num] = 1
                        current_game.append(board.copy())

                else:
                    if random.uniform(0, 1) <= e_greedy:
                        choosing = True
                        while choosing:
                            c = random.randint(0, 8)
                            if board[c] == 0:
                                choosing = False
                                board[c] = -1
                                current_game.append(board.copy())
                    else:
                        pre = model_2.predict(np.asarray([one_hot(board)]), batch_size=1)[0]
                        highest = -1000
                        num = -1
                        for j in range(0, 9):
                            if board[j] == 0:
                                if pre[j] > highest:
                                    highest = pre[j].copy()
                                    num = j

                        choosing = False
                        board[num] = -1
                        current_game.append(board.copy())

                playable = False

                for square in board:
                    if square == 0:
                        playable = True

                if not get_outcome(board) == 0:
                    playable = False

                if not playable:
                    playing = False

                nn_turn = not nn_turn

            games.append(current_game)

            print("la taille de games est :", len(games))

        x_train = process_games(games, model, model_2, x_train)
        jouer = False

def play():
    print('')
    print('Un nouveau jeu commence !')
    print('')

    team = input('Choisissez un camp : (x/o) ')
    print('')

    board = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    running = True
    x_turn = True
    while running:
        if (x_turn and team == 'o') or (not x_turn and not team == 'o'):
            if team == 'o':
                pre = model.predict(np.asarray([one_hot(board)]))[0]
            elif team == 'x':
                pre = model_2.predict(np.asarray([one_hot(board)]))[0]
            print('')
            highest = -1000
            num = -1
            for j in range(0, 9):
                if board[j] == 0:
                    if pre[j] > highest:
                        highest = pre[j].copy()
                        num = j

            print(pre)

            if team == 'o':
                board[num] = 1
            elif team == 'x':
                board[num] = -1
            x_turn = not x_turn
            print('IA pense...')
        else:
            move = int(input('Entrez le mouvement : '))
            if board[move] == 0:
                if team == 'o':
                    board[move] = -1
                elif team == 'x':
                    board[move] = 1
                x_turn = not x_turn
            else:
                print('Mouvement invalid!')

        r_board = []

        for square in board:
            if square == 0:
                r_board.append('-')
            elif square == 1:
                r_board.append('x')
            elif square == -1:
                r_board.append('o')

        print(r_board[0], r_board[1], r_board[2])
        print(r_board[3], r_board[4], r_board[5])
        print(r_board[6], r_board[7], r_board[8])

        full = True

        for square in board:
            if square == 0:
                full = False

        if full:
            running = False
            if get_outcome(board) == 0:
                print('Le jeu était nul !')

        if not get_outcome(board) == 0:
            running = False
            print(get_outcome(board), 'a gagné le jeu!')

if mode == 'training':
    train()
elif mode == 'playing':
    play()


