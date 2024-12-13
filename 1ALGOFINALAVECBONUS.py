import tkinter as tk
from tkinter import simpledialog, messagebox
import pygame

class Joueur:
    def __init__(self, couleur_reine, couleur_tours):
        self.couleur_reine = couleur_reine
        self.couleur_tours = couleur_tours
        self.position_reine = None
        self.positions_tours = []

    def nombre_pieces(self):
        return 1+len(self.positions_tours)

class Jeu:
    def __init__(self, dimension=8):      
        self.dimension = dimension
        self.plateau = []                 
        for i in range(dimension):      
            ligne = []                    
            for j in range(dimension):    
                ligne.append(None)        
            self.plateau.append(ligne)      

        self.joueur1 = Joueur("purple", "blue")    
        self.joueur2 = Joueur("orange", "red")
        self.joueur_actuel = self.joueur1         
        self.piece_selectionnee = None            
        self.case_selectionnee = None

        self.root = tk.Tk()                       
        self.root.title("Jeu de Tours et Reines")  
        self.canvas = tk.Canvas(self.root, width=900, height=600) 
        self.canvas.pack()               

        self.canvas.bind("<Button-1>", self.selectionner_case)

        self.initialiser_plateau()      
        self.dessiner_plateau()           
        pygame.mixer.init()

    def initialiser_plateau(self):
        n = self.dimension
        mid = n // 2
        self.joueur1.position_reine = (n-1, 0)
        self.plateau[n-1][0] = ("R", "purple")
        for i in range(mid, n):
            for j in range(mid):
                if (i, j) != (n-1, 0):
                    self.plateau[i][j] = ("T", "blue")
                    self.joueur1.positions_tours.append((i, j))
        self.joueur2.position_reine = (0, n-1)
        self.plateau[0][n-1] = ("R", "orange")
        for i in range(mid):
            for j in range(mid, n):
                if (i, j) != (0, n-1):
                    self.plateau[i][j] = ("T", "red")
                    self.joueur2.positions_tours.append((i, j))

    def dessiner_plateau(self):
        self.canvas.delete("all")      
        taille_case = 600 // self.dimension    
        for i in range(self.dimension):       
            for j in range(self.dimension):   
                x1, y1 = j*taille_case, i*taille_case  
                x2, y2 = x1+taille_case, y1+taille_case  
                couleur = "white"                
                if (i, j) == self.case_selectionnee:   
                    couleur = "lightblue"
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=couleur, outline="black") 
                piece = self.plateau[i][j]     
                if piece:                  
                    type_piece, couleur = piece   
                    self.canvas.create_oval(x1 + 5, y1 + 5, x2 - 5, y2 - 5, fill=couleur)
        self.afficher_joueur_actuel()    

    def afficher_joueur_actuel(self):
        self.canvas.delete("joueur_actuel")
        texte = f"Tour de : {'Joueur 1' if self.joueur_actuel == self.joueur1 else 'Joueur 2'}"
        couleur = "black"
        self.canvas.create_text(640, 300, text=texte, font=("Arial", 24), fill=couleur, anchor="w", tag="joueur_actuel")

    def joueur_suivant(self):
        if self.joueur_actuel == self.joueur1:
            self.joueur_actuel = self.joueur2 
        else:
            self.joueur_actuel = self.joueur1
        self.afficher_joueur_actuel()



    def previsualiser_coups_possibles(self):
        if not self.piece_selectionnee:
            return
        type_piece, (ligne_orig, colonne_orig) = self.piece_selectionnee
        taille_case = 600 // self.dimension
        for i in range(self.dimension):
            for j in range(self.dimension):
                if self.deplacement_valide(ligne_orig, colonne_orig, i, j, type_piece):
                    x1, y1 = j * taille_case, i * taille_case
                    x2, y2 = x1 + taille_case, y1 + taille_case
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill="lightgreen", outline="black")

    def selectionner_case(self, event):
        taille_case = 600 // self.dimension
        colonne, ligne = event.x // taille_case, event.y // taille_case
        if (ligne, colonne) == self.case_selectionnee:
            self.case_selectionnee = None
            self.piece_selectionnee = None
            self.dessiner_plateau()
            return
        if self.piece_selectionnee:
            self.deplacer_piece(ligne, colonne)
        elif self.plateau[ligne][colonne]:
            type_piece, couleur = self.plateau[ligne][colonne]
            if (self.joueur_actuel == self.joueur1 and couleur in ["purple", "blue"]) or \
               (self.joueur_actuel == self.joueur2 and couleur in ["orange", "red"]):
                self.piece_selectionnee = (type_piece, (ligne, colonne))
                self.case_selectionnee = (ligne, colonne)
                self.dessiner_plateau()
                self.previsualiser_coups_possibles()

    def deplacement_valide(self, ligne_orig, colonne_orig, ligne, colonne, type_piece):
        if ligne < 0 or ligne >= self.dimension or colonne < 0 or colonne >= self.dimension:
            return False
        if self.plateau[ligne][colonne] is not None:
            return False
        if type_piece == "T":
            if ligne_orig != ligne and colonne_orig != colonne:
                return False
            if ligne_orig == ligne:
                pas = 1 if colonne > colonne_orig else -1
                for c in range(colonne_orig + pas, colonne, pas):
                    if self.plateau[ligne][c] is not None:
                        return False
            elif colonne_orig == colonne:
                pas = 1 if ligne > ligne_orig else -1
                for l in range(ligne_orig + pas, ligne, pas):
                    if self.plateau[l][colonne] is not None:
                        return False
        elif type_piece == "R":
            if ligne_orig == ligne or colonne_orig == colonne:
                return self.deplacement_valide(ligne_orig, colonne_orig, ligne, colonne, "T")
            elif abs(ligne - ligne_orig) == abs(colonne - colonne_orig):
                pas_ligne = 1 if ligne > ligne_orig else -1
                pas_colonne = 1 if colonne > colonne_orig else -1
                l, c = ligne_orig + pas_ligne, colonne_orig + pas_colonne
                while l != ligne and c != colonne:
                    if self.plateau[l][c] is not None:
                        return False
                    l += pas_ligne
                    c += pas_colonne
            else:
                return False
        return True

    def deplacer_piece(self, ligne, colonne):
        if self.piece_selectionnee:
            type_piece, (ligne_orig, colonne_orig) = self.piece_selectionnee
            if self.deplacement_valide(ligne_orig, colonne_orig, ligne, colonne, type_piece):
                self.plateau[ligne][colonne] = self.plateau[ligne_orig][colonne_orig]
                self.plateau[ligne_orig][colonne_orig] = None
                if type_piece == "T":
                    for i, t in enumerate(self.joueur_actuel.positions_tours):
                        if t == (ligne_orig, colonne_orig):
                            self.joueur_actuel.positions_tours[i] = (ligne, colonne)
                            break
                elif type_piece == "R":
                    self.joueur_actuel.position_reine = (ligne, colonne)
                self.capture_tours(ligne, colonne)
                self.piece_selectionnee = None
                self.case_selectionnee = None
                self.joueur_suivant()
                self.dessiner_plateau()
                self.verifier_victoire()


    def capture_tours(self, ligne, colonne):
        reine_l, reine_c = self.joueur_actuel.position_reine
        if self.joueur_actuel == self.joueur1:
            adversaire = self.joueur2 
        else:
            adversaire = self.joueur1
        if ligne != reine_l and colonne != reine_c:
            sommets = [(ligne, reine_c),(reine_l, colonne)]
            for sommet in sommets:
                l, c = sommet
                if self.plateau[l][c] == ("T", adversaire.couleur_tours):
                    self.plateau[l][c] = None  
                    adversaire.positions_tours.remove((l, c))  
                    self.soncapture()
                    
    def soncapture(self):
        son_chemin = r"C:\Users\Vidal\OneDrive\Bureau\TP SUPINFO\Python\piou-piou.mp3"
        pygame.mixer.music.load(son_chemin) 
        pygame.mixer.music.play()         

    def sonvictoire(self):
        son_chemin = r"C:\Users\Vidal\OneDrive\Bureau\TP SUPINFO\Python\victoire.mp3"
        pygame.mixer.music.load(son_chemin) 
        pygame.mixer.music.play()  

    def verifier_victoire(self):
        perdant = "0"
        if self.joueur1.nombre_pieces() <= 2:
            perdant = "2"
        elif self.joueur2.nombre_pieces() <= 2:
            perdant = "1"
        if perdant !="0":
            self.canvas.unbind("<Button-1>") 
            self.afficher_victoire(perdant)
            self.sonvictoire()
            
    def afficher_victoire(self, gagnant):
        self.fenetre_victoire = tk.Toplevel(self.root)
        self.fenetre_victoire.title("Victoire")
        label = tk.Label(self.fenetre_victoire, text=f"Le joueur {gagnant} a gagné !", font=("Arial", 24), fg="green")
        label.pack(pady=20, padx=20)
        bouton = tk.Button(self.fenetre_victoire, text="Relancer une partie", command=self.relancer_partie)
        bouton.pack(pady=10)
        bouton_quitter = tk.Button(self.fenetre_victoire, text="Quitter", command=self.fermer_jeu)
        bouton_quitter.pack(pady=10)
    
    def relancer_partie(self):
        self.root.destroy()
        self.__init__(self.dimension)  
        self.lancer()

    
    def fermer_jeu(self):
        self.root.destroy()

    def reinitialiser_jeu(self):
        self.plateau = []
        for i in range(self.dimension):
            ligne = []
            for j in range(self.dimension):
                ligne.append(None)
            self.plateau.append(ligne)
        self.joueur1 = Joueur("purple", "blue")
        self.joueur2 = Joueur("orange", "red")
        self.joueur_actuel = self.joueur1
        self.piece_selectionnee = None
        self.case_selectionnee = None
        self.initialiser_plateau()
        self.dessiner_plateau()
        self.canvas.bind("<Button-1>", self.selectionner_case) 
    
    def lancer(self):
        self.root.mainloop()

def demander_taille_plateau():
    while True:
        try:
            taille = int(simpledialog.askstring("Configuration", "Entrez la taille du plateau (pair, entre 6 et 12) :"))
            if 6 <= taille <= 12 and taille % 2 == 0:
                return taille
        except (ValueError, TypeError):
            break
        simpledialog.messagebox.showerror("Erreur", "Veuillez entrer une taille valide (6-12, pair).")

jeu = Jeu(demander_taille_plateau())
jeu.lancer()