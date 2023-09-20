import pygame
import numpy as np
import random

class game(object):
    def __init__(self):

        # Initialisation de pygame
        pygame.init()

        # Dimensions de la grille
        self.largeur = 100
        self.hauteur = 100
        self.case_taille = 40  # Taille en pixels de chaque case

        # Dimensions de la fenetre
        self.largeur_fenetre = 1000
        self.hauteur_fenetre = 1000

        self.zoom = 100  # zoom
        self.souris = False  # souris pressée ?
        self.x, self.y = pygame.mouse.get_pos()  # position de la souris
        self.timespentdown = 0  # temps passé a appuyer
        self.camX = 0 # position de la caméra X
        self.camY = 0 # position de la caméra Y

        self.inventorySize = 500 # taille de l'inventaire des cellules

        self.run = False # jeu en cours d'execution 

        # Creation de la fenetre
        self.fenetre = pygame.display.set_mode((self.largeur_fenetre, self.hauteur_fenetre))
        pygame.display.set_caption("Simulation de cellule")


        # Cretion de la grille avec numpy
        self.grille = np.zeros((self.hauteur, self.largeur, self.inventorySize + 1), dtype=object)

        # Types de molecules de base et leurs noms
        self.molecules_de_base = np.array(("H2O", "O2", "CO2", "C6O6H12", "H2", "C21H28N7O17P3", "C10H15N5O10P2", "C10H16N5O13P3", "C21H29N7O17P3", "H3O4P", "H+", "Ca2+",
                                            "K+", "Na+", "Cl-", "SO4^2-", "SiO2", "NO3-", "NO2-", "NH3", "NH4+", "PGA", "G3P", "RuBP"))
        self.molecules_de_base_nom = np.array(("eau", "O2", "CO2", "Glucose", "H2", "NADP+", "ADP", "ATP", "NADPH", "Pi", "Ions Hydrogene",
                                                "Ions Calcium", "Ions Potassium", "Ions Sodium", "Ions Chlorure", "Ions Sulfate", "Ions Silicone", "Nitrite", "Nitrate", 
                                                "Ammoniac", "Ion Ammonium", "PGA", "G3P", "RuBP"))

        self.atomes_de_base = np.array(("H","C","O","N","P","Mg"))

        # Liste des couts de construction des morceaux de cellule pour les automatismes futures et les stats (couleur, inventaire etc...)
        #idée : proton pump, 
        self.stats_cellule = np.array((
            ["membrane", 50, 40, 30, 5, 5, 0, 0, 0, 200, 1],
            ["cytoplasm", 50, 40, 30, 5, 5, 0, 150, 150, 255, 1],
            ["light harvesting complex", 100, 50, 30, 20, 0, 10, 255, 255, 0, 0],
            ["CO2 fixing complex", 0, 0, 0, 0, 0, 0, 200, 60, 40, 0],
            ["PGA reduction complex", 0, 0, 0, 0, 0, 0, 50, 150, 50, 0],
            ["RuBP regenerator", 0, 0, 0, 0, 0, 0, 150, 150, 50, 0],
            ["ATP package", 0, 0, 0, 0, 0, 0, 218, 112, 214, 0],
            ["NADPH package", 0, 0, 0, 0, 0, 0, 147, 112, 219, 0],
            ["PGA package", 0, 0, 0, 0, 0, 0, 100, 88, 120, 0],
            ["Evacuation tube", 0, 0, 0, 0, 0, 0, 255, 88, 120, 0],
            ["Eradicate cell", 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            ["autre", 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]))
        #yep this shit is horrible to read but it's easy to add new stuffs to it 
        #qui?, lumiére?, id element 1, quantitée élément 1, id element 2, quantitée élément 2 etc... x 10 
        #puis id résultat 1, quantité 1, id résultat 2, quantité 2... x 10 puis le total d'éléments crées et consomé
        self.stats_cellules_cosomation_production = np.array(([3, 1, 1, 2, 6, 2, 7, 3, 10, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 1, 9, 2, 8, 3, 11, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10, 8],
                                                              [4, 0, 24, 3, 3, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 22, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 6, 6],
                                                              [5, 0, 22, 6, 8, 6, 9, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 23, 6, 6, 6, 7, 6, 10, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 18, 24])) 
        
        self.cellSelected = 1 # id de la cellule sélectionnée

        self.moovingchance = 10 # chance de mouvement d'une molecule 10 = 1/10






########################################################################





    def afficher_grille(self):
        # Efface la fenêtre avec une couleur blanche
        self.fenetre.fill((255, 255, 255))

        # Parcourt toutes les cellules de la grille
        for i in range(self.hauteur):
            for j in range(self.largeur):
                x = j * (self.case_taille + self.zoom / 100) + self.camX #position du carre
                y = i * (self.case_taille + self.zoom / 100) + self.camY

                # Dessine un rectangle vide pour représenter chaque cellule
                pygame.draw.rect(self.fenetre, (200,200,200), (x, y, self.case_taille + self.zoom / 100, self.case_taille + self.zoom / 100))

                # Récupère le contenu de la cellule
                case = self.grille[i, j]

                # Si la cellule n'est pas vide (contient quelque chose)
                if case[0] != 0:
                    # Dessine un rectangle rempli avec la couleur correspondant au type de cellule
                    pygame.draw.rect(self.fenetre, (int(self.stats_cellule[case[0]-1][len(self.atomes_de_base)+1]),int(self.stats_cellule[case[0]-1][len(self.atomes_de_base)+2]),int(self.stats_cellule[case[0]-1][len(self.atomes_de_base)+3])), (x, y, self.case_taille + self.zoom / 100, self.case_taille + self.zoom / 100))

        # Affiche le nom de la cellule sélectionnée en haut à gauche
        font = pygame.font.SysFont(None, 30)
        img = font.render('selected : ' + self.stats_cellule[self.cellSelected-1][0], True, (0, 0, 0))
        self.fenetre.blit(img, (20, 20))

        # Affiche l'état d'exécution du jeu (en cours ou arrêté)
        font = pygame.font.SysFont(None, 30)
        img = font.render('Running : ' + str(self.run), True, (0, 0, 0))
        self.fenetre.blit(img, (20, 60))

        # Met à jour l'affichage de la fenêtre
        pygame.display.update()





########################################################################






    def mainInstruction(self):
        # Initialisation de listes pour stocker les coordonnées des cellules traitées
        lastcellX = np.array([], dtype = int)
        lastcellY = np.array([], dtype = int)
        alreadyseen = set()  # Utilisation d'un ensemble pour stocker les cellules déjà traitées

        # Parcours de la grille pour trouver les cellules actives et enregistrement de leurs coordonnées
        for i in range(self.hauteur - 2):
            for j in range(self.largeur - 2):
                if self.grille[i, j][0] != 0:
                    lastcellX = np.append(lastcellX, i)
                    lastcellY = np.append(lastcellY, j)

        # Parcours des coordonnées des cellules trouvées
        for i in range(len(lastcellX)):
            for n in range(lastcellX[i] - 2, lastcellX[i] + 2, 1):
                for m in range(lastcellY[i] - 2, lastcellY[i] + 2, 1):
                    cell = (n, m)  # Représentation de la cellule sous forme d'un tuple de ses coordonnées

                    # Vérification si la cellule a déjà été traitée
                    if cell in alreadyseen:
                        continue
                    else:
                        alreadyseen.add(cell)  # Ajout de la cellule à l'ensemble des cellules traitées

                        # Traitement spécifique en fonction du type de cellule
                        if self.grille[n, m][0] == 7:
                            self.grille[n, m][0] = 2
                            for k in range(random.randint(25, 50)):
                                self.grille[n][m][random.randint(0, self.inventorySize - 1) + 1] = 8  # ATP
                        if self.grille[n, m][0] == 11:
                            for k in range(self.inventorySize + 1):
                                self.grille[n][m][k] = 0  # Vide
                        if self.grille[n, m][0] == 8:
                            self.grille[n, m][0] = 2
                            for k in range(random.randint(25, 50)):
                                self.grille[n][m][random.randint(0, self.inventorySize - 1) + 1] = 9  # NADPH
                            for k in range(random.randint(25, 50)):
                                self.grille[n][m][random.randint(0, self.inventorySize - 1) + 1] = 11  # H+
                        if self.grille[n, m][0] == 9:
                            self.grille[n, m][0] = 2
                            for k in range(random.randint(10, 25)):
                                self.grille[n][m][random.randint(0, self.inventorySize - 1) + 1] = 22  # PGA

                        # Parcours de l'inventaire des cellules
                        for k in range(self.inventorySize):
                            # Déplacement aléatoire des molécules
                            if random.randint(0,self.moovingchance - 1) == 0:
                                direction = random.randint(0,3)
                                if direction == 0: #direction déplacement
                                    if i < self.hauteur - 1:
                                        choix = random.randint(0,self.inventorySize - 1) #vérification de la zone d'arrivée et de sa disponibilitée
                                        itsok = self.checksmovementsconditions(n, m, n+1, m, self.grille[n][m][k + 1])
                                        if self.grille[n + 1][m][choix + 1] == 0 and itsok:
                                            self.grille[n + 1][m][choix + 1] = self.grille[n][m][k + 1]
                                            self.grille[n][m][k + 1] = 0
                                elif direction == 1:
                                    if j < self.largeur - 1:
                                        choix = random.randint(0, self.inventorySize - 1)
                                        itsok = self.checksmovementsconditions(n, m, n, m + 1, self.grille[n][m][k + 1])
                                        if self.grille[n][m + 1][choix + 1] == 0 and itsok:
                                            self.grille[n][m + 1][choix + 1] = self.grille[n][m][k + 1]
                                            self.grille[n][m][k + 1] = 0
                                elif direction == 2:
                                    if i > 0:
                                        choix = random.randint(0, self.inventorySize - 1)
                                        itsok = self.checksmovementsconditions(n, m, n - 1, m, self.grille[n][m][k + 1])
                                        if self.grille[n - 1][m][choix + 1] == 0 and itsok:
                                            self.grille[n - 1][m][choix + 1] = self.grille[n][m][k + 1]
                                            self.grille[n][m][k + 1] = 0
                                else:
                                    if j > 0:
                                        choix = random.randint(0,self.inventorySize - 1)
                                        itsok = self.checksmovementsconditions(n, m, n, m - 1, self.grille[n][m][k + 1])
                                        if self.grille[n][m - 1][choix + 1] == 0 and itsok:
                                            self.grille[n][m - 1][choix + 1] = self.grille[n][m][k + 1]
                                            self.grille[n][m][k + 1] = 0
                        self.checkrecipe(n, m) # Vérification de si une cellule peux produire des ressources 






########################################################################




    
    def checkrecipe(self, caseX, caseY):
        # Récupère la liste de molécules dans la cellule à la position (caseX, caseY)
        macase = self.grille[caseX][caseY]

        # Parcours toutes les recettes possibles dans stats_cellules_cosomation_production
        for i in range(len(self.stats_cellules_cosomation_production)):
            # Vérifie si la recette n'est pas vide et si l'id de la cellule correspond
            if self.stats_cellules_cosomation_production[i][0] != 0 and self.stats_cellules_cosomation_production[i][0] == macase[0]:
                # Copie la recette pour pouvoir la modifier
                needforspeedprocess = self.stats_cellules_cosomation_production[i].copy()
                # Stocke les indices des éléments à supprimer après le traitement
                needtodeleteafteward = np.array((), dtype=int)
                # Compte le nombre de zéros (emplacements vides) dans la cellule
                zeros = 0
                # Stocke les id des molécules créées par la recette
                truccree = np.array((), dtype=int)

                # Parcours les emplacements de molécules dans la cellule
                for j in range(self.inventorySize - 1):
                    # Vérifie si une molécule dans la recette correspond à une molécule dans la cellule
                    for k in range(5):
                        if needforspeedprocess[2 * k + 2] == macase[j + 1] and macase[j + 1] != 0 and needforspeedprocess[2 * k + 3] > 0:
                            # Décrémente la quantité requise pour cette molécule dans la recette
                            needforspeedprocess[2 * k + 3] -= 1
                            # Ajoute l'indice de la molécule à supprimer après traitement
                            needtodeleteafteward = np.append(needtodeleteafteward, j + 1)
                    
                    # Compte les emplacements vides dans la cellule
                    if macase[j + 1] == 0:
                        zeros += 1

                # Parcours les résultats de la recette
                for k in range(5):
                    for l in range(needforspeedprocess[2 * k + 23]):
                        if needforspeedprocess[2 * k + 22] != 0:
                            # Ajoute les id des molécules créées à la liste
                            truccree = np.append(truccree, needforspeedprocess[2 * k + 22])
                
                # Vérifie si la recette peut être exécutée
                ok = True
                for j in range(5):
                    if needforspeedprocess[2 * j + 3] > 0 or 0 > zeros + needforspeedprocess[len(needforspeedprocess) - 2] - needforspeedprocess[len(needforspeedprocess) - 1]:
                        ok = False

                if ok == True:
                    print(macase[0])  # Affiche l'ID de la cellule

                    # Supprime les molécules de la cellule après traitement
                    for s in range(len(needtodeleteafteward) - 1):
                        self.grille[caseX][caseY][needtodeleteafteward[s]] = 0

                    # Ajoute les molécules créées à la cellule
                    for s in range(len(truccree)):
                        l = 0
                        end = 0
                        while l < self.inventorySize and end == 0:
                            if self.grille[caseX][caseY][l + 1] == 0:
                                self.grille[caseX][caseY][l + 1] = truccree[s]
                                end = 1
                            l += 1





########################################################################





    
    def checksmovementsconditions(self, fromX:int, fromY:int, toX:int, toY:int, iam:int):
        # Calcul des mouvements en X et Y
        movementX = toX - fromX
        movementY = toY - fromY
        
        # Variable pour gérer les cas compliqués
        itscomplicated = False
        
        # Liste pour stocker les éléments derrière la cellule en mouvement
        casebehind = []
        
        # Vérifier si la cellule en mouvement est située sur le bord de la grille
        if fromX == 0 or fromY == 0 or fromX == self.hauteur - 1 or fromY == self.largeur - 1:
            itscomplicated = True
        else:
            # Obtenir les informations sur la cellule derrière celle en mouvement
            casebehind = self.grille[fromX - movementX][fromY - movementY][0]

        # Si la cellule de destination est vide
        if self.grille[toX][toY][0] == 0:
            # Si la cellule de départ est vide
            if self.grille[fromX][fromY][0] == 0:
                return True
            # Si la cellule de départ est une membrane
            elif self.grille[fromX][fromY][0] == 1:
                if itscomplicated == False:
                    if casebehind == 0:
                        return True
            # Si la cellule de départ est une tube d'évacuation (id 10)
            elif self.grille[fromX][fromY][0] == 10:
                return True
        
        # Si la cellule de destination est une membrane (id 1)
        elif self.grille[toX][toY][0] == 1:
            # Vérifier les conditions pour déplacer la cellule en cours
            if iam == 0 or iam == 1 or iam == 2:
                if self.grille[fromX][fromY][0] == 0:
                    return True
        
        # Si la cellule de destination est une cytoplasm (id 2)
        elif self.grille[toX][toY][0] == 2:
            # Si la cellule de départ n'est pas une tube d'évacuation (id 10)
            if self.grille[fromX][fromY][0] != 10 and self.grille[fromX][fromY][0] != 0:
                if iam == 0 or iam == 1 or iam == 2:
                    zeros = np.sum(self.grille[toX][toY] == 0) - 1
                    # Si plus de 25% des emplacements sont vides, la molécule peut se déplacer
                    if zeros > self.inventorySize / 4: 
                        return True
                else:
                    return True
        
        # Si la cellule de destination est une light harvesting complex (id 3)
        elif self.grille[toX][toY][0] == 3:
            if iam == 1 or iam == 6 or iam == 7 or iam == 10:
                return True
        
        # Si la cellule de destination est un CO2 fixing complex (id 4)
        elif self.grille[toX][toY][0] == 4:
            if iam == 24 or iam == 3:
                return True
        
        # Si la cellule de destination est un PGA Reduction complex (id 5)
        elif self.grille[toX][toY][0] == 5:
            if iam == 8 or iam == 9 or iam == 22:
                return True
        
        # Si la cellule de destination est un tube d'évacuation (id 10)
        elif self.grille[toX][toY][0] == 10 and self.grille[toX][toY][0] != 0:
            zeros = np.sum(self.grille[toX][toY] == 0) - 1
            # Si moins de 20% des emplacements sont vides et iam n'est pas l'un des types spécifiés, la cellule peut se déplacer
            if zeros < self.inventorySize / 5 and iam != 8 and iam != 7 and iam != 6 and iam != 9 and iam != 10 and iam != 11 and iam != 22 and iam != 23 and iam != 24: 
                return True
            





########################################################################





                



    def mainloop(self):
        for i in range(self.hauteur):
            for j in range(self.largeur):
                for k in range(random.randint(self.inventorySize//6,self.inventorySize//4)):
                    self.grille[i][j][random.randint(0,self.inventorySize - 1) + 1] = 1 #the first is the id of the cell
                for k in range(random.randint(self.inventorySize//8,self.inventorySize//4)):
                    self.grille[i][j][random.randint(0,self.inventorySize - 1) + 1] = 3
                for k in range(random.randint(self.inventorySize/20,self.inventorySize/10)):
                    self.grille[i][j][random.randint(0,self.inventorySize - 1) + 1] = 2
                for l in range(11):
                    for k in range(random.randint(self.inventorySize/50,self.inventorySize/25)):
                        self.grille[i][j][random.randint(0,self.inventorySize - 1) + 1] = 10 + l

        # Boucle principale du jeu
        self.running = True

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 4:
                        self.zoom += 100
                        self.camX -= 8
                        self.camY -= 8

                    elif event.button == 5:
                        self.zoom -= 100
                        self.camX += 8
                        self.camY += 8

                    else:
                        self.souris = True
                        self.x, self.y = pygame.mouse.get_pos()
                        self.primeX = self.camX
                        self.primeY = self.camY
                elif event.type == pygame.MOUSEBUTTONUP:
                    self.souris = False
                    if event.button == 4 or event.button == 5:
                        pass
                    else:
                        if self.timespentdown < 60 and 10 > np.sqrt((self.camX - self.primeX)**2) and 10 > np.sqrt((self.camY - self.primeY)**2):
                            i, j = ((self.y - self.camY) // (self.case_taille + self.zoom / 100)), ((self.x - self.camX) // (self.case_taille + self.zoom / 100))
                            if 0 <= i < self.hauteur and 0 <= j < self.largeur:
                                self.grille[int(i), int(j)][0] = self.cellSelected
                    self.timespentdown = 0
                elif event.type == pygame.TEXTINPUT:
                    if event.text == 'e':
                        if self.cellSelected == 1:
                            self.cellSelected = len(self.stats_cellule) - 1
                        else:
                            self.cellSelected -= 1
                    elif event.text == 'r':
                        if self.cellSelected < len(self.stats_cellule) - 1:
                            self.cellSelected += 1
                        else:
                            self.cellSelected = 1
                    elif event.text == 'a':
                        if self.run == False:
                            self.run = True
                        else:
                            self.run = False
                    elif event.text == 'z':
                        self.x, self.y = pygame.mouse.get_pos()
                        i, j = ((self.y - self.camY) // (self.case_taille + self.zoom / 100)), ((self.x - self.camX) // (self.case_taille + self.zoom / 100))
                        element = np.array([])
                        zeros = 0
                        elementpseudo = np.array([])
                        liste = self.grille[int(i)][int(j)]
                        for k in range(len(liste) - 1):
                            if liste[k + 1] != 0:
                                molecule = self.molecules_de_base_nom[liste[k + 1]-1]
                                if molecule in elementpseudo:
                                    index = np.where(elementpseudo == molecule)[0][0]
                                    element[index] += 1
                                else:
                                    element = np.append(element, 1)
                                    elementpseudo = np.append(elementpseudo, molecule)
                            else: 
                                zeros += 1
                        print("///////////////////////////////////////////")
                        for i in range(len(elementpseudo)):
                            print(elementpseudo[i] + " : " + str(element[i]))
                        print("rempli à " + str((self.inventorySize - zeros)/(self.inventorySize/100)) + "%")


            if self.souris == True:
                self.timespentdown+=1
                self.pos = pygame.mouse.get_pos()
                self.camX += self.pos[0] - self.x
                self.camY += self.pos[1] - self.y
                self.x, self.y = self.pos

            if self.run == True:
                self.mainInstruction()


            self.afficher_grille()



        pygame.quit()


g = game()

g.mainloop()
