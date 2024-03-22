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

# Fonction pour entraîner le modèle
def train():
    global x_train 
    jouer = True
    while jouer:
        # Initialisation du plateau de jeu, de la liste des parties et de la partie actuelle
        board = [0, 0, 0, 0,  0, 0, 0, 0, 0]
        games = []
        current_game = []

        # Affichage de l'indicateur x_train
        print(x_train)
        # Nombre total de parties à jouer
        total_games = 1000
        # Paramètre de l'epsilon-greedy
        e_greedy = .7

        # Boucle pour chaque partie à jouer
        for i in range(0, total_games):
            playing = True
            nn_turn = True
            c = 0
            board = [0, 0, 0, 0,  0, 0, 0, 0, 0]
            current_game = []
            current_game.append(board.copy())
            nn_board = board

            # Boucle pour chaque tour de jeu dans la partie
            while playing:
                if nn_turn:
                    # Exploration ou exploitation pour le joueur basé sur epsilon-greedy
                    # Si le nombre aléatoire est inférieur ou égal à e_greedy, l'IA choisit un mouvement aléatoire
                    if random.uniform(0, 1) <= e_greedy:
                        choosing = True
                        # Tant que le choix n'a pas été effectué, sélectionner un mouvement aléatoire valide
                        while choosing:
                            c = random.randint(0, 8)
                            if board[c] == 0:
                                choosing = False
                                board[c] = 1
                                current_game.append(board.copy())
                    # Sinon, l'IA choisit le meilleur mouvement en fonction de ses prédictions
                    else:
                        pre = model.predict(np.asarray([one_hot(board)]), batch_size=1)[0]
                        highest = -1000
                        num = -1
                        # Recherche du meilleur mouvement disponible
                        for j in range(0, 9):
                            if board[j] == 0:
                                if pre[j] > highest:
                                    highest = pre[j].copy()
                                    num = j

                        # Mise à jour du plateau avec le meilleur mouvement sélectionné
                        choosing = False
                        board[num] = 1
                        current_game.append(board.copy())

                else:
                    # Exploration ou exploitation pour l'adversaire basé sur epsilon-greedy
                    # Si le nombre aléatoire est inférieur ou égal à e_greedy, l'IA choisit un mouvement aléatoire
                    if random.uniform(0, 1) <= e_greedy:
                        choosing = True
                        # Tant que le choix n'a pas été effectué, sélectionner un mouvement aléatoire valide
                        while choosing:
                            c = random.randint(0, 8)
                            if board[c] == 0:
                                choosing = False
                                board[c] = -1
                                current_game.append(board.copy())
                    # Sinon, l'IA choisit le meilleur mouvement en fonction de ses prédictions
                    else:
                        pre = model_2.predict(np.asarray([one_hot(board)]), batch_size=1)[0]
                        highest = -1000
                        num = -1
                        # Recherche du meilleur mouvement disponible
                        for j in range(0, 9):
                            if board[j] == 0:
                                if pre[j] > highest:
                                    highest = pre[j].copy()
                                    num = j

                        # Mise à jour du plateau avec le meilleur mouvement sélectionné
                        choosing = False
                        board[num] = -1
                        current_game.append(board.copy())


                # Vérification de la possibilité de jouer sur le plateau
                playable = False
                for square in board:
                    if square == 0:
                        playable = True

                # Vérification de l'issue de la partie
                if not get_outcome(board) == 0:
                    playable = False

                # Si le plateau n'est pas jouable, la partie est terminée
                if not playable:
                    playing = False

                # Changement de tour
                nn_turn = not nn_turn

            # Ajout de la partie actuelle à la liste des parties
            games.append(current_game)

            # Affichage de la taille de la liste des parties
            print("la taille de games est :", len(games))

        # Traitement des parties pour entraîner les modèles
        x_train = process_games(games, model, model_2, x_train)
        # Fin de l'entraînement
        jouer = False

# Fonction pour jouer une partie contre l'IA
def play():
    print('')
    print('Un nouveau jeu commence !')
    print('')

    # Sélection du camp pour le joueur humain
    team = input('Choisissez un camp : (x/o) ')
    print('')

    # Initialisation du plateau de jeu et des variables de jeu
    board = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    running = True
    x_turn = True

    # Boucle principale du jeu
    while running:
        # Tour de l'IA ou du joueur humain en fonction de x_turn et du camp choisi
        if (x_turn and team == 'o') or (not x_turn and not team == 'o'):
            # Sélection du mouvement par l'IA
            if team == 'o':
                pre = model.predict(np.asarray([one_hot(board)]))[0]
            elif team == 'x':
                pre = model_2.predict(np.asarray([one_hot(board)]))[0]

            # Recherche du meilleur mouvement
            highest = -1000
            num = -1
            for j in range(0, 9):
                if board[j] == 0:
                    if pre[j] > highest:
                        highest = pre[j].copy()
                        num = j

            # Affichage des prédictions de l'IA
            print(pre)

            # Mise à jour du plateau avec le mouvement sélectionné par l'IA
            if team == 'o':
                board[num] = 1
            elif team == 'x':
                board[num] = -1
            x_turn = not x_turn
            print('IA pense...')
        else:
            # Tour du joueur humain
            move = int(input('Entrez le mouvement : '))
            if board[move] == 0:
                if team == 'o':
                    board[move] = -1
                elif team == 'x':
                    board[move] = 1
                x_turn = not x_turn
            else:
                print('Mouvement invalid!')

        # Affichage du plateau de jeu
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

        # Vérification si le plateau est plein
        full = True
        for square in board:
            if square == 0:
                full = False

        # Vérification de l'issue de la partie
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


