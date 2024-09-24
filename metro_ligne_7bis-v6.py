# coding: utf-8
"""
Chapitre: NSIT_03_POO
Activité: rames de métro ligne 7 avec interface graphique tkinter

Créé le 24/09/2020 à 10:00

@author: eric.buonocore
"""
from tkinter import *


def manege():
    """ Fait avancer toutes les rames (si elles le peuvent).
        Déplace les cercles sur le canevas
        Se relance automatiquement dans 1000ms
    """
    for rame in rames: # On tente de faire avancer chaque rame.
        rame.avance(rames)
    j = 0
    for rame in rames: # On affiche la station de chaque rame sur une ligne
        x = rame.stations[rame.get_station()]['x']
        y = rame.stations[rame.get_station()]['y']
        canvas.coords(cercles[j], x, y, x+15, y+15)
        j += 1
    fenetre.after(400,manege)
    

class Rame_ligne_7bis:
    stations = [{'nom':'Louis Blanc_1', 'x':100,'y':84}, {'nom':'Jaurès_1', 'x':197,'y':55},
                {'nom':'Bolivar_1', 'x':252,'y':87}, {'nom':'Buttes Chaumont_1', 'x':375,'y':165},
                {'nom':'Botzaris_1', 'x':475,'y':120}, {'nom':'Place des fêtes', 'x':558,'y':184},
                {'nom':'Pré Saint-Gervais', 'x':643,'y':114}, {'nom':'Danube', 'x':548,'y':27},
                {'nom':'Botzaris_2', 'x':478,'y':74}, {'nom':'Buttes Chaumont_2', 'x':370,'y':117},
                {'nom':'Bolivar_2', 'x':258,'y':50}, {'nom':'Jaurès_2', 'x':196,'y':12},
                {'nom':'Louis Blanc_2', 'x':97,'y':40}]
    def __init__(self, reference_rame, station = 0):
        """ reference_rame: Nom ou référence de la rame de métro
            station: Indice de la sation dans la liste 'stations'
        """
        self.reference_rame = reference_rame
        self.__station = station
        
    def station_suivante(self, indice_station:int)->int:
        """ Renvoie l'indice de la prochaine station.
            Retourne à l'indice 0 si on arrive en fin de liste pour éviter un débordement.
        """
        if indice_station  < len(self.stations)-1:
            return indice_station + 1
        else:
            return 0
        
    def avance(self,liste_rames:list)->bool:
        """ Si l'une des autres rame se trouve sur la prochaine station, notre rame ne peut pas partir.
            La sation ne change pas et la fonction renvoie False.
            Sinon, la station passe à l'indice suivante et la fonction renvoie True
        """
        # Examen de toutes les rames pour savoir s'il y en a une juste devant
        for autre_rame in liste_rames: 
            if autre_rame.get_station() == self.station_suivante(self.__station):
                print("Ca coince.")
                return False
        # Examen de toutes les rames pour savoir s'il y en a une deux sations plus loin
        for autre_rame in liste_rames:
            if autre_rame.get_station() == self.station_suivante(self.station_suivante(self.__station)):
                print("Ca coince plus loin.")
                return False
        # Si tout est libre, on passe à la station suivante
        self.__station = self.station_suivante(self.__station)
        return True
    
    def get_station(self)->int:
        """ Accesseur de l'attribut privé '__station'.
        """
        return self.__station
    
def cherche_place_libre():
    """ Cherche parmi les rames la première de la liste a être libre de métro.
        Renvoie l'indice de la station ,sinon renvoie None
    """
    libres = []
    if len(rames) > 0: # Si le nombre de rames n'est pas nul
        libres = [i for i in range(len(rames[0].stations))] # Construit la liste des entiers correspondant au nombre de stations
        for i in range(len(rames)): # Pour chaque rame
            #print(libres, rames[i].get_station())
            libres.remove(rames[i].get_station()) # J'enlève de la liste le numéro de la station occupé par cette rame
        if len(libres) > 0:
            return libres[0] # Renvoie l'indice de la première statio libre
        else:
            print("Plus de place")
            return None
    return 0 # Sinon, si la liste des stations libre est vide, renvoie None
    
def plus():
    """ Si une station est libre, instancie le nouvel objet 'rame' à cet endroit.
        Crée le cercle correspondant avec la couleur correspondante à l'indice de la station libre
    """
    station_libre = cherche_place_libre()
    if station_libre != None:
        #print("Première station libre en", station_libre,":",rames[0].stations[station_libre]['nom'])
        nouvelle_rame = Rame_ligne_7bis("MF88_"+str(len(rames)),station_libre)
        rames.append(nouvelle_rame)
        n_x = nouvelle_rame.stations[nouvelle_rame.get_station()]['x'] # Récupération des coordonnées de la station
        n_y = nouvelle_rame.stations[nouvelle_rame.get_station()]['y']
        n_couleur = '#4' + str(hex(15-station_libre))[2] + str(hex(station_libre))[2] # Création du code hexadécimal de la couleur de la rame
        cercles.append(canvas.create_oval(n_x,n_y,n_x+15,n_y+15, fill=n_couleur, outline='black')) # Création du cercle et ajout dans l'agrégateur 'cercles'

def moins():
    """ Si il existe au moins une rame, il détruit la dernière de la liste 'rames' et son cercle associé.
    """
    if len(rames) > 0: # Si le nombre de rames n'est pas nul
        rames.pop()
        dernier_cercle = cercles.pop()
        canvas.delete(dernier_cercle)
    
fenetre = Tk() # Instanciation de la fenêtre
# Instanciation des objets boutons
bouton_fin = Button(fenetre, text = "Fin", width = 6, command = fenetre.destroy)
bouton_plus = Button(fenetre, text = "Plus", width = 6, command = plus)
bouton_moins = Button(fenetre, text = "Moins", width = 6, command = moins)

# Paramétrage géométrique des boutons (pack)
bouton_fin.pack(pady=10)
bouton_plus.pack(pady=10)
bouton_moins.pack(pady=10)

photo = PhotoImage(file="plan_metro.png") # Chargement de la photo (plan de la ligne 7bis)
canvas = Canvas(fenetre,width=800, height=210) # Création du canevas dans la fenêtre (zone de dessin)
canvas.create_image(0, 0, anchor=NW, image=photo) # Insertion de la photo dans le canevas

# Instanciation des rames
MF88_1 = Rame_ligne_7bis("MF88_1")
MF88_2 = Rame_ligne_7bis("MF88_2",1)
MF88_3 = Rame_ligne_7bis("MF88_3",2)
MF88_4 = Rame_ligne_7bis("MF88_4",3)
MF88_5 = Rame_ligne_7bis("MF88_5",4)
MF88_6 = Rame_ligne_7bis("MF88_6",5)
MF88_7 = Rame_ligne_7bis("MF88_7",6)

# rames: Agrégateur de rames
rames = [ MF88_1, MF88_2, MF88_3, MF88_4 , MF88_5, MF88_6]

cercles = [] # Agrégateurs des cercles associés aux rames
i=0
for rame in rames:
    x = rame.stations[rame.get_station()]['x'] # Récupération des coordonnées de chaque station
    y = rame.stations[rame.get_station()]['y']
    couleur = '#4' + str(hex(15-i))[2] + str(hex(i))[2] # Création du code hexadécimal de la couleur de la rame
    cercles.append(canvas.create_oval(x,y,x+15,y+15, fill=couleur, outline='black')) # Création du cercle et ajout dans l'agrégateur 'cercles'
    i += 1
    
canvas.pack() # Paramétrage géométrique du canevas. Ici, aucun paramètre spécifié.
fenetre.after(2000,manege) # Premier lancement de la procédure 'manege' dans 1000ms
fenetre.mainloop() # Fenêtre principale tkinter