#On importe les modules nécessaires
from tkinter import *
import time
from winsound import PlaySound


fen = Tk() #On crée la fenetre
fen.title("Super Pig") #On nomme la fenetre
fen.geometry("800x650") #On donne une dimension a la fenetre
Can = Canvas(fen, width=800, height=600, bg="#3170CE") #On crée un canvas pour afficher les images, le canvas occupe  presque toute la fenetre
Can.place(x=0,y=0) #On place le canvas au coordonnées x=0 y=0 en pixels

T_Score = Label(fen, text="Score :", font="arial 26") #On crée le texte score en bas de la fenetere
T_Score.place(x=600,y=602) #On place le label
NumScore = 0 #Le nombre de points au debut, il est reintialise au debut de chaque niveau
Score = Label(fen, text=NumScore, font="times 26")
Score.place(x=720,y=602)

###Variables###

#On defini chaque image que l'on va utiliser
F_Item_Bottes = PhotoImage(file="Images/Item_Bottes.png")
F_Nuage = PhotoImage(file="Images/Nuage.png")
F_Cactus = PhotoImage(file="Images/Cactus.png")
F_Perdu = PhotoImage(file="Images\PP.png")
F_Fond = PhotoImage(file="Images\Fond.gif")
F_Fond_Bleu = PhotoImage(file="Images\Fond_Bleu.png")
F_Stone2 = PhotoImage(file="Images\Stone2.png")
F_Stone = PhotoImage(file="Images\Stone.png")
F_Brique = PhotoImage(file="Images\Brique.png")
F_Goomba = PhotoImage(file="Images\Goomba.png")
F_Level_1 = PhotoImage(file="Images\Level1.png")
F_Level_1b = PhotoImage(file="Images\Level1b.png")
F_Level_2 = PhotoImage(file="Images\Level2.png")
F_Level_2b = PhotoImage(file="Images\Level2b.png")
F_Drapeau = PhotoImage(file="Images\Arrivee.png")
F_MENU = PhotoImage(file="Images\MENU.png")
F_Fleche = PhotoImage(file="Images\Fleche.png")
F_Fleche_Haut = PhotoImage(file="Images\Fleche_Haut.png")
F_Level_Tuto = PhotoImage(file="Images\Level_Tuto.png")

#On initialise les variables qui ne change pas au cours du jeu
Allow_Musique = True
Etat_Musique = "On"
gravite_P = [0,1]
vPx = 4 #On avance de vPx pixels a chaque deplacement 
vdep = 13 #Le temps que met la fonction du mouvement avant de se repeter avec fen.after(vdep, fonction)
nulle = ()
Can.configure(xscrollincrement=str(vPx)) #On defini l'unite a laquelle le canvas defile, c'est la meme que vPx pour que le Perso reste au meme endroit sur la fenetre

def Perso_Bottes():
	global Bottes_Allow, F_PD0, F_PG0, F_PSG, F_PSD
	
	F_PD0 = PhotoImage(file="Images\PD0B.png")
	F_PG0 = PhotoImage(file="Images\PG0B.png")
	F_PSD = PhotoImage(file="Images\PSDB.png")
	F_PSG = PhotoImage(file="Images\PSGB.png")
	Bottes_Allow = True
	

def Interrupteur_Musique(inutile): #"inutile" est durant tout le programme, une variable qui ne sert à rien mais qui est necessaire pour la variable event
	global Etat_Musique, Allow_Musique
	
	""" Cette fonction permet d'allumer ou d'eteindre la musique """
	
	if Etat_Musique == "On":
		Etat_Musique = "Off"
		Allow_Musique = False 
		Can.itemconfig(T_Etat_Musique, text=Etat_Musique) #On change le texte de la musique
		PlaySound("Musiques\Vide.wav",1)
	else:
		Etat_Musique = "On"
		Allow_Musique = True
		Can.itemconfig(T_Etat_Musique, text=Etat_Musique)
		
def Interrupteur_Musique_MENU(inutile):
	global Etat_Musique, Allow_Musique
	
	""" Meme fonction que Interrupteur_Musique mais qui permet de lancer la musique du Menu lorsqu'on la met sur "on" """
	
	if Etat_Musique == "On":
		Etat_Musique = "Off"
		Allow_Musique = False
		Can.itemconfig(T_Etat_Musique, text=Etat_Musique)
		PlaySound("Musiques\Vide.wav",1) 
	else:
		Etat_Musique = "On"
		Allow_Musique = True
		Can.itemconfig(T_Etat_Musique, text=Etat_Musique)
		PlaySound("Musiques\CreamOnChrome.wav",1) #Lance une musique
		
def Reprendre(inutile):
	global repeat_func, T_Reprendre, T_Menu, Allow_Musique, Active_Pause
	
	""" Fonction qui permet de reprendre le jeu apres pause """
	
	if Allow_Musique == True:
		PlaySound("Musiques\DesertEagle.wav",1)
	
	Active_Pause = False
	Can.delete(T_Reprendre, T_Menu, T_Musique, T_Etat_Musique) #On enleve les textes du mode pause
	repeat_func = True #Les fonctions de mouvement se relance toute seules, cette variable leur permet de se répeter lorsqu'elle est sur True, ici cela empeche qu'elles se répetent
	Mvt_Lateral() #On relance la fonction du mouvement
	Deplacement_Goomba() #On relance le deplacement des ennemis, un ennemi = un goomba (reference a mario)
	
def Retour_MENU(inutile):
	global Allow_Musique

	""" Fonction qui permet de revenir au menu """
	
	if Allow_Musique == True:
		PlaySound("Musiques\CreamOnChrome.wav",1)
	MENU("inutile")
	
def Pause():
	global repeat_func, T_Reprendre, T_Menu, Etat_Musique, T_Musique, T_Etat_Musique, Active_Pause
	
	""" On met le jeu en pause """
	
	Active_Pause = True
	PlaySound("Musiques\Pause.wav",1)
	repeat_func = False 
	fen.unbind_all('<Key>') #On enleve la prise en compte des touches du clavier
	T_Reprendre = Can.create_text(pos_P[0]+200, 100, text="Reprendre", font="arial 32 bold", activefill="red", tag="Tag_Reprendre") #On crée les textes du mode pause
	T_Musique = Can.create_text(pos_P[0]+180, 300, text="Musique :", font="arial 32 bold")
	T_Etat_Musique = Can.create_text(pos_P[0]+330, 300, text=Etat_Musique, font="arial 32 bold",activefill="red", tag="Tag_Musique")
	T_Menu = Can.create_text(pos_P[0]+200, 500, text="Retour au menu", font="arial 32 bold", activefill="red", tag="Tag_Menu")
	
	Can.tag_bind("Tag_Musique", "<Button-1>", Interrupteur_Musique) #On associe aux tags une fonction, lorsqu'on clique sur un objet tagé, cela lance une fonction
	Can.tag_bind("Tag_Reprendre", "<Button-1>", Reprendre)
	Can.tag_bind("Tag_Menu", "<Button-1>", Retour_MENU)

def Perdre():
	global Perso, pos_P, NumLevel
	
	PlaySound("Musiques\perso-meurt.wav",1)
	fen.unbind_all('<Key>')
	Can.delete(Perso)
	Perso = Can.create_image(pos_P[0], pos_P[1], image=F_Perdu, anchor=NW) #On change l'image du Perso pour une image où il meurt
	Can.create_text(pos_P[0]+200, 300, text="Perdu !", font="arial 32 bold", fill="blue")
	
	#On relance le niveau dans lequel on joue, il n'y a que deux niveaux en tout
	if NumLevel == 1: 
		fen.after(3000, Level1, "inutile")
	if NumLevel == 2:
		fen.after(3000, Level2, "inutile")

def Gagne():
	global pos_P, repeat_func
	
	"""Fonction qui fait revenir au menu apres avoir gagné le niveau"""
	
	PlaySound("Musiques\yipe.wav",1)
	repeat_func = False
	fen.unbind_all('<Key>')
	Can.create_text(pos_P[0]+200, 300, text="GAGNE !", font="arial 32 bold", fill="blue")
	fen.after(3000, Retour_MENU, "inutile")

def Quitter_Jeu(inutile):
	""" Fonction qui ferme le jeu"""
	fen.quit()
	
def Comment_Jouer(inutile):

	"""Fonction qui explique comment jouer, cliquez sur "comment jouer ?" dans le menu """

	Can.delete(ALL)
	Can.create_image(0, 0, image=F_MENU, anchor=NW)
	Can.create_text(200, 210, text="Deplacer vous avec ", font="arial 25 bold")
	Can.create_image(350, 105, image=F_Fleche, anchor=NW)
	Can.create_text(150, 310, text="Appuyer sur ", font="arial 25 bold")
	Can.create_image(255, 280, image=F_Fleche_Haut, anchor=NW)
	Can.create_text(550, 310, text="pour sauter sur les ennemis", font="arial 25 bold")
	Can.create_text(210, 410, text="Votre score s'affiche ", font="arial 25 bold")
	Can.create_image(410, 350, image=F_Level_Tuto, anchor=NW)
	
	T_Retour = Can.create_text(130, 30, text="<= Retour", font="arial 32 bold", activefill="red", tag="Tag_Menu")
	Can.tag_bind("Tag_Menu", "<Button-1>", MENU)
	
def MENU(inutile):
	global repeat_func, Allow_Musique, Etat_Musique, T_Etat_Musique, T_Musique

	"""Fonction qui montre le menu"""
	
	repeat_func = False
	fen.unbind_all('<Key>')
	
	Can.delete(ALL) #On enleve tous les objets du Canvas
	Can.create_image(0, 0, image=F_MENU, anchor=NW)
	Can.xview_moveto(0) #Remet le Canvas à la bonne place en abscisses
	Titre = Can.create_text(400, 50, text="Super PIG", font="arial 32 bold", fill="red")
	Choix_niveau = Can.create_text(400, 150, text="Choisir le niveau", tag="Choix_level", font="arial 25 bold", activefill="red", fill="white")
	T_Musique = Can.create_text(380, 250, text="Musique :", font="arial 25 bold", fill="white")
	T_Etat_Musique = Can.create_text(490, 250, text=Etat_Musique, font="arial 25 bold",activefill="red", tag="Tag_Musique", fill="white")
	T_Comment_Jouer = Can.create_text(400, 350, text="Comment jouer ?", tag="Tag_Comment_Jouer", font="arial 25 bold", activefill="red", fill="white")
	Quitter = Can.create_text(400, 450, text="Quitter", tag="Quit", font="arial 25 bold", activefill="red", fill="white")
	
	Can.tag_bind("Tag_Comment_Jouer", "<Button-1>", Comment_Jouer)
	Can.tag_bind("Tag_Musique", "<Button-1>", Interrupteur_Musique_MENU)
	Can.tag_bind("Choix_level", "<Button-1>", Choisir_niveau)
	Can.tag_bind("Quit", "<Button-1>", Quitter_Jeu)

def Choisir_niveau(inutile):
	
	""" Fonction qui montre la page où on choisi le niveau """
	Can.delete(ALL)
	Can.create_image(0, 0, image=F_MENU, anchor=NW)
	Can.create_text(400, 30, text="Choix du niveau", font="arial 32 bold", fill="red")
	Can.create_image(50, 200, image=F_Level_1, anchor=NW, activeimage=F_Level_1b, tag="Level1")
	Can.create_image(400, 200, image=F_Level_2, anchor=NW, activeimage=F_Level_2b, tag="Level2")
	T_Retour = Can.create_text(130, 30, text="<= Retour", font="arial 32 bold", activefill="red", tag="Tag_Menu")
	
	Can.tag_bind("Tag_Menu", "<Button-1>", MENU)
	Can.tag_bind("Level1", "<Button-1>", Level1)
	Can.tag_bind("Level2", "<Button-1>", Level2)
	
def Level2(inutile):
	global NumLevel, Allow_Musique
	
	"""Fonction qui lance le niveau 2"""
	
	Can.delete(ALL)
	Can.xview_moveto(0)
	NumLevel = 2
	
	Init_Var() #On reinitialise les variables
	Charge_Level() #On charge le niveau
	Affiche_Perso() #On affiche le Peros
	Mvt_Lateral()  #On lance la fonction du mouvement
	Deplacement_Goomba() #On lance le deplacement des annemis 
	verif()
	if Allow_Musique == True: #si la musique est activé, on lance le morceau
		PlaySound("Musiques\DesertEagle.wav",1)
	
	#On detecte les appuies de touches
	fen.bind("<KeyRelease>", Relache_Touche)
	fen.bind("<Key>", Appuie_Touche)
	
def Level1(inutile):
	global NumLevel, Allow_Musique
	
	"""Fonction qui lance le niveau 1"""
	
	Can.delete(ALL)
	Can.xview_moveto(0)
	NumLevel = 1
	
	Init_Var()
	Charge_Level()
	Affiche_Perso()
	Mvt_Lateral()
	Deplacement_Goomba()
	verif()
	if Allow_Musique == True:
		PlaySound("Musiques\DesertEagle.wav",1)
	
	fen.bind("<KeyRelease>", Relache_Touche)
	fen.bind("<Key>", Appuie_Touche)
	
def Init_Var():
	global F_PD0, F_PG0, F_PSG, F_PSD, \
	Photo_Perso, Goomba, DirG, IDGoomba, result2, fin_Saut, faire, Init_fini, \
	vitesse_P_init, orientation, orientation_vert, Saut, dep, repeat_func, Perdu, NumScore, \
	Active_Pause, Cactus, Bottes_Allow, Bottes, IDBottes
	
	""" On remet a zero toutes les variables qui change au cours du jeu """
	
	F_PD0 = PhotoImage(file="Images\PD0.png")
	F_PG0 = PhotoImage(file="Images\PG0.png")
	F_PSG = PhotoImage(file="Images\PSG.png")
	F_PSD = PhotoImage(file="Images\PSD.png")
	
	Active_Pause = False
	NumScore = 0
	Score.configure(text=NumScore)
	Perdu = False
	Photo_Perso = F_PD0
	Goomba = []
	Cactus = []
	Bottes = []
	IDBottes = []
	Bottes_Allow = False
	DirG = []
	IDGoomba = []
	result2 = "rien"
	fin_Saut = True
	faire = False
	Init_fini = False
	vitesse_P_init = [0, -20]
	orientation = "Droite"
	orientation_vert = "Aucune"
	Saut = False
	dep = "Stand"
	repeat_func = True
	
#Relache_Touche, Appuie_Touche les deux fonctions pour gerer les appuies de touches. Il y en a deux pour permettre l'appuie enfonce sur une touche sans décalage.
def Relache_Touche(event):
	global Touche_Relache, dep
	
	Touche_Relache = event.keycode #On associe a l'évènement un numero
	
	if Touche_Relache == 37:
		if dep == "Gauche":
			dep = "Stand"
	if Touche_Relache == 39:
		if dep == "Droite":
			dep = "Stand"
	
def Appuie_Touche(event):
	global dep, Saut, orientation, fin_Saut, coordH1, coordH2, Active_Pause, Appuie_Double_Saut, pos_P, Bottes_Allow

	code = event.keycode 
	
	if code == 27: #Echap
		if Active_Pause == False: #Empeche de mettre le jeu "plusieurs fois" en pause
			Pause()
	
	if code == 37: #Left
		dep = "Gauche"
		orientation = "Gauche"
	
	if code == 39: #Right
		dep = "Droite"
		orientation = "Droite"
	
	if code==38: #Up
		if Saut == False:
			if coordH1 == nulle and coordH2 == nulle:
				#fen.after(8, lance_Saut) #Pour ne pas que le saut s'effectue trop vite sinon il y a un bug
				lance_Saut()
		else:
			if Bottes_Allow == True:
				if Appuie_Double_Saut == False:
					if coordH1 == nulle and coordH2 == nulle:
						Appuie_Double_Saut = True
						Nuage = Can.create_image(pos_P[0], pos_P[1]+40, image=F_Nuage, anchor=NW)
						fen.after(300, Delete_Can, Nuage)
						lance_Saut()
				
def lance_Saut():
	global vitesse_P, fin_Saut, vitesse_P_init, Saut
	
	"""Fonction qui fait sauter le Perso"""
	
	Saut = True
	vitesse_P = vitesse_P_init
	fin_Saut = False
def lance_Saut2():
	global vitesse_P, fin_Saut, Saut
	
	"""Fonction qui fait rebondir le Perso apres avoir elimine un ennemi"""
	
	vitesse_P = [0, -12]
	fin_Saut = False
	Saut = True
	
#Fonction pour arrondir au multiple de 40 au dessus ou au dessous
def arrondir_sup40(nombre):
	reste = nombre%40
	if reste != 0:
		return nombre+(40-reste)
	else:
		return nombre
def arrondir_inf40(nombre):
	reste=nombre%40
	if reste != 0:
		return nombre-reste
	else:
		return nombre

def Delete_Can(objet):

	"""Fonction permettant de supprimer un objet du canvas"""
	
	Can.delete(objet)
		
def verif():
	global dep, pos_P, vitesse_P, nextpos_P, fin_Saut, Saut, nulle, orientation_vert, repeat_func, Perdu, Appuie_Double_Saut, \
	nextH1X, nextH1Y, nextH2X, nextH2Y, nextB1X, nextB1Y, nextB2X, nextB2Y, nextD1X, nextD1Y, nextD2X, nextD2Y, nextG1X, nextG1Y, nextG2X, nextG2Y, \
	nextHDX, nextHDY, nextBDX, nextBDY, nextHGX, nextHGY, nextBGX, nextBGY, nextB3X, nextB3Y, nextB4X, nextB4Y, \
	coordH1, coordH2, coordB1, coordB2, coordB3, coordB4, coordD1, coordD2, coordG1, coordG2, coordHD, coordHG, coordBD, coordBG, \
	Goomba, faire, NumScore, Cactus, Bottes, IDBottes
	
	
	#Les verifs de deplacement: si le déplacement est empêché alors on redéfinie nextpos_P 
	
	fin_Saut_verif = fin_Saut
	Saut_verif = Saut
	
	if Perdu == False:
		if nextpos_P[1] > 600: #Si on tombe en dehors du jeu
			repeat_func = False
			Perdu = True
		if nextpos_P[0] < 0:
			nextpos_P[0] = 0
		
	if Perdu == False:
		for a in range(len(Bottes)):
			try:
				posB = Can.coords(Bottes[a])
				if nextpos_P[0] >= posB[0]-40 and nextpos_P[0] <= posB[0]+40 and nextpos_P[1] >= posB[1]-40 and nextpos_P[1] <= posB[1]+40:
					Perso_Bottes()
					Can.delete(Bottes[a])
			except IndexError:
				break
		
	if Perdu == False:
		for a in range(len(Cactus)):
			posC = Can.coords(Cactus[a])
			if nextpos_P[0] > posC[0]-40 and nextpos_P[0] < posC[0]+40 and nextpos_P[1] > posC[1]-40 and nextpos_P[1] < posC[1]+40:
				print("fait")
				repeat_func = False
				Perdu = True
	
	if Perdu == False:
		if Saut == False:
			if coordD1 != nulle:
				if nextpos_P[0]+40 >= nextD1X:
					nextpos_P[0] = nextD1X-40
			if coordG1 != nulle:
				if nextpos_P[0] <= nextG1X+40:
					nextpos_P[0] = nextG1X+40
			if coordB1 == nulle and coordB2 == nulle:
				vitesse_P = [0, 1]
				fin_Saut_verif = False
				faire = True
	
	if Perdu == False:
		if Saut == True:
			if coordD1 != nulle or coordD2 != nulle:
				if nextpos_P[0]+40 >= nextD1X:
					nextpos_P[0] = nextD1X-40
			if coordG1 != nulle or coordG2 != nulle:
				if nextpos_P[0] <= nextG1X+40:
					nextpos_P[0] = nextG1X+40
			Do = True
			if coordH1 != nulle or coordH2 != nulle:
				for a in range(len(IDBottes)): #On verifie si l'objet detecte n'est pas un ennemi ou un item
					if coordH1 == IDBottes[a] or coordH2== IDBottes[a]:
						Do = False
				if Do == True:
					if nextpos_P[1] <= nextH1Y+40:
						vitesse_P = [0, 5]	
			Do = True
			Done = False #Variable nécessaire pour ne pas tomber "dans" une brique...
			if coordB1 != nulle or coordB2 != nulle:
				for a in range(len(IDGoomba)):
					if coordB1 == IDGoomba[a] or coordB2 == IDGoomba[a]: 
						Do = False
				for a in range(len(IDBottes)):
					if coordB1 == IDBottes[a] or coordB2 == IDBottes[a]:
						Do = False	
				if Do == True:
					if nextpos_P[1]+40 >= nextB1Y:
						nextpos_P[1] = nextB1Y-40
						fin_Saut_verif = True
						Saut_verif = False
						Done = True
			Do = True
			if Done == False: #evite de faire 2 verif
				if coordB3 != nulle or coordB4 != nulle:
					for a in range(len(IDGoomba)):
						if coordB3 == IDGoomba[a] or coordB4 == IDGoomba[a]: 
							Do = False
					for a in range(len(IDBottes)):
						if coordB3 == IDBottes[a] or coordB4 == IDBottes[a]:
							Do = False	
					if Do == True:
						if nextpos_P[1]+80 >= nextB3Y:
							nextpos_P[1] = nextB3Y-40
							fin_Saut_verif = True
							Saut_verif = False
			if coordHD != nulle:
				if nextpos_P[0]+40 >= nextHDX and nextpos_P[1] <= nextHDY+40:
					nextpos_P[0] = nextHDX-40
			if coordBD != nulle:
				if nextpos_P[0]+40 >= nextBDX and nextpos_P[1]+40 >= nextBDY:
					nextpos_P[0] = nextBDX-40
			if coordHG != nulle:
				if nextpos_P[0] <= nextHGX+40 and nextpos_P[1] <= nextHGY+40:
					nextpos_P[0] = nextHGX+40
			if coordBG != nulle:
				if nextpos_P[0] <= nextBGX+40 and nextpos_P[1]+40 >= nextBGY:
					nextpos_P[0] = nextBGX+40
	
	
	if Perdu == False:
		for a in range(len(Goomba)): #On verifie si on touche un goomba
			try:
				posG = Can.coords(Goomba[a])
				if posG[0] > pos_P[0]: #Si le goomba est a droite du perso
					if nextpos_P[0]+40 >= posG[0] and nextpos_P[0]+40 <= posG[0]+40 and pos_P[0] < posG[0]: #Verification pour les abscisses
						if nextpos_P[1] != posG[1]-40:
							if nextpos_P[1] >= posG[1]-40 and nextpos_P[1] <= posG[1]+40: #Verification pour les ordonnées
								repeat_func = False
								Perdu = True			
				
				else: #si le goomba est a gauche du perso
					if nextpos_P[0] <= posG[0]+40 and nextpos_P[0] >= posG[0] and pos_P[0] > posG[0]: #Verification pour les abscisses
						if nextpos_P[1] != posG[1]-40:
							if nextpos_P[1] >= posG[1]-40 and nextpos_P[1] <= posG[1]+40: #Verification pour les ordonnées
								repeat_func = False
								Perdu = True
			
				#Derniere verif pour les goomba car on supprime un indice de la liste donc pour ne pas avoir l'erreur "index out of range"
				if Saut == True: #Si on elimine l'ennemi
					if nextpos_P[0] >= posG[0]-40 and nextpos_P[0] <= posG[0]+40: #si on est sur le goomba (abscisses)
						if orientation_vert == "Bas":
							if pos_P[1]+40 < posG[1]: #Si on est pas encore sur le goomba
								if nextpos_P[1]+40 >= posG[1]-30 and nextpos_P[1]+40 <= posG[1]+40: # and nextpos_P[1]+40 <= posG[1]+40: #Si on est au dessus du goomba (ordonnées) (marge de ~=20)
									vitesse_P = [0, -15] #On lance le rebond
									nextpos_P[1] = posG[1]-40
									Can.delete(Goomba[a]) #On supprime le goomba
									Goomba.remove(Goomba[a])
									IDGoomba.remove(IDGoomba[a])
									Ajout = Can.create_text(posG[0]+40, posG[1]-20, text="+ 10", font="times 15", fill="yellow") #On ajoute le score (affiche un +10 et actualise le score du bas)
									fen.after(400, Delete_Can, Ajout)
									NumScore += 10
									Score.configure(text=NumScore)
									if fin_Saut_verif == True:
										fin_Saut_verif = False
										Saut_verif = True
									PlaySound("Musiques\Chaton.wav",1)
			except IndexError: #Pour permettre la suppression du goomba
				break
			
	
	#Deplacement de la caméra
	
	if pos_P[0] != nextpos_P[0]:
		if dep == "Droite":
			Can.xview_scroll(1, UNITS)
		if dep == "Gauche":
			Can.xview_scroll(-1, UNITS)
	
	a = nextpos_P[0]
	b = nextpos_P[1]
	pos_P = [a, b]
	fin_Saut = fin_Saut_verif #puisque Saut est en global on le change qu'a la fin
	Saut = Saut_verif
	
	if Saut == False:
		Appuie_Double_Saut = False
	
	if pos_P[0] > finX:
		Gagne()
	
	
	#Reperage des cases a proximité
	#Case H1: au dessus a gauche, H2:au dessus a droite
	nextH1X = arrondir_inf40(pos_P[0])   
	nextH1Y = arrondir_inf40(pos_P[1]-40)
	nextH2X = arrondir_sup40(pos_P[0])
	nextH2Y = arrondir_inf40(pos_P[1]-40)
	
	nextB1X = arrondir_inf40(pos_P[0])
	nextB1Y = arrondir_sup40(pos_P[1]+40)
	nextB2X = arrondir_sup40(pos_P[0])
	nextB2Y = arrondir_sup40(pos_P[1]+40)
	nextB3X = arrondir_inf40(pos_P[0])
	nextB3Y = arrondir_sup40(pos_P[1]+80)
	nextB4X = arrondir_sup40(pos_P[0])
	nextB4Y = arrondir_sup40(pos_P[1]+80)
	
	nextD1X = arrondir_sup40(pos_P[0]+40)
	nextD1Y = arrondir_inf40(pos_P[1])
	nextD2X = arrondir_sup40(pos_P[0]+40)
	nextD2Y = arrondir_sup40(pos_P[1])
	
	nextG1X = arrondir_inf40(pos_P[0]-40)
	nextG1Y = arrondir_inf40(pos_P[1])
	nextG2X = arrondir_inf40(pos_P[0]-40)
	nextG2Y = arrondir_sup40(pos_P[1])
	
	nextHDX = arrondir_sup40(pos_P[0]+40)
	nextHDY = arrondir_inf40(pos_P[1]-40)
	
	nextBDX = arrondir_sup40(pos_P[0]+40)
	nextBDY = arrondir_sup40(pos_P[1]+40)
	
	nextHGX = arrondir_inf40(pos_P[0]-40)
	nextHGY = arrondir_inf40(pos_P[1]-40)
	
	nextBGX = arrondir_inf40(pos_P[0]-40)
	nextBGY = arrondir_sup40(pos_P[1]+40)
	
	coordH1 = Can.find_enclosed(nextH1X, nextH1Y, nextH1X+40, nextH1Y+40) #On verifie ce qu'il y a dans le carré de 40x40 observé
	coordH2 = Can.find_enclosed(nextH2X, nextH2Y, nextH2X+40, nextH2Y+40)
	coordB1 = Can.find_enclosed(nextB1X, nextB1Y, nextB1X+40, nextB1Y+40)
	coordB2 = Can.find_enclosed(nextB2X, nextB2Y, nextB2X+40, nextB2Y+40)
	coordB3 = Can.find_enclosed(nextB3X, nextB3Y, nextB3X+40, nextB3Y+40)
	coordB4 = Can.find_enclosed(nextB4X, nextB4Y, nextB4X+40, nextB4Y+40)
	coordG1 = Can.find_enclosed(nextG1X, nextG1Y, nextG1X+40, nextG1Y+40)
	coordG2 = Can.find_enclosed(nextG2X, nextG2Y, nextG2X+40, nextG2Y+40)	
	coordD1 = Can.find_enclosed(nextD1X, nextD1Y, nextD1X+40, nextD1Y+40)
	coordD2 = Can.find_enclosed(nextD2X, nextD2Y, nextD2X+40, nextD2Y+40)
	coordHD = Can.find_enclosed(nextHDX, nextHDY, nextHDX+40, nextHDY+40)
	coordBD = Can.find_enclosed(nextBDX, nextBDY, nextBDX+40, nextBDY+40)
	coordHG = Can.find_enclosed(nextHGX, nextHGY, nextHGX+40, nextHGY+40)
	coordBG = Can.find_enclosed(nextBGX, nextBGY, nextBGX+40, nextBGY+40)
		
	
	
#Fonction qui effectue les mouvements latéraux et vérifie si le déplacement est possible
def Mvt_Lateral():
	global dep, pos_P, vPx, Photo_Perso, vitesse_P, deplacement_lateral, nextpos_P, fin_Saut, Saut, vdep, orientation_vert, Perdu, \
	nextH1X, nextH1Y, nextH2X, nextH2Y, nextB1X, nextB1Y, nextB2X, nextB2Y, nextD1X, nextD1Y, nextD2X, nextD2Y, nextG1X, nextG1Y, nextG2X, nextG2Y, \
	nextHDX, nextHDY, nextBDX, nextBDY, nextHGX, nextHGY, nextBGX, nextBGY, nextB3X, nextB3Y, nextB4X, nextB4Y, \
	coordH1, coordH2, coordB1, coordB2, coordB3, coordB4, coordD1, coordD2, coordG1, coordG2, coordHD, coordHG, coordBD, coordBG, \
	Goomba, faire, result2, repeat_func
	
	"""Fonction qui permet le déplacement du Perso"""
	
	#On définie quelle est la prochaine position du Perso
	deplacement_lateral = "off"
	if dep == "Gauche":
		nextpos_P[0] = pos_P[0]-vPx
		deplacement_lateral = "on"
	elif dep == "Droite":
		nextpos_P[0] = pos_P[0]+vPx
		deplacement_lateral = "on"
	
		
	if Saut == True:
		nextvitesse_P = vectorAdd(vitesse_P, gravite_P)
		result = vectorAdd(pos_P, vitesse_P)
		nextpos_P[1] = result[1]
		if nextvitesse_P[1] > 20: #On met une borne a la vitesse
			nextvitesse_P[1] = 20
	
		if nextpos_P[1] < pos_P[1]:
			orientation_vert = "Haut"
		if nextpos_P[1] >= pos_P[1]:
			orientation_vert = "Bas"
		
		result = vitesse_P #Variable pour garder la valeur de vitesse_P
		result2 = fin_Saut
		
		
	if deplacement_lateral == "on" or Saut == True: #On verifie le deplacement
		verif()
		
	if Saut == True:
		if result == vitesse_P: #si vitesse_P n'a pas ete changé par verif()
			vitesse_P = nextvitesse_P
		
		
	
	#On modifie l'image du perso en fonction de son déplacement
	if deplacement_lateral == "on":
		if Saut == False:
			if dep == "Gauche":
				Photo_Perso = F_PG0
			else:
				Photo_Perso = F_PD0
	#Orientation : si on monte ou descend
	if fin_Saut == False:
		if orientation == "Gauche":
			if Photo_Perso != F_PSG:
				Photo_Perso = F_PSG
		if orientation == "Droite":
			if Photo_Perso != F_PSD:
				Photo_Perso = F_PSD
	else:
		if orientation == "Gauche":
			Photo_Perso = F_PG0
		if orientation == "Droite":
			Photo_Perso = F_PD0
		
	if deplacement_lateral == "on" or Saut == True or result2 != fin_Saut:
		Affiche_Perso()
	
	if faire == True:
		Saut = True
		faire = False
		
	if Perdu == True:
		Perdre()
		
	if repeat_func == True:
		fen.after(vdep, Mvt_Lateral)
	
def Affiche_Perso():
	global Perso, pos_P, Photo_Perso
	
	"""Fonction qui affiche le Perso"""
	
	Can.delete(Perso)
	Perso = Can.create_image(pos_P[0], pos_P[1], image=Photo_Perso, anchor=NW)

#Fonction qui additionne des vecteurs
def vectorAdd(a,b):
	return [a[0]+b[0],a[1]+b[1]]
	
def Deplacement_Goomba():
	global Goomba, nulle, vPx, DirG, vdep, pos_P, fin_Saut, Saut, vitesse_P, repeat_func, NumScore
	
	"""fonction qui permet le déplacement des ennemis"""
	
	for a in range(len(Goomba)): #Pour chaque ennemi:
		try:
			pos = Can.coords(Goomba[a]) #On regarde quelles sont les coordonnées de l'ennemi
			continuer = True
		
			#Verif case a gauche du goomba
			GX = arrondir_inf40(pos[0]-40)	
			GY = pos[1]
			caseG = Can.find_enclosed(GX, GY, GX+40, GY+40)
			if caseG != nulle: #Ici comme en dessous c'est pour savoir si on rencontre un autre goomba, si c'est le cas, les goombas se passent au travers
				for b in range(len(IDGoomba)):
					if caseG == IDGoomba[b]:
						continuer = False
				if continuer == True:
					if pos[0] <= GX+40:
						DirG[a] = "Droite"	
					
			#Verif case a droite du goomba
			DX =  arrondir_sup40(pos[0]+40)
			DY = pos[1]
			caseD = Can.find_enclosed(DX, DY, DX+40, DY+40)
			if caseD != nulle:
				for b in range(len(IDGoomba)):
					if caseD == IDGoomba[b]:
						continuer = False
				if continuer == True:
					if pos[0]+40 >= DX:
						DirG[a] = "Gauche"
			
			#Verif case en bas à droite du goomba
			BDX = arrondir_sup40(pos[0]+40)
			BDY = pos[1]+40
			caseBD = Can.find_enclosed(BDX, BDY, BDX+40, BDY+40)
			if caseBD == nulle:
				if pos[0]+40 >= BDX:
					DirG[a] = "Gauche"
		
			#Verif case en bas à gauche du goomba
			BGX = arrondir_inf40(pos[0]-40)
			BGY = pos[1]+40
			caseBG = Can.find_enclosed(BGX, BGY, BGX+40, BGY+40)
			if caseBG == nulle:
				if pos[0] <= BGX+40:
					DirG[a] = "Droite"
		
			#Verif si il ne touche pas le perso pour empecher le bug où le perso reste sur le goomba
			if pos_P[0]+40 >= pos[0] and pos_P[0] <= pos[0]+40:###
				if pos_P[1]+40 == pos[1]:
					Can.delete(Goomba[a]) #On supprime le goomba
					Goomba.remove(Goomba[a])
					IDGoomba.remove(IDGoomba[a])
					vitesse_P = [0, -15]
					fin_Saut = False
					Saut = True
					Ajout = Can.create_text(pos[0]+40, pos[1]-20, text="+ 10", font="times 15", fill="yellow") #On ajoute le score (affiche un +10 et actualise le score du bas)
					fen.after(400, Delete_Can, Ajout)
					NumScore += 10
					Score.configure(text=NumScore)
						
			#On deplace le goomba
			if DirG[a] == "Gauche":
				Can.move(Goomba[a], -vPx, 0)
			else:
				Can.move(Goomba[a], vPx, 0)
				
		except IndexError:  #Pour permettre la suppression du goomba
			break
	
	#Quand le perso ne se deplace pas on verifie si il n'est pas touché par un goomba
	if deplacement_lateral == "off" and Saut == False:
		verif()
	
	
	if repeat_func == True:
		fen.after(6*vdep, Deplacement_Goomba) #6*vdep = 6 fois plus lent que la vitesse du Perso
	
#Fonction qui affiche le niveau
def Charge_Level():
	global Goomba, DirG, IDGoomba, Fond, pos_P, nextpos_P, NumLevel, Perso, finX, Cactus, Bottes, IDBottes, \
	nextH1X, nextH1Y, nextH2X, nextH2Y, nextB1X, nextB1Y, nextB2X, nextB2Y, nextD1X, nextD1Y, nextD2X, nextD2Y, nextG1X, nextG1Y, nextG2X, nextG2Y, \
	nextHDX, nextHDY, nextBDX, nextBDY, nextHGX, nextHGY, nextBGX, nextBGY, nextB3X, nextB3Y, nextB4X, nextB4Y, \
	coordH1, coordH2, coordB1, coordB2, coordB3, coordB4, coordD1, coordD2, coordG1, coordG2, coordHD, coordHG, coordBD, coordBG
	
	"""Fonction qui ouvre un fichier texte, et associe a chaque caractere une image"""
	
	#On crée une image de fond
	Fond = Can.create_image(0, 0, image=F_Fond_Bleu, anchor=NW)
	
	x, y = 0, 0
	niveau = open("Niveaux\Level_"+str(NumLevel)+".txt") #On ouvre le fichier texte
	
	for ligne in niveau:
		for i in range(225):
			case = ligne[i]
			if case == "f":
				Can.create_image(x, y, image=F_Drapeau, anchor=NW)
				finX = x
			if case == "x":
				pos_P = [x, y]
				nextpos_P = [x, y] #ne pas mettre pos_P = nextpos_P sinon pos_P change tout seul
			if case == "|": #un mur
				Can.create_image(x, y, image=F_Stone2, anchor=NW)
			if case == "B": #un mur
				Can.create_image(x, y, image=F_Stone, anchor=NW)
			if case == "-": #un mur
				Can.create_image(x, y, image=F_Brique, anchor=NW)
			if case == "O":
				Bottes.append(Can.create_image(x, y, image=F_Item_Bottes, anchor=NW))
				a = Can.find_enclosed(x, y, x+40, y+40)
				IDBottes.append(a)
			if case == "K": #un cactus
				Cactus.append(Can.create_image(x, y, image=F_Cactus, anchor=NW))
			if case == "g": #Goomba, un ennemi
				Goomba.append(Can.create_image(x, y, image=F_Goomba, anchor=NW))
				a = Can.find_enclosed(x, y, x+40, y+40)
				IDGoomba.append(a)
				DirG.append("Gauche")
			x += 40
		x = 0
		y += 40
	niveau.close()

	
	Perso = Can.create_image(pos_P[0], pos_P[1], image=Photo_Perso, anchor=NW)
	
	nextH1X = arrondir_inf40(pos_P[0])   
	nextH1Y = arrondir_inf40(pos_P[1]-40)
	nextH2X = arrondir_sup40(pos_P[0])
	nextH2Y = arrondir_inf40(pos_P[1]-40)
	
	nextB1X = arrondir_inf40(pos_P[0])
	nextB1Y = arrondir_sup40(pos_P[1]+40)
	nextB2X = arrondir_sup40(pos_P[0])
	nextB2Y = arrondir_sup40(pos_P[1]+40)
	nextB3X = arrondir_inf40(pos_P[0])
	nextB3Y = arrondir_sup40(pos_P[1]+80)
	nextB4X = arrondir_sup40(pos_P[0])
	nextB4Y = arrondir_sup40(pos_P[1]+80)
		
	nextD1X = arrondir_sup40(pos_P[0]+40)
	nextD1Y = arrondir_inf40(pos_P[1])
	nextD2X = arrondir_sup40(pos_P[0]+40)
	nextD2Y = arrondir_sup40(pos_P[1])

	nextG1X = arrondir_inf40(pos_P[0]-40)
	nextG1Y = arrondir_inf40(pos_P[1])
	nextG2X = arrondir_inf40(pos_P[0]-40)
	nextG2Y = arrondir_sup40(pos_P[1])

	nextHDX = arrondir_sup40(pos_P[0]+40)
	nextHDY = arrondir_inf40(pos_P[1]-40)

	nextBDX = arrondir_sup40(pos_P[0]+40)
	nextBDY = arrondir_sup40(pos_P[1]+40)

	nextHGX = arrondir_inf40(pos_P[0]-40)
	nextHGY = arrondir_inf40(pos_P[1]-40)

	nextBGX = arrondir_inf40(pos_P[0]-40)
	nextBGY = arrondir_sup40(pos_P[1]+40)

	coordH1 = Can.find_enclosed(nextH1X, nextH1Y, nextH1X+40, nextH1Y+40)
	coordH2 = Can.find_enclosed(nextH2X, nextH2Y, nextH2X+40, nextH2Y+40)
	coordB1 = Can.find_enclosed(nextB1X, nextB1Y, nextB1X+40, nextB1Y+40)
	coordB2 = Can.find_enclosed(nextB2X, nextB2Y, nextB2X+40, nextB2Y+40)
	coordB3 = Can.find_enclosed(nextB3X, nextB3Y, nextB3X+40, nextB3Y+40)
	coordB4 = Can.find_enclosed(nextB4X, nextB4Y, nextB4X+40, nextB4Y+40)
	coordG1 = Can.find_enclosed(nextG1X, nextG1Y, nextG1X+40, nextG1Y+40)
	coordG2 = Can.find_enclosed(nextG2X, nextG2Y, nextG2X+40, nextG2Y+40)	
	coordD1 = Can.find_enclosed(nextD1X, nextD1Y, nextD1X+40, nextD1Y+40)
	coordD2 = Can.find_enclosed(nextD2X, nextD2Y, nextD2X+40, nextD2Y+40)
	coordHD = Can.find_enclosed(nextHDX, nextHDY, nextHDX+40, nextHDY+40)
	coordBD = Can.find_enclosed(nextBDX, nextBDY, nextBDX+40, nextBDY+40)
	coordHG = Can.find_enclosed(nextHGX, nextHGY, nextHGX+40, nextHGY+40)
	coordBG = Can.find_enclosed(nextBGX, nextBGY, nextBGX+40, nextBGY+40)
	
	
PlaySound("Musiques\CreamOnChrome.wav",1)
MENU("inutile")
fen.mainloop()








