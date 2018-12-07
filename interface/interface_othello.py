from tkinter import *
from tkinter import colorchooser, messagebox
from othello.partie import Partie
#from time import sleep

difficulte = "Normale"
nb_cases = 8
nb_joueurs = 1
pasfini = True


# ======= TODO STYLE ======= #
# TODO 1- Faire barre d'outils en haut (Menubutton()?)
# TODO 2- Faire en sorte que clic dessine pièce MILIEU de la case
# TODO 3- Faire plus belle pièce
# TODO

#
# ======= TODO FONCTIONS ======= #
# TODO 1- convertir la position demandée sur le GUI Format (A, 1) en format
# TODO    (0, 0) avant de la valider ou de la jouer
# TODO 2- À chaque coup demandé, verifier avec self.partie.exceptions
# TODO 3- Établir des conditions if qui disent à quelle case appartient le clic
# TODO 4- Établir le centre de chaque case pour y mettre la pièce
# TODO 5- Gérer cas où joueur ferme le toplevel sans réponse

# === Définition des objets esclaves et de leurs éléments de style === #

# class BarreDoutils(MenuButton):
#     """Barre d'outils contenant les options de sauvegarde, chargement,
#     etc"""
#     def __init__(self, boss, **kwargs):
#         Menubutton.__init__(self, boss, **kwargs)


class Color:
    color = "black"

    def choisir_couleur(self):
        clr = colorchooser.askcolor(title="Sélectionnez la couleur de votre choix")
        if None not in clr:
            self.color = clr[1]
        else:
            self.color = "black"


    def afficher_couleur(self):
        return str(self.color)


couleur = Color()


class Bouton(Button):
    """Classe définissant le style des boutons utilisés dans le jeu"""
    def __init__(self, boss, **kwargs):

        Button.__init__(self, boss, bg="dark grey", fg="black", bd=5,
                        activebackground=couleur.afficher_couleur(),
                        activeforeground="black",
                        font='Helvetica', **kwargs)


class Glissoir(Scale):
    """Classe définissant le style des glissoirs gradués"""
    def __init__(self, boss, **kwargs):
        Scale.__init__(self, boss, **kwargs)


class PlancheDeJeu(Canvas):
    """
    le damier, n'accepte présentement que des nombres pair de largeur de
    carrées, ex largeur de 6, 8, 10, 12 carrées de large
    """
    def __init__(self, boss):
        Canvas.__init__(self, boss, width=500, height=500)
        self.nb_cases = boss.nb_cases
        self.largeur = boss.largeur

    def dessiner_carres(self):
        self.largeur = 500 // self.nb_cases
        x, y = 1, 1
        for i in range(1, self.nb_cases + 1):
            if i % 2 != 0:
                for j in range(self.nb_cases//2):
                    self.create_rectangle(x, y, x + self.largeur, y + self.largeur,
                                          fill=couleur.afficher_couleur())
                    x += self.largeur
                    self.create_rectangle(x, y, x + self.largeur, y + self.largeur,
                                          fill="white")
                    x += self.largeur
            else:
                for j in range(self.nb_cases//2):
                    self.create_rectangle(x, y, x + self.largeur, y + self.largeur,
                                          fill="white")
                    x += self.largeur
                    self.create_rectangle(x, y, x + self.largeur, y + self.largeur,
                                          fill=couleur.afficher_couleur())
                    x += self.largeur
            x = 1
            y += self.largeur


class Historique(Frame):
    """Défini la zone de texte avec l'historique des coups joués"""
    def __init__(self, root, width=25, height=25):
        Frame.__init__(self, root, bd=2, bg='white',
                       width=width, height=height, relief=SUNKEN)
        self.text = Text(self, font='Helvetica', bg='white', bd=1, width=width,
                         height=height)
        scroll = Scrollbar(self, bd=1, command=self.text.yview)
        self.text.configure(yscrollcommand=scroll.set)
        self.text.pack(side=LEFT, expand=YES, fill=BOTH, padx=2, pady=2)
        scroll.pack(side=RIGHT, expand=YES, fill=BOTH, padx=2, pady=2)

    def ajouter_texte(self, action_a_ecrire):
        """Écrit le message demandé dans la zone historique de coup"""
        self.text.insert(END, action_a_ecrire + "\n")


class ScoreActuel(Label):
    def __init__(self, boss):
        Label.__init__(self, boss, font='Helvetica', text="score: ")

    def changer_score(self, score_a_ecrire):
        self.labelText = ('1.0', score_a_ecrire)


# ====== Définition des fenêtres popup ====== #

class FenJoueurs(Toplevel):
    """
    Fenêtre satellite contenant les boutons pour choisir combien de joueurs
    humains participeront à la partie
    """
    def __init__(self, boss):
        super().__init__(boss)
        self.boss = boss
        self.transient(boss)
        self.grab_set()

        self.geometry("250x250+550+250")  # 300x300 dimension+posX+posY
        self.resizable(width=0, height=0)  # empeche resize
        self.attributes('-topmost', 'true')
        Bouton(self, text="1 joueur", command=self.unjoueur).pack(pady=5, padx=10)
        Bouton(self, text="2 joueurs", command=self.deuxjoueurs).pack(pady=5, padx=10)
    def unjoueur(self):
        """ouvre une FenNiveauDif si 1 joueur choisi"""
        self.nb_joueurs = 1
        self.grab_release()
        self.master.focus_set()
        self.destroy()

    def deuxjoueurs(self):
        """ouvre FenTypePartie si 2 joueurs"""
        self.nb_joueurs = 2
        self.grab_release()
        self.master.focus_set()
        self.destroy()


class FenNiveauDif(Toplevel):
    """
    Fenêtre satellite contenant les boutons pour choisir le niveau de
    difficulté des parties à 1 joueur.
    """
    def __init__(self, boss):
        super().__init__(boss)
        self.boss = boss
        self.transient(boss)
        self.grab_set()

        self.geometry("250x250+550+250")
        self.resizable(width=0, height=0)
        self.attributes('-topmost', 'true')
        Bouton(self, text="Normal", command=self.set_easy).pack(pady=15, padx=10)
        Bouton(self, text="Difficile", command=self.set_hard).pack(pady=15, padx=10)
        Bouton(self, text="Légendaire", command=self.set_legend).pack(pady=15, padx=10)

    def set_easy(self):
        self.difficulte = "Normal"
        self.grab_release()
        self.master.focus_set()
        self.destroy()

    def set_hard(self):
        self.difficulte = "Difficile"
        self.grab_release()
        self.master.focus_set()
        self.destroy()

    def set_legend(self):
        self.difficulte = "Légendaire"
        self.grab_release()
        self.master.focus_set()
        self.destroy()


class FenTypePartie(Toplevel):
    """
    Fenêtre satellite contenant les boutons pour choisir le type de partie
    soit classique ou personnalisée
    """
    def __init__(self, boss):
        super().__init__(boss)
        self.boss = boss
        self.transient(boss)
        self.grab_set()

        self.geometry("250x250+550+250")
        self.resizable(width=0, height=0)
        self.attributes('-topmost', 'true')
        Bouton(self, text="Partie Classique", command=self.partie_classique).\
            pack(pady=5, padx=10)
        Bouton(self, text="Partie Personalisée", command=self.partie_perso).\
            pack(pady=5, padx=10)

    def partie_classique(self):
        self.type_partie = 'classique'
        self.grab_release()
        self.master.focus_set()
        self.destroy()

    def partie_perso(self):
        self.type_partie = 'perso'
        self.grab_release()
        self.master.focus_set()
        self.destroy()


class FenPartiePerso(Toplevel):
    """
    Fenêtre satellite contenant les options de personnalisations lorsque le
    joueur choisi de faire une partie personnalisée
    """
    def __init__(self, boss):
        super().__init__(boss)
        self.boss = boss
        self.transient(boss)
        self.grab_set()

        self.geometry("250x250+550+250")
        self.attributes('-topmost', 'true')
        Label(self, text="Combien de cases?").pack(padx=20, pady=20, fill=X)
        self.gliss = Glissoir(self, orient=HORIZONTAL, relief=SUNKEN, bd=2, from_=6,
                 to_=12, tickinterval=2, resolution=2)
        self.gliss.pack(padx=20, pady=20, fill=X)
        Bouton(self, text="jouer", command=self.set_perso).\
            pack(padx=20, pady=20, fill=X)

    def set_perso(self):
        """Envoie les paramètres choisis par l'utilisateur"""
        self.nb_cases = self.gliss.get()
        self.grab_release()
        self.master.focus_set()
        self.destroy()


# ====== Définition de la fenêtre maîtresse ====== #

class Brothello(Tk):
    """Classe de la fenêtre principale du jeu"""
    def __init__(self):
        """Constructeur de la fenêtre principale"""
        super().__init__()

        # Caractérisiques de la fenêtre principale
        self.title("Brothello")
        self.geometry("800x600+550+250")
        self.resizable(height=0, width=0)
        bout_conseil = Bouton(self, text="Voir les coups possibles",
                              command=self.conseil, state=DISABLED)
        bout_conseil.grid(row=0, column=0, padx=5, pady=5, sticky=W)
        bout_newgame = Bouton(self, text="Nouvelle partie",
                              command=self.nouvelle_partie,state=DISABLED)
        bout_newgame.grid(row=1, column=2, padx=5, pady=5, sticky=W+E)
        bout_abandon = Bouton(self, text="Abandonner", command=self.abandon,
               state=DISABLED)
        bout_abandon.grid(row=2, column=2, padx=5, pady=5, sticky=W+E)
        ScoreActuel(self).grid(row=0, column=2, sticky=W)
        self.histo = Historique(self, height=21)
        self.histo.grid(row=3, column=2, padx=10, pady=5, sticky=W+E)

        # Gestion couleur du board
        couleur.choisir_couleur()
        fond = "#"
        number = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        for i in range(1, 7):
            if couleur.color[i] not in number:
                fond += couleur.color[i]
            else:
                fond += "9"
        Brothello.config(self, bg=fond)

        # Définition des caractéristiques de la partie par défaut
        self.nb_cases = 8
        self.difficulte = 'Normal'
        self.type_partie = 'perso'
        self.nb_joueurs = 1
        self.largeur = 500//self.nb_cases

        # Popups choix options du jeu
        fen_joueur = FenJoueurs(self)
        self.wait_window(fen_joueur)
        self.nb_joueurs = fen_joueur.nb_joueurs
        if self.nb_joueurs == 1:
            fen_diff = FenNiveauDif(self)
            self.wait_window(fen_diff)
            self.difficulte = fen_diff.difficulte
            fen_type = FenTypePartie(self)
            self.wait_window(fen_type)
            self.type_partie = fen_type.type_partie
        elif self.nb_joueurs == 2:
            fen_type = FenTypePartie(self)
            self.wait_window(fen_type)
            self.type_partie = fen_type.type_partie
        else:
            fen_joueur = FenJoueurs(self)  # Si erreur nb_joueurs redemande
            self.wait_window(fen_joueur)
            self.nb_joueurs = fen_joueur.nb_joueurs
        if self.type_partie == 'classique':
            self.nb_cases = 8
        elif self.type_partie == 'perso':
            fen_perso = FenPartiePerso(self)
            self.wait_window(fen_perso)
            self.nb_cases = fen_perso.nb_cases
        else:
            fen_perso = FenPartiePerso(self)  # Si erreur redemande nb_cases
            self.wait_window(fen_perso)
            self.nb_cases = fen_perso.nb_cases
        # Création de l'instance du jeu et du canevas
        self.largeur = 500//self.nb_cases
        self.partie = Partie(self.nb_joueurs, self.difficulte, self.nb_cases)
        self.damier = PlancheDeJeu(self)
        self.damier.grid(row=2, column=0, rowspan=3, padx=5, pady=5)
        self.damier.bind("<Button-1>", self.pointeur)
        self.damier.dessiner_carres()

        # Activation des éléments de l'interface
        bout_newgame.config(state=NORMAL)
        bout_abandon.config(state=NORMAL)
        bout_conseil.config(state=NORMAL)

    def pointeur(self, event):
        """ Dessine une pièce (gros rond laid) où on clique"""
        # TODO plus belles pièces

        # coordonnées (x, y) de la case en range (0, nb_cases) ex (0, 4)
        case_clic = (event.x//self.largeur, event.y//self.largeur)
        print(case_clic, "Case choisie")  # print pour fins de tests
        mid_x = event.x - event.x % self.largeur + self.largeur//2
        mid_y = event.y - event.y % self.largeur + self.largeur//2
        r = self.largeur//5*2
        self.damier.create_oval(mid_x-r, mid_y-r, mid_x+r, mid_y+r,
                                fill='black')

    def conseil(self):
        """ Dira à l'utilisateur les coups possibles """
        # TODO marche pas encore

        if self.difficulte == "Normal":
            coups_possibles = self.partie.coups_possibles
            if not coups_possibles or len(coups_possibles) < 1:
                coups_possibles = "aucun coup possible"
            self.histo.ajouter_texte("Les coups possibles sont:{}".format(
                coups_possibles))
        else:
            self.histo.ajouter_texte(" Aide seulement disponible en difficulté"
                                     " normale! Débrouillez-vous! ")

    def abandon(self):
        self.histo.ajouter_texte("Le joueur {} abandonne la partie! ".format(
            self.partie.couleur_joueur_courant))

    def nouvelle_partie(self):
        """ Démarre une nouvelle partie (Redémarre l'application) """
        # TODO marche pas probablement parce que c'est pas le main qu'il repart
        self.destroy()
        le_jeu = Brothello()
        le_jeu.mainloop()



