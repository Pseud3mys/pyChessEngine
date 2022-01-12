import numpy as np
from matplotlib import pyplot as plt
import matplotlib as mpl
import ChessEngine as e


def affichage(matrice: [[int]], d=1):
    '''Fonction permettant d'afficher une grille représentée par une matrice
    Entrée : une matrice carrée de taille n
    Sortie : Rien'''
    colors = ['black', 'yellow', 'red', 'blue']
    bounds = [0, 1, 2, 3, 4]
    cmap = mpl.colors.ListedColormap(colors)
    norm = mpl.colors.BoundaryNorm(bounds, cmap.N)

    plt.clf()  # Nettoie l'affichage si besoin
    plt.imshow(matrice, cmap=cmap, norm=norm, interpolation='nearest')  # Affiche la grille
    ######## Mise en forme des axes de la grille pour que ce soit "joli" ########
    axes = plt.gca()
    n = len(matrice)
    axes.xaxis.set_ticks([-0.5 + i for i in range(n)])
    axes.yaxis.set_ticks([-0.5 + i for i in range(n)])
    axes.xaxis.set_ticklabels([])
    axes.yaxis.set_ticklabels([])
    plt.grid()
    #############################################################################
    plt.ion()  # Affichage dynamique
    plt.pause(d)  # Temps de pause pour que l'affichage dynamique laisse le temps d'observer les évolutions du jeu

# py Chess/test.py


print("Start !")
g = e.ChessGame()
while True:
    g.play_next(deleteQuestion=True)
    #print(g.board)
