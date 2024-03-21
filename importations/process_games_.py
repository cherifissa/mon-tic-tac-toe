from keras.models import load_model
import math
import random
import numpy as np

from importations.get_outcome_ import get_outcome
from importations.one_hot_ import one_hot 

reward_dep = .7

def process_games(games, model, model_2, x_train):
    xt = 0  # Compteur pour les victoires du joueur X
    ot = 0  # Compteur pour les victoires du joueur O
    dt = 0  # Compteur pour les matchs nuls
    states = []  # Liste des états du jeu
    q_values = []  # Liste des valeurs Q correspondantes
    states_2 = []  # Liste des états du jeu pour le joueur 2
    q_values_2 = []  # Liste des valeurs Q correspondantes pour le joueur 2

    # Parcourir chaque partie de jeu
    for game in games:
        # Calculer la récompense totale en fonction du résultat du jeu
        total_reward = get_outcome(game[-1])
        if total_reward == -1:
            ot += 1  # Incrémenter le compteur de victoires du joueur O
        elif total_reward == 1:
            xt += 1  # Incrémenter le compteur de victoires du joueur X
        else:
            dt += 1  # Incrémenter le compteur de matchs nuls

        # Parcourir chaque étape du jeu
        for i in range(0, len(game) - 1):
            if i % 2 == 0:
                # Pour les étapes paires, correspondant au joueur X
                for j in range(9):
                    if game[i][j] != game[i + 1][j]:
                        # Si la case a changé entre deux étapes consécutives
                        reward_vector = np.zeros(9)
                        reward_vector[j] = total_reward * (reward_dep ** (math.floor((len(game) - i) / 2) - 1))
                        states.append(game[i].copy())  # Ajouter l'état du jeu à la liste des états
                        q_values.append(reward_vector.copy())  # Ajouter la valeur Q correspondante à la liste des valeurs Q
            else:
                # Pour les étapes impaires, correspondant au joueur O
                for j in range(9):
                    if game[i][j] != game[i + 1][j]:
                        # Si la case a changé entre deux étapes consécutives
                        reward_vector = np.zeros(9)
                        reward_vector[j] = -1 * total_reward * (reward_dep ** (math.floor((len(game) - i) / 2) - 1))
                        states_2.append(game[i].copy())  # Ajouter l'état du jeu à la liste des états pour le joueur 2
                        q_values_2.append(reward_vector.copy())  # Ajouter la valeur Q correspondante à la liste des valeurs Q pour le joueur 2

    if x_train:
        # Entraîner le modèle pour le joueur X

        # Préparer les données d'entraînement en mélangeant les états et les valeurs Q
        zipped = list(zip(states, q_values))
        random.shuffle(zipped)
        states, q_values = zip(*zipped)
        new_states = [one_hot(state) for state in states]  # Encoder les états en one-hot encoding

        # Entraîner le modèle avec les données préparées
        model.fit(np.asarray(new_states), np.asarray(q_values), epochs=10, batch_size=32)

        # Sauvegarder le modèle entraîné pour le joueur X
        model.save('tic_tac_toe')

        # Afficher les statistiques du jeu (victoires de X, victoires de O, matchs nuls)
        print("Le joueur X a gagné :", xt)
        print("Le joueur O a gagné :", ot)
        print(f"Il y a {dt} matchs nuls.")

    else:
        # Entraîner le modèle pour le joueur O

        # Préparer les données d'entraînement pour le joueur O en mélangeant les états et les valeurs Q correspondantes
        zipped = list(zip(states_2, q_values_2))
        random.shuffle(zipped)
        states_2, q_values_2 = zip(*zipped)
        new_states = [one_hot(state) for state in states_2]  # Encoder les états en one-hot encoding

        # Entraîner le modèle pour le joueur O avec les données préparées
        model_2.fit(np.asarray(new_states), np.asarray(q_values_2), epochs=10, batch_size=32)

        # Sauvegarder le modèle entraîné pour le joueur O
        model_2.save('tic_tac_toe_2')

        # Afficher les statistiques du jeu (victoires de X, victoires de O, matchs nuls)
        print("Le joueur X a gagné :", xt)
        print("Le joueur O a gagné :", ot)
        print(f"Il y a {dt} matchs nuls.")

    # Inverser la valeur de x_train pour la prochaine itération
    x_train = not x_train

    return x_train
