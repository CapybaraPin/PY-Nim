import pygame
import random

# Initialisation de Pygame
pygame.init()

# Création de la fenêtre
screen = pygame.display.set_mode((720, 400))

# Titre de la fenêtre
pygame.display.set_caption("Jeu de Nim")

# Définition des coordonnées et du rayon des cercles
circles = [(80*i, 200, 25) for i in range(1, 9)]

# Définition des possibilités
L = []

for y in range(8):
    L.append([])
    for z in range(1,4):
        L[y].append(z)

#L = [[1,2,3], [2,3], [3], [], [1], [1,2,3], [1,2,3], [1,2,3]]

# Définition des couleurs
yellow = (232, 203, 53)
red = (255, 87, 51)

# Fonction permettant l'affichage de texte
def displayText(text, x, y, size):
    """
    L'affichage d'un texte sur pygame étant redondant, cette fonction simplifie fortement la tache.

    Paramètres : 
        - text:str: Ce que vous voulez afficher comme texte
        - x:int: La coordonnée en x de votre texte
        - y:int: La coordonnée en y de votre texte
        - size:int: La taille de votre texte
    """

    font = pygame.font.Font('Inter-Medium.ttf', size)
    text_display = font.render(text, True, (0, 0, 0))
    text_rect = text_display.get_rect()
    text_rect.center = (x, y)
    screen.blit(text_display, text_rect)

def possbilityList(L):
    """
        Affiche au dessus des cercles les possibilités que l'odinateur peut encore jouer.

        Paramètres :
            - L:list: La liste de liste comportant les possibilités.
    """

    for i in range(len(L)):

        for k in range(len(L[i])):

            displayText(str(L[i][k]), 80+(i*80), 100+(k*20), 15)

def reload():
    """
        Permet de recommencer une partie en rechargant les cercles.

    :return: la liste des cercles
    """

    circles = [(80 * i, 200, 25) for i in range(1, 9)]

    return circles

actions = ""
last = None


win_rate = 0
total_games = 0

# Boucle principale
active = True
while active:

    # Gestion des événements
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            active = False

    # Affichage du fond en blanc
    screen.fill((249, 249, 233))

    # Dessin des cercles
    num_red_circles = 0
    
    displayText("Machine : " + str(win_rate) + " / " + str(total_games), 60, 20, 15)

    for i, circle in enumerate(circles):

        # Vérification si la souris est sur le cercle
        if pygame.mouse.get_pos()[0] >= circle[0] - circle[2] and pygame.mouse.get_pos()[0] <= circle[0] + circle[2] and pygame.mouse.get_pos()[1] >= circle[1] - circle[2] and pygame.mouse.get_pos()[1] <= circle[1] + circle[2]:
            # Si la souris est sur le cercle, les cercles à droite deviennent rouges

            if i > len(circles)-4:
                num_red_circles = 1
                pygame.draw.circle(screen, red, circle[:2], circle[2])

                for j in range(i+1, len(circles)):
                    if num_red_circles < 3:
                        pygame.draw.circle(screen, red, circles[j][:2], circles[j][2])
                        num_red_circles += 1
                    else:
                        pygame.draw.circle(screen, yellow, circles[j][:2], circles[j][2])

                if pygame.mouse.get_pressed()[0] == 1:
                    actions = f"Vous avez retiré {num_red_circles} jetons."
                    
                    # Si le joueur n'a pas gagné alors on retire le montant de jetons qu'il a sélectionné
                    if num_red_circles < len(circles):
                        for i in range(num_red_circles):
                            circles.pop()

                        # La machine joue
                        indice = len(circles)-1
                        
                        # Vérifie que la liste n'est pas vide
                        if len(L[indice]) == 0:

                            # Vérifie que la liste de la dernière action n'est pas vide
                            if L[last[0]] != []:
                                
                                # On supprime le dernier élement joué par la machine qui amène à la liste vide
                                L[last[0]].remove(last[1])

                            actions = f"Bravo : Vous avez gagné ! (Ordi tombé sur L4)"
                            total_games += 1                               
                            
                            # On relance une partie
                            circles = reload()

                        
                        else:
                            # On pioche parmis les possibilités
                            n = random.choice(L[indice])                                
                                
                            last = indice, n

                            # Si la machine ne gagne pas alors on retire les jetons
                            if n < len(circles):
                                for i in range(n):
                                    circles.pop()
                                    
                                actions = f"La machine retire {n} jetons!"

                            # Sinon la machine à gagnée
                            elif n >= len(circles):
                                actions = f"Dommage ! La machine a gagnée!"
                                
                                total_games += 1
                                win_rate += 1
                                
                                # On relance une partie
                                circles = reload()
                                
                    # Sinon je joueur à gagné
                    elif num_red_circles >= len(circles):
                        
                        actions = f"Bravo : Vous avez gagné !"
                        total_games += 1
                               
                        # On supprime le dernier coup de la machine
                        L[indice].remove(n)
                        
                        # On relance la partie
                        circles = reload()

                break
            else:
                pygame.draw.circle(screen, yellow, circle[:2], circle[2])
        else:
            # Si la souris n'est pas sur le cercle, tous les cercles sont jaunes
            pygame.draw.circle(screen, yellow, circle[:2], circle[2])

    # Affichage des différentes actions et messages
    displayText(actions, 720 / 2, 350, 20)

    # Affichage de la liste des possibilités
    possbilityList(L)

    pygame.display.flip()

pygame.quit()
