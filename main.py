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

L = [[1,2,3], [2,3], [3], [], [1], [1,2,3], [1,2,3], [1,2,3]]

# Définition des couleurs
yellow = (226, 207, 16)
red = (255, 0, 0)

# Fonction permettant l'affichage de texte
def displayText(texte, x, y, size):
    """
    L'affichage d'un texte sur pygame étant redondant, cette fonction simplifie fortement la tache.
    """

    font = pygame.font.Font('Inter-Medium.ttf', size)
    texte_affiche = font.render(texte, True, (0, 0, 0))
    texte_rect = texte_affiche.get_rect()
    texte_rect.center = (x, y)
    screen.blit(texte_affiche, texte_rect)

def possbilityList(L):

    for i in range(len(L)):

        for k in range(len(L[i])):

            displayText(str(L[i][k]), 80+(i*80), 100+(k*20), 15)

def reload():
    circles = [(80 * i, 200, 25) for i in range(1, 9)]

    return circles


actions = ""
precedent = None
active = True
while active:

    # Gestion des événements
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            active = False

    screen.fill((255, 255, 255))

    # Dessin des cercles
    num_red_circles = 0

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

                    if num_red_circles < len(circles):
                        for i in range(num_red_circles):
                            circles.pop()

                        # La machine joue
                        indice = len(circles)-1

                        if len(L[indice]) == 0:

                            if L[precedent[0]] != []:
                                L[precedent[0]].remove(precedent[1])

                            actions = f"Bravo : Vous avez gagné ! (Ordi tombé sur L4)"

                            circles = reload()

                        else:

                            if len(L[indice]) == 1:
                                n = L[indice][0]

                            elif len(L[indice]) == 2:
                                n = random.choice([L[indice][0],L[indice][1]])

                            elif len(L[indice]) == 3:
                                n = random.randint(1,3)

                            precedent = indice, n

                            if n < len(circles):
                                for i in range(n):
                                    circles.pop()
                                actions = f"La machine retire {n} jetons!"

                            elif n >= len(circles):
                                actions = f"Dommage ! La machine a gagnée!"
                                circles = reload()

                    elif num_red_circles >= len(circles):
                        actions = f"Bravo : Vous avez gagné !"
                        L[indice].remove(n)
                        circles = reload()

                break
            else:
                pygame.draw.circle(screen, yellow, circle[:2], circle[2])
        else:
            # Si la souris n'est pas sur le cercle, tous les cercles sont jaunes
            pygame.draw.circle(screen, yellow, circle[:2], circle[2])

    displayText(actions, 720 / 2, 350, 20)

    possbilityList(L)

    pygame.display.flip()

pygame.quit()
