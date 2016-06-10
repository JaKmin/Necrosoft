import tkinter as tk
from tkinter import ttk as ttk
from tkinter import messagebox
import donnees
import texts
from random import randrange, choice
import json
import time
from operator import attrgetter

__author__ = 'Jamin'
# -*-coding:utf-8 -*

dark_grey = '#545454'
darker_grey = '#424242'
light_grey = '#BFC0C0'
lighter_grey = '#D7D8D8'
MENU_FONT = ("Helvetica", 30, "bold")
TITLE_FONT = ("Helvetica", 16, "bold")
FONT = ("Helvetica", 16)

largeur = 1280
hauteur = 720

# ----FONCTIONS-GENERALES------------------------------------------------------------------------------------------------


def D6(x=1):
    de = 0
    i = 0
    while i!=x:
        de += randrange(1,7)
        i+=1
    return de

# ----CLASSES-D'OBJETS---------------------------------------------------------------------------------------------------


class Gang:
    _id = 0

    def __init__(self, nom, joueur, maison, magot=1000):
        Gang._id += 1
        if debug:
            print("Creation d'un gang (id : {})".format(Gang._id))
        self.nom = nom

        self.joueur = joueur

        self.maison = maison

        self.magot = magot

        self.arsenal = []

        self.territoires = []

        self._id=Gang._id

        self.fichier = self.setNomFichier()

        self.date_creation = self.initDateCreation()

        self.nb_vict=[0,0]

    # ---FONCTIONS D'AFFICHAGE

    def affNom(self):
        n_nom = tk.StringVar()
        n_nom.set(self.nom)
        return n_nom

    def affJoueur(self):
        n_joueur = tk.StringVar()
        n_joueur.set(self.joueur)
        return n_joueur

    def affMaison(self):
        n_maison = tk.StringVar()
        n_maison.set(self.maison)
        return n_maison

    def affMagot(self):
        n_magot = tk.IntVar()
        n_magot.set(self.magot)
        return n_magot

    def affVict(self):
        vict = tk.IntVar()
        vict.set(self.nb_vict[0])
        tot = tk.IntVar()
        tot.set(self.nb_vict[1])
        return [vict, tot]

    def affDateCreation(self):
        date = tk.StringVar()
        date.set(self.date_creation)
        return date

    # ---CREATION AUTO DES DONNEES

    def setNomFichier(self):
        nom_fichier = ''
        for l in self.nom.lower():
            if l == ' ':
                nom_fichier += '_'
            elif l not in ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r',
                           's', 't', 'u', 'v', 'w', 'x', 'y', 'z']:
                pass
            else:
                nom_fichier += l
        nom_fichier += '.gg'
        return nom_fichier

    def initDateCreation(self):
        date = time.localtime()
        date_creation = "{}/{}/{}".format(date.tm_mday, date.tm_mon, date.tm_year)
        return date_creation

    def valeurGang(self, gangers):
        valeur = 0
        for gun in self.arsenal:
            valeur += donnees.arsenal[gun][0]
        for gg in gangers:
            if gg.gang == self.nom:
                valeur += gg.cout
                valeur += gg.exp
                for equip in gg.equip:
                    cout = donnees.arsenal[equip][0]
                    valeur += cout
            else:
                pass
        return valeur

    # ---GESTION DES GANGERS

    def addGanger(self, ganger):
        self.l_gangers.append(ganger)
        ganger.gang = self

    def listeGangers(self, list):
        self.l_gangers = []
        for gr in list:
            if self.nom == gr.gang:
                self.l_gangers.append(gr.nom)

    # ---FONCTIONS DE MODIFICATION

    def depenser(self, nb):
        if (self.magot-nb) < 0:
            tk.messagebox.showwarning("Greed is good, but ...", "Vous ne pouvez pas vous permettre cette dépense.")
            return False
        else:
            self.magot-=nb
            return True

    def bataille(self, victoire):
        self.nb_vict[1] += 1
        if victoire:
            self.nb_vict += 1

    def setNom(self, nom):
        self.nom = nom

    def setMagot(self, magot):
        self.magot = magot

    def setJoueur(self, joueur):
        self.joueur = joueur

    def setNbVict(self, nb_vict):
        self.nb_vict = nb_vict

    def setDateCreation(self, date_creation):
        self.date_creation = date_creation


class Ganger:
    def __init__(self, nom, gang, grade):
        self.nom = nom

        self.gang = gang

        self.grade=grade

        self.carac = donnees.stats_type[self.grade]

        self.level_up = 0

        self.comp = []
        self.equip = []
        self.bless = []

        self.cout = donnees.cout_recrut[self.grade]

        l_xp = donnees.exp_recrut[self.grade]

        self.exp = D6(l_xp[0])+l_xp[1]
        self.rang = self.indiquerRang()
        self.etat = 'Indemne'

        self.blessure = False

    # ---FONCTION D'AFFICHAGE

    def affNom(self):
        n_nom = tk.StringVar()
        n_nom.set(self.nom)
        return n_nom

    def affGrade(self):
        n_gd = tk.StringVar()
        n_gd.set(donnees.nom_grades[self.grade])
        return n_gd

    def getCarac(self):
        carac = []
        i = 0
        for cc in self.carac:
            carac.append([donnees.noms_stats[i],cc])
            i+=1
        return carac

    def getEtat(self):
        n_etat = tk.StringVar()
        n_etat.set(self.etat)
        return n_etat

    # ---FONCTION DE MODIFICATION

    def modCarac(self, carac, modif):
        self.carac[carac] += modif
        self.level_up += 1

    def setNom(self, nom):
        self.nom = nom

    def setEtat(self, etat):
        self.etat = etat

    def setGang(self, gang):
        self.gang = gang

    # ---CREATION AUTO DES DONNEES

    def indiquerRang(self):
        i = -1
        for rang in donnees.rangs:
            i += 1
            if self.exp <= rang[0]:
                return [i, donnees.rangs[i][1]]

    def rangSuivant(self):
        i = -1
        for rang in donnees.rangs:
            i += 1
            if self.exp <= rang[0]:
                return [donnees.rangs[i-1][0],donnees.rangs[i][0]]

    def getMaison(self):
        gang = self.gang
        for g in self.gangs:
            if gang == g.nom:
                return g.maison

    def getID(self, gangs):
        for g in gangs:
            if g.nom == self.gang:
                return g._id

    def expPlus(self, xp):
        self.exp += xp
        if self.grade == 0 and self.exp > 20:
            self.grade = 1
        else:
            pass

    def ajouterComp(self, comp):
        erreur = False
        for com in self.comp:
            if comp == com:
                tk.messagebox.showerror('Compétence déjà acquise','Vous ne pouvez pas avoir 2 fois la même compétence !')
                erreur = True
            else:
                pass
        if erreur == False:
            self.comp.append(comp)

    def retirerComp(self, comp):
        if comp in self.comp:
            self.comp.remove(comp)
        else:
            tk.messagebox.showerror('Erreur !', "Vous essayez de retirer une compétence que le ganger n'a pas !")

    def ajouterEquip(self, equip):
        self.equip.append(equip)

    def retirerEquip(self, equip):
        if equip in self.equip:
            self.equip.remove(equip)
        else:
            tk.messagebox.showerror('Erreur !', "Vous essayez de retirer un équipement que le ganger n'a pas !")

# ----CLASSE-PRINCIPALE--------------------------------------------------------------------------------------------------


class App(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)

        # --METHODE DE CREATION
        if fichier_svg:
            try:
                save = self.chargerSave()
                self.gangs = save[0]
                self.gangers = save[1]
            except:
                print("Erreur pendant la création des variables")

        if creation:
            self.gangs = [Gang("Rico and the Flying Ducks", "Benj", "Delaque", 820),
                          Gang("Smelling Rats", "Lucas", "Orlock", 820),
                          Gang("Coucou", "JD", "Van Saar", 820),
                          Gang("Encore", "Bidule", "Cawdor", 820),
                          Gang("Un", "Truc", "Escher", 820),
                          Gang("De plus", "Machin","Goliath", 820)]


            self.gangers = [Ganger("Rico","Rico and the Flying Ducks",3),
                            Ganger("Joe le Rigolo", "Rico and the Flying Ducks", 2),
                            Ganger("Rico","Smelling Rats",3),
                            Ganger("Joe le Rigolo", "Smelling Rats", 2),
                            Ganger("Rico", "Coucou", 3),
                            Ganger("Joe le Rigolo", "Coucou", 2),
                            Ganger("Rico", "Encore", 3),
                            Ganger("Joe le Rigolo", "Encore", 2),
                            Ganger("Rico", "Un", 3),
                            Ganger("Joe le Rigolo", "Un", 2),
                            Ganger("Rico", "De plus", 3),
                            Ganger("Joe le Rigolo", "De plus", 2)]

        # ---APPEL DES IMAGES---
        chef = tk.PhotoImage(file='img/chef.gif')
        self.chef = chef
        baleze_img = tk.PhotoImage(file='img/baleze.gif')
        self.baleze = baleze_img
        ganger_img = tk.PhotoImage(file='img/ganger.gif')
        self.ganger = ganger_img
        kid_img = tk.PhotoImage(file='img/kid.gif')
        self.kid = kid_img
        bg_img = tk.PhotoImage(file='img/bg.gif')
        self.bg_img = bg_img
        b_open = tk.PhotoImage(file='img/open.gif')
        self.b_open = b_open

        self.initUI()

    def initUI(self, liste=False):

        # ---SAUVEGARDE---
        # if fichier_svg:
            # self.enregistrer()

        # création d'un notebook
        self.ntb = ttk.Notebook(self, width=int(largeur*0.956), height=int(hauteur*0.92))
        self.ntb.grid(row=0, column=0)

        # ajout d'un onglet "accueil"
        self.home_tab = tk.Frame(self.ntb, bg=dark_grey)
        self.ntb.add(self.home_tab, text="Accueil")

        rel_size_x = (largeur/10000)*0.4
        rel_size_y = (hauteur/10000)*0.519

        size_y = hauteur/720
        size_x = largeur/1280*0.87

        # --TITRE

        img_size=1
        ban = tk.PhotoImage(file='img/ban.gif')
        self.ban = ban
        # self.ban.configure(width=int(852*img_size), height=int(80*img_size))
        tk.Label(self.home_tab, width=int(852*size_x), height=int(80*size_y), image=self.ban, bg=dark_grey).\
            grid(row=0, column=0, columnspan=2, sticky='nsew')


        # --VERSION

        vers = tk.PhotoImage(file='img/ban2.gif')
        self.vers = vers
        # self.vers.configure(width=int(426*img_size), height=int(80*img_size))
        tk.Label(self.home_tab, text="Version "+version, width=int(426*size_x), height=int(80*size_y),
                 image=self.vers, compound=tk.CENTER, fg='white', bg=dark_grey, font=FONT).grid(row=0, column=2, sticky='nsew')

        # bouton creer gang
        button = tk.PhotoImage(file='img/button.gif')
        self.button = button

        tk.Button(self.home_tab, text="Créer un nouveau Gang", command=self.newGang,
                  width=int(426*rel_size_x), height=int(50*rel_size_y), anchor='n', font=FONT).grid(row=1, column=0, sticky='nsew')

        nb_col = 3
        row_base = 2
        indice = 0

        fond = tk.PhotoImage(file='img/fond.gif')
        self.fond = fond

        # LISTES DES GANGS ET DES TRUCS
        for gg in self.gangs:

            # --AJOUT-DES-ONGLETS--
            tab = tk.Frame(self.ntb)
            self.ntb.add(tab, text=gg.nom, compound="bottom")

            # ----PAGE-PRINCIPALE---------------------------------------------------------------------------------------

            # --CREATION DE LA FRAME--
            fr_row=int(indice/nb_col)+row_base
            fr_col=(indice%nb_col)

            fr_gang = tk.Frame(self.home_tab, bd=2, bg='black')
            fr_gang.grid(row=fr_row, column=fr_col, sticky='nsew')

            # --NOM--
            len_max = 30
            nom = tk.StringVar()
            nom.set(gg.nom)

            l = tk.Button(fr_gang, textvariable=nom, command=lambda gg=gg: self.selectTab(gg._id), font=MENU_FONT
                          , width=int(426*size_x), height=int(134*size_y), anchor='n', bg=light_grey,
                          wraplength=len_max, image=self.fond, compound=tk.CENTER)

            l.grid(row=0, column=0, columnspan=4, sticky='nsew')

            # --JOUEUR--
            tk.Label(fr_gang, text="Joueur", width=int(67*rel_size_x), height=int(57*rel_size_y),
                     bg=light_grey, font=FONT).grid(row=1, column=0, sticky='nsew')
            joueur = tk.StringVar()
            joueur.set(gg.joueur)
            l = tk.Label(fr_gang, textvariable=joueur, width=int(67*rel_size_x), height=int(57*rel_size_y),
                         bg=lighter_grey, font=FONT)
            l.grid(row=2, column=0, sticky='nsew')

            # --MAISON--
            tk.Label(fr_gang, text="Maison", width=int(67*rel_size_x), height=int(57*rel_size_y),bg=light_grey
                     , font=FONT).grid(row=1, column=1, sticky='nsew')
            maison = tk.StringVar()
            maison.set(gg.maison)
            l = tk.Label(fr_gang, textvariable=maison, width=int(67*rel_size_x), height=int(57*rel_size_y),
                         bg=lighter_grey, font=FONT)
            l.grid(row=2, column=1, sticky='nsew')

            # --VALEUR--
            tk.Label(fr_gang, text="Valeur", width=int(67*rel_size_x), height=int(57*rel_size_y), bg=light_grey
                     , font=FONT).grid(row=1, column=2, sticky='nsew')

            valeur = tk.StringVar()
            valeur.set(gg.valeurGang(self.gangers))
            l = tk.Label(fr_gang, textvariable=valeur, width=int(67*rel_size_x), height=int(57*rel_size_y),
                         bg=lighter_grey, font=FONT).grid(row=2, column=2, sticky='nsew')

            # --NB-GANGERS
            tk.Label(fr_gang, text="Gangers", width=int(67*rel_size_x), height=int(57*rel_size_y), bg=light_grey
                     , font=FONT).grid(row=1, column=3, sticky='nsew')
            gg.listeGangers(self.gangers)
            nb_gr = len(gg.l_gangers)
            nb = tk.IntVar(value=nb_gr)
            l = tk.Label(fr_gang, textvariable=nb, width=int(67*rel_size_x), height=int(57*rel_size_y),
                         bg=lighter_grey, font=FONT)
            l.grid(row=2, column=3, sticky='nsew')

            # ----PAGE-DE-GANG------------------------------------------------------------------------------------------
            infos_gang = tk.Frame(tab, bg=darker_grey)
            infos_gang.pack(side='top', fill='x')

            rel_pg_x = 1
            rel_pg_y = 1

            # --NOM-DU-GANG--
            nom = tk.StringVar()
            nom.set(gg.nom)
            tk.Label(infos_gang, textvariable=nom, anchor='nw', font=MENU_FONT, bg=light_grey).grid(row=0, column=0, rowspan=2)

            # --MAISON--
            mai = tk.StringVar()
            mai.set("Maison : " + gg.maison)
            tk.Label(infos_gang, textvariable=mai, width=20, bg=lighter_grey).grid(row=0, column=1)

            # --VALEUR--
            val = tk.StringVar()
            val.set("Valeur : " + valeur.get())
            tk.Label(infos_gang, textvariable=val, width=20, bg=lighter_grey).grid(row=0, column=2)

            # --JOUEUR--
            jou = tk.StringVar()
            jou.set("Joueur : " + str(gg.joueur))
            tk.Label(infos_gang, textvariable=jou, width=20, bg=lighter_grey).grid(row=0, column=3)

            # --MAGOT--
            mago = tk.StringVar()
            mago.set(gg.magot)

            mag = tk.StringVar()
            mag.set("Magot : " + mago.get())
            tk.Label(infos_gang, textvariable=mag, width=20, font=MENU_FONT, bg=light_grey).grid(row=0, column=6)

            cmd = tk.Frame(tab, bg=lighter_grey)
            cmd.pack(side='top', fill='x')

            # --RETOUR--
            bt_home = tk.Button(cmd, text="Retour", command=lambda: self.ntb.select(0))
            bt_home.grid(row=0, column=0, sticky="w")

            # --RECRUTER--
            tk.Button(cmd, text="Recruter", command=lambda gg=gg: self.newGanger(gg)).grid(row=0, column=1)

            # --SUPPRIMER--
            tk.Button(cmd, text="Supprimer", command=lambda gg=gg: self.supprGang(gg)).grid(row=0, column=2)

            # ---SOUS INFOS---
            sous_info = tk.Frame(tab, height=50, bg=light_grey)
            sous_info.pack(side='bottom', fill='x')

            # ---BOUTONS---
            tk.Button(sous_info, text="Mode Admin", command=lambda gg=gg: self.modeAdmin(gg)).pack(side='right')
            tk.Button(sous_info, text="Post-bataille", command=lambda gg=gg: self.modePostBataille(gg)).pack(side='right')
            tk.Button(sous_info, text="Mode Bataille !").pack(side='right')

            # ---DATE CREATION
            dt_creation = tk.StringVar()
            dt_creation.set("Date de création : {}".format(gg.date_creation))

            tk.Label(sous_info, textvariable=dt_creation).pack(side='left')

            # ---STATS
            nb_vict = tk.StringVar()
            nb_vict.set("Victoires : {}/{}".format(gg.nb_vict[0], gg.nb_vict[1]))
            tk.Label(sous_info, textvariable=nb_vict).pack(side='left')

            nb_baleze = 0
            nb_gger = 0
            nb_kid = 0
            for gr in self.gangers:
                if gr.gang == gg.nom:
                    if gr.grade == 0:
                        nb_kid+=1
                    elif gr.grade == 1:
                        nb_gger+=1
                    elif gr.grade == 2:
                        nb_baleze+=1
                    else:
                        pass

            nb_truc = tk.StringVar()
            nb_truc.set("Balèzes : {}  Gangers : {}  Kids : {}".format(nb_baleze, nb_gger, nb_kid))

            tk.Label(sous_info, textvariable=nb_truc).pack(side='left')

            # ---AFFICHAGE LISTE
            if liste:

                # --BOUTON-BADGES--
                tk.Button(cmd, text="Mode Badge", command=lambda gg=gg: self.modListe(gg, False)).grid(row=0, column=3)

                # --LISTE-DES-GANGERS--
                aff_gangers = tk.Frame(tab, bg='green')
                aff_gangers.pack(side='left', fill='y')

                """CREATION DE LA LISTE DES GANGERS"""

                self.liste_gg = self.creerListeGangers(gg)

                # --LARGEUR-DES-COLONNES--
                w_col = [16, 17, 20, 15, 15, 5, 4, 10]
                col = 0
                row = 0

                # --LIBELLES--
                libelles = ("NOM", "CARACTERISTIQUES", "COMPETENCES", "EQUIPEMENT", "BLESSURES", "COUT", "XP", "RANG")

                for tit in libelles:
                    inti = tk.StringVar()
                    inti.set(tit)
                    tk.Label(aff_gangers, textvariable=inti, font=FONT, width=w_col[col]).grid(row=row, column=col, sticky='nsew')
                    col += 1

                i = 1
                # --AFFICHER-LISTE-DES-GANGERS-(FONCTION)--
                for gr in self.liste_gg:

                    # COL 0 --- NOM & GRADE
                    nom = tk.StringVar()
                    nom.set(gr.nom)
                    tk.Button(aff_gangers, textvariable=nom, command=lambda gr=gr: self.popUpGanger(gr)).grid(row=i, column=0,
                                                                                                         sticky='nsew')

                    grade = tk.StringVar()
                    grade.set(donnees.nom_grades[gr.grade])

                    tk.Label(aff_gangers, textvariable=grade).grid(row=i + 1, column=0, sticky='nsew')

                    # COL 1 --- CARAC

                    cc = tk.Frame(aff_gangers)
                    cc.grid(row=i, column=1, rowspan=2, sticky='nsew')
                    self.affCarac(cc, gr)

                    # COL 2 --- COMPETENCES
                    aff_comp = tk.Frame(aff_gangers)
                    aff_comp.grid(row=i, column=2, rowspan=2, sticky='nsew')
                    x = 0

                    for comp in gr.comp:
                        n_comp = tk.StringVar()
                        n_comp.set(comp)
                        ro = x % 2
                        co = int(x / 2)
                        tk.Button(aff_comp, textvariable=n_comp, command=lambda comp=comp: self.getCompText(comp)
                                  ).grid(row=ro, column=co, sticky='nsew')
                        x += 1

                    # COL 3 --- EQUIPEMENT
                    aff_equip = tk.Frame(aff_gangers)
                    aff_equip.grid(row=i, column=3, rowspan=2, sticky='nsew')
                    x = 0
                    for equ in self.triArsenal(gr.equip):
                        n_equ = tk.StringVar()
                        n_equ.set(equ)
                        ro = x % 2
                        co = int(x / 2)
                        tk.Label(aff_equip, textvariable=n_equ).grid(row=ro, column=co, sticky='nsew')
                        x += 1

                    # COL 4 --- BLESSURES
                    tk.Label(aff_gangers, textvariable=gr.bless).grid(row=i, column=4, rowspan=2, sticky='nsew')

                    # COL 5 --- COUT
                    cout = tk.IntVar()
                    cout.set(gr.cout)
                    tk.Label(aff_gangers, textvariable=cout).grid(row=i, column=5, rowspan=2, sticky='nsew')

                    # COL 6 --- EXPERIENCE
                    exp = tk.StringVar()
                    exp.set(gr.exp)
                    tk.Label(aff_gangers, textvariable=exp).grid(row=i, column=6, rowspan=2, sticky='nsew')

                    # COL 7 --- RANG
                    rang1 = tk.StringVar()
                    rang1.set("Rang {} :".format(gr.rang[0]))
                    tk.Label(aff_gangers, textvariable=rang1).grid(row=i, column=7, sticky='nsew')

                    rang2 = tk.StringVar()
                    rang2.set(gr.rang[1])
                    tk.Label(aff_gangers, textvariable=rang2).grid(row=i + 1, column=7, sticky='nsew')

                    # COL 8 --- EQUIPER

                    tk.Button(aff_gangers, text="Equiper", command=lambda gr=gr: self.popUpEquip(gr)).grid(row=i, column=8,
                                                                                                      sticky='nsew')
                    tk.Button(aff_gangers, text="Déséquiper", command=lambda gr=gr: self.desequip(gr)).grid(row=i + 1, column=8,
                                                                                                       sticky='nsew')

                    # COL 9 --- LEVEL UP
                    l_up = gr.rang[0] - gr.level_up
                    if l_up < 1:
                        tk.Label(aff_gangers, text="", width=5).grid(row=i, column=9, rowspan=2, sticky='nsew')
                    else:
                        l_up = "+" + str(l_up) + " !"
                        up = tk.StringVar()
                        up.set(l_up)
                        tk.Button(aff_gangers, textvariable=up, width=5, command=lambda gr=gr: self.levelUp(gr)
                                  ).grid(row=i, column=9, rowspan=2, sticky='nsew')

                    # --- INCREMENTATION
                    i += 2

            # ---AFFICHAGE BADGE
            else:
                # --BOUTON-BADGES--
                tk.Button(cmd, text="Mode Liste", command=lambda gg=gg: self.modListe(gg, True)).grid(row=0, column=3)


                # --LISTE-DES-GANGERS--
                aff_gangers = tk.Frame(tab, bg=dark_grey, padx=10, pady=10)
                aff_gangers.pack(side='left', fill='both')

                # --CREATION DE LA LISTE DES GANGERS--

                self.liste_gr = self.creerListeGangers(gg)

                liste_img=[self.kid, self.ganger, self.baleze, self.chef]

                g_li = 0
                g_col = 5
                g_indice = 0

                # ---AFFICHAGE DES BADGES---
                for gr in self.liste_gr:

                    b_row=int(g_indice/g_col)*8
                    b_col=(g_indice%g_col)

                    if g_indice%2 == 1:
                        bg_c = light_grey
                        bg_alt = lighter_grey
                    else:
                        bg_c = lighter_grey
                        bg_alt = light_grey

                    # --NOM--

                    tk.Button(aff_gangers, textvariable=gr.affNom(), width=20, command=lambda gr=gr: self.popUpGanger(gr),
                              font=TITLE_FONT).grid(row=b_row, column=b_col, sticky='nsew')

                    # --GRADE--

                    tk.Label(aff_gangers, textvariable=gr.affGrade(), bg=bg_c).grid(row=b_row+1,
                                                    column=b_col, sticky='nsew')

                    # --RANG--

                    lvl = tk.Frame(aff_gangers, width=100, height=75, bg=bg_c)
                    lvl.grid(row=b_row+2, column=b_col, sticky='nsew')
                    tk.Button(lvl, image=liste_img[gr.grade], width=100, command=lambda gr=gr: self.popUpGanger(gr),
                              height=75, bg=bg_c).pack(side='left')

                    # ---BARRE EXP---
                    rs = gr.rangSuivant()
                    r_ancien = rs[0]
                    r_suivant = rs[1]
                    r_actuel = gr.exp

                    if gr.exp == 0:
                        r_ancien=0

                    lv = (r_actuel-r_ancien)*100/(r_suivant-r_ancien)

                    cadre = tk.Label(lvl, width=9, bg=bg_c)
                    cadre.pack(side='right', fill='y')

                    ttk.Progressbar(lvl, orient='vertical', value=lv, length=70).pack(side='left', fill='y')

                    if r_ancien == 0:
                        ind = 0
                    else:
                        ind = 1

                    nb_max = tk.StringVar()
                    nb_max.set("- {}".format(r_suivant+ind))
                    nb_min = tk.StringVar()

                    nb_min.set("- {}".format(r_ancien+ind))
                    exp = tk.StringVar()
                    exp.set(gr.exp)
                    lvl_width = 3
                    tk.Label(cadre, textvariable=nb_max, width=lvl_width, font=("Helvetica", 10), anchor='w', bg=bg_c).pack(side='top', fill='x')
                    tk.Label(cadre, text='XP', width=lvl_width, bg=bg_c).pack(side='top')
                    tk.Label(cadre, textvariable=exp, width=lvl_width, height=1, font=("Helvetica", 20, "bold"), bg=bg_c).pack(side='top')
                    tk.Label(cadre, textvariable=nb_min, width=lvl_width, font=("Helvetica", 10), anchor='w', bg=bg_c).pack(side='bottom', fill='x')

                    # ---LEVEL UP---
                    l_up = gr.rang[0] - gr.level_up
                    if l_up < 1:
                        rg = gr.indiquerRang()
                        n_rg = tk.StringVar()
                        n_rg.set(rg[1])
                        tk.Label(aff_gangers, textvariable=n_rg, bg=bg_c).grid(row=b_row+3, column=b_col, sticky='nsew')
                    else:
                        l_up = "+" + str(l_up) + " !"
                        up = tk.StringVar()
                        up.set(l_up)
                        tk.Button(aff_gangers, bg=bg_c, textvariable=up, command=lambda gr=gr: self.levelUp(gr)
                                  ).grid(row=b_row+3, column=b_col, sticky='nsew')

                    # ---CARAC---

                    carac = gr.getCarac()
                    grille_carac = tk.Frame(aff_gangers, padx=4, bg=bg_alt)
                    grille_carac.grid(row=b_row+4, column=b_col, sticky='ew')
                    ind_c = 0
                    lg=2
                    for couple in carac:
                        cc_nom = tk.StringVar()
                        cc_nom.set(couple[0])
                        cc = tk.StringVar()
                        cc.set(couple[1])
                        tk.Label(grille_carac, padx=1, textvariable=cc_nom, width=lg, bg=bg_alt).grid(row=0, column=ind_c, sticky='nsew')
                        tk.Label(grille_carac, padx=1, textvariable=cc, width=lg, bg=bg_alt).grid(row=1, column=ind_c, sticky='nsew')
                        ind_c+=1

                    # ---ARMES---

                    ligne = 0
                    armes = self.triArsenal(gr.equip)

                    tk.Label(aff_gangers, text='', bg=bg_c).grid(row=b_row+6, column=b_col, sticky='nsew')

                    if len(armes)==0:
                        tk.Button(aff_gangers, text="Equiper", command=lambda gr=gr: self.popUpEquip(gr)).grid(
                            row=b_row+5+ligne, column=b_col)

                        ligne+=1
                    else:
                        for arme in armes:
                            n_arme=tk.StringVar()
                            n_arme.set(arme)
                            tk.Label(aff_gangers, textvariable=n_arme, bg=bg_c).grid(row=b_row+5+ligne, column=b_col, sticky='nsew')
                            ligne+=1

                    g_li+=g_indice*b_row

                    g_indice+=1


                # ---TERRITOIRES---
                territoires = tk.Label(tab, bg=darker_grey, image=self.bg_img, padx=20, pady=20)
                territoires.pack(side='top', fill='x')

                aff_territoires = tk.Frame(territoires, bg=darker_grey, padx=5, pady=5)
                aff_territoires.pack()

                tk.Label(aff_territoires, text="TERRITOIRES", font=TITLE_FONT, bg=dark_grey, fg=lighter_grey, width=20
                         ).grid(row=0, column=0, columnspan=2, sticky='ew')


                if len(gg.territoires) == 0:
                    tk.Button(aff_territoires, text="Générer des territoires",
                              command=lambda gg=gg: terrDebut(gg)).grid(row=1, column=0, columnspan=2,
                                                                        sticky='nsew')
                else:
                    ro = 1
                    for terr in sorted(gg.territoires):
                        if ro%2 == 0:
                            bg_terr = light_grey
                        else:
                            bg_terr = lighter_grey

                        terr_vue = tk.Button(aff_territoires, image=self.b_open, command=lambda terr=terr: self.popUpTerr(terr)).grid(row=ro, column=0)

                        n_terr = tk.StringVar()
                        n_terr.set(terr)
                        tk.Label(aff_territoires, textvariable=n_terr, anchor='w', bg=bg_terr).grid(row=ro, column=1, sticky='nsew')

                        revenu = donnees.territ_revenu[terr]
                        n_rev = tk.StringVar()
                        n_rev.set(revenu)
                        tk.Label(aff_territoires, textvariable=n_rev, bg=bg_terr).grid(row=ro, column=2, sticky='nsew')
                        ro += 1

                def terrDebut(gang):
                    i = 5
                    while i != 0:
                        self.newTerritoire(gang)
                        i -= 1
                    interface.initUI()
                    self.selectTab(gang._id)

                tk.Frame(tab, bg=dark_grey, height=5).pack(side='top', fill='x')

                # --ARSENAL--
                aff_arsenal = tk.Frame(tab, bg=darker_grey, padx=10, pady=10)
                aff_arsenal.pack(side='top', fill='both')

                # ---CREATION DE L'ARSENAL
                gun_libre = self.triArsenal(gg.arsenal)

                o_gun_pris=[]
                for gr in self.liste_gr:
                    for gun in gr.equip:
                        o_gun_pris.append(gun)

                gun_pris = self.triArsenal(o_gun_pris)

                # ---ARMES DISPO
                tk.Label(aff_arsenal, text="ARSENAL", font=TITLE_FONT, bg=dark_grey, fg=lighter_grey, width=29
                         ).grid(row=0, sticky='nsew')
                lig = 1

                if len(gun_libre)==0:
                    tk.Label(aff_arsenal, text='aucune arme disponible', bg=lighter_grey, fg=dark_grey).grid(
                        row=lig, sticky='ew')
                    lig+=1

                for gun in gun_libre:
                    if lig%2 == 1:
                        bg_ars = lighter_grey
                    else:
                        bg_ars = light_grey
                    n_gun = tk.StringVar()
                    n_gun.set(gun)
                    tk.Label(aff_arsenal, textvariable=n_gun, bg=bg_ars).grid(row=lig, sticky='nsew')
                    lig += 1

                # ---SEP
                tk.Label(aff_arsenal, bg=dark_grey, height=1).grid(row=lig, sticky='ew')

                # ---ARMES NON DISPO
                tk.Label(aff_arsenal, text="Armes déjà équipées", bg=darker_grey, fg=lighter_grey).grid(row=lig+1, sticky='nsew')
                lig += 2

                for gun in gun_pris:
                    if lig%2 == 1:
                        bg_a = lighter_grey
                        fg_a = dark_grey
                    else:
                        bg_a = light_grey
                        fg_a = darker_grey

                    n_gun = tk.StringVar()
                    n_gun.set(gun)
                    tk.Label(aff_arsenal, textvariable=n_gun, bg=bg_a, fg=fg_a).grid(row=lig, sticky='nsew')
                    lig += 1

            # ---ITERATION DE LA BOUCLE GENERALE---
            indice += 1

    # ----FONCTIONS-DE-TRI-----------------------------------------------------------------------------------------------

    # ---CREER LA LISTE DES GANGERS D'UN GANG DEFINI
    def creerListeGangers(self, gang):
        liste_gg = []
        for gg in self.gangers:
            if gg.gang == gang.nom:
                liste_gg.append(gg)
        return sorted(liste_gg, key=attrgetter("grade", "exp"), reverse=True)

    # ---RECUPERER LA MAISON DU GANGER
    def getMaison(self, ganger, listeGangs):
        gang = ganger.gang
        for g in listeGangs:
            if gang == g.nom:
                return g.maison

#----FONCTION-DE-NAVIGATION---------------------------------------------------------------------------------------------

    # ---CHANGER D'ONGLET
    def selectTab(self, _id):
        """ sélectionner un onglet """
        self.ntb.select(_id)

    # ---POP-UP-GANGER
    def popUpGanger(self,ganger):
        pop = tk.Toplevel()
        pop.config(padx=20, pady=20)

        pop_nom = tk.StringVar()
        pop_nom.set(ganger.nom)
        tk.Label(pop, textvariable=pop_nom).grid(row=0, column=0, columnspan=3)



        ng = tk.StringVar()
        gr = donnees.nom_grades[ganger.grade]
        ng.set(gr)

        tk.Label(pop, textvariable=ng).grid(row=1, column=0, columnspan=3)

        # COL 1 --- CARAC

        cc = tk.Frame(pop)
        cc.grid(row=2, column=0, columnspan=3)
        self.affCarac(cc, ganger)

        nb_ligne = []
        # COL 2 --- COMPETENCES
        r_span = len(ganger.comp)
        nb_ligne.append(r_span)
        tk.Label(pop, text="Compétences").grid(row=3, column=0)
        r_cp = 4 #Ligne de départ
        for cp in ganger.comp:
            n_cp = tk.StringVar()
            n_cp.set(cp)
            tk.Label(pop, textvariable=n_cp).grid(row=r_cp, column=0)
            r_cp+=1

        # COL 3 --- EQUIPEMENT
        r_span = len(ganger.equip)
        nb_ligne.append(r_span)
        tk.Label(pop, text="Equipement").grid(row=3, column=1)
        r_eq = 4 #Ligne de départ
        for eq in ganger.equip:
            n_eq = tk.StringVar()
            n_eq.set(eq)
            tk.Label(pop, textvariable=n_eq).grid(row=r_eq, column=1)
            r_eq += 1

        # COL 4 --- BLESSURES
        r_span = len(ganger.bless)
        nb_ligne.append(r_span)
        tk.Label(pop, text="Blessures").grid(row=3, column=2)
        r_bl = 4  # Ligne de départ
        for bl in ganger.bless:
            n_bl = tk.StringVar()
            n_bl.set(bl)
            tk.Label(pop, textvariable=n_bl).grid(row=r_bl, column=1)
            r_eq += 1

        new_ligne = max(nb_ligne)+4

        # COL 5 --- COUT
        tk.Label(pop, text="Coût").grid(row=new_ligne, column=0)
        cout = tk.IntVar()
        cout.set(ganger.cout)
        tk.Label(pop, textvariable=cout).grid(row=new_ligne+1, column=0)

        # COL 6 --- EXPERIENCE
        tk.Label(pop, text="Exp").grid(row=new_ligne, column=1)
        exp = tk.StringVar()
        exp.set(ganger.exp)
        tk.Label(pop, textvariable=exp).grid(row=new_ligne+1, column=1)

        # COL 7 --- RANG
        tk.Label(pop, text="Rang").grid(row=new_ligne, column=2)
        rang = tk.StringVar()
        rang.set(str(ganger.rang[0]) + " : " + ganger.rang[1])
        tk.Label(pop, textvariable=rang).grid(row=new_ligne+1, column=2)

        # COL 8 --- LEVEL UP
        l_up = ganger.rang[0] - ganger.level_up
        if l_up < 1:
            pass
        else:
            l_up = "+" + str(l_up) + " !"

            up = tk.StringVar()
            up.set(l_up)

            tk.Button(pop, textvariable=up, command=lambda :self.levelUp(ganger)).grid(row=new_ligne+2, column=0)

        tk.Button(pop, text="Equiper", command=lambda gr=gr: self.popUpEquip(ganger)).grid(row=new_ligne+2, column=1)
        tk.Button(pop, text="Supprimer", command=lambda : self.supprGanger(pop, ganger)).grid(row=new_ligne+2, column=2)

        pop.mainloop()

    # ---OBTENIR LE GANG
    def getGang(self, ganger):
        for gg in self.gangs:
            if gg.nom == ganger.gang:
                return gg

    # ---POP-UP-EQUIPEMENT
    def popUpEquip(self, ganger):
        pop = tk.Toplevel()

        maison = self.getMaison(ganger, self.gangs)

        tk.Label(pop, text="Equipement disponible").grid(row=0, column=0, columnspan=3)
        tk.Label(pop, text="Coût").grid(row=1, column=1)

        i=1
        for style in donnees.armes_grade[ganger.grade]:
            n_style = tk.StringVar()
            n_style.set(style)
            tk.Label(pop, textvariable=n_style, font=TITLE_FONT, width=30).grid(row=i, column=0)
            i+=1
            for gun in donnees.armes_debut[maison][style]:
                n_gun = tk.StringVar()
                n_gun.set(gun)
                tk.Button(pop, textvariable=n_gun, width=30).grid(row=i, column=0)
                prix = donnees.arsenal[gun][0]
                n_prix = tk.StringVar()
                n_prix.set(prix)
                tk.Label(pop, textvariable=n_prix).grid(row=i, column=1)
                tk.Button(pop, text="Acheter", command=lambda gun=gun: valAchat(gun)).grid(row=i, column=2)
                i+=1

        tk.Label(pop, text="Choisir dans l'arsenal").grid(row=1, column=3)
        gg = self.getGang(ganger)
        col = 3
        ro=2
        for equ in sorted(gg.arsenal):
            n_equ = tk.StringVar()
            n_equ.set(equ)
            tk.Button(pop, textvariable=n_equ, command=lambda equ=equ: choisirEqu(equ)).grid(row=ro, column=col)
            ro+=1

        def choisirEqu(equ):
            self.affecterEqu(gg, equ, ganger)
            interface.initUI()
            self.selectTab(ganger.getID(self.gangs))
            pop.destroy()


        def valAchat(equip):
            self.acheterEqu(gg, equip)
            self.affecterEqu(gg, equip, ganger)
            interface.initUI()
            self.selectTab(gg._id)
            pop.destroy()



        pop.mainloop()

    # ---TRI-DE-L'ARSENAL-(RENVOIE-UNE-LISTE-ORDONNEE)
    def triArsenal(self, arsenal):
        tri = {}

        for obj in arsenal:
            try:
                tri[obj] += 1
            except:
                tri[obj] = 1

        aff_ars = []
        for key, value in tri.items():
            if value == 1:
                aff_ars.append(key)
            else:
                txt = "{} x{}".format(key, value)
                aff_ars.append(txt)
        return sorted(aff_ars)

    # ----FONCTIONS-DE-CREATION------------------------------------------------------------------------------------------

    #---CREER UN GANG
    def newGang(self):
        f = tk.Toplevel()
        f.config(padx=20, pady=20)

        tk.Label(f, text="Nom du gang :").grid(row=0, column=0, columnspan=2)
        ng_nom = tk.Entry(f,width=30)
        ng_nom.grid(row=1, column=0, columnspan=2)

        tk.Label(f, text="Joueur :").grid(row=2, column=0, columnspan=2)
        ng_joueur = tk.Entry(f, width=30)
        ng_joueur.grid(row=3, column=0, columnspan=2)

        tk.Label(f, text="Maison :").grid(row=4, column=0, columnspan=2)
        maison = tk.StringVar(value='Choisissez votre maison')
        tk.OptionMenu(f, maison, *donnees.noms_maison).grid(row=5, column=0, columnspan=2)

        tk.Button(f, text="Annuler", command=f.destroy).grid(row=9, column=0)
        tk.Button(f, text="Valider", command=lambda: val_newGang(ng_nom.get(),ng_joueur.get(),maison.get())).grid(row=9, column=1)

        tk.Label(f, text="Descriptions : ").grid(row=0, column=2)

        l_ms = 1
        for ms in donnees.noms_maison:
            n_ms = tk.StringVar()
            n_ms.set(ms)
            tk.Button(f, textvariable=n_ms, command=lambda ms=ms:self.getMaisonText(ms)).grid(row=l_ms, column=2)
            l_ms+=1

        def val_newGang(nom, joueur, maison):
            if nom == "":
                tk.messagebox.showwarning("Attention", "Vous n'avez pas entré de nom pour votre gang !")
            elif joueur == "":
                tk.messagebox.showwarning("Attention", "Vous n'avez pas indiqué votre nom !")
            elif maison not in ['Cawdor', 'Escher', 'Delaque','Goliaths', 'Orlocks', 'Van Saar']:
                tk.messagebox.showwarning("Attention", "Choisis une maison, connard ...")
            else:
                n_gang = (Gang(nom,joueur,maison))
                self.gangs.append(n_gang)
                interface.initUI()
                self.selectTab(n_gang._id)
                f.destroy()

        f.mainloop()

    #---CREER UN GANGER
    def newGanger(self, gang):
        fen = tk.Toplevel()
        fen.config(padx=20, pady=20)

        tk.Label(fen, text="Nom :").grid(row=0, column=0, columnspan=2)
        ngg_nom = tk.Entry(fen, width=30)
        ngg_nom.grid(row=1, column=0, columnspan=2)

        chef_max = False

        for ggr in self.gangers:
            if ggr.gang == gang.nom and ggr.grade == 3:
                chef_max = True

        nb_bleze = 0

        for ggr in self.gangers:
            if ggr.gang == gang.nom and ggr.grade == 2:
                nb_bleze+=1

        if chef_max == False and nb_bleze<2 :
            list_grades = ["Chef de Gang", "Balèze","Ganger","Kid"]
        elif chef_max and nb_bleze<2:
            list_grades = ["Balèze", "Ganger", "Kid"]
        else:
            list_grades = ["Ganger", "Kid"]

        tk.Label(fen, text="Grade :").grid(row=2, column=0, columnspan=2)
        grade = tk.StringVar(value='Sélectionnez un grade')
        ngg_grade = tk.OptionMenu(fen, grade, *list_grades)
        ngg_grade.grid(row=3, column=0, columnspan=2)

        tk.Button(fen, text="Annuler", command=fen.destroy).grid(row=5, column=0)
        tk.Button(fen, text="Valider", command=lambda: val_newGanger(ngg_nom.get(), grade.get(), gang)).grid(row=5, column=1)

        def val_newGanger(nom, grade, gang):
            if nom == "":
                tk.messagebox.showwarning("Attention", "Vous n'avez pas donnée de nom à votre ganger !")
            elif grade not in donnees.nom_grades:
                tk.messagebox.showwarning("Attention", "Veuillez choisir un grade")
            else:
                if grade == 'Chef de Gang':
                    n_gr = 3
                elif grade == 'Balèze':
                    n_gr = 2
                elif grade == 'Ganger':
                    n_gr = 1
                elif grade == 'Kid':
                    n_gr = 0

                if gang.depenser(donnees.cout_recrut[n_gr]):
                    n_ganger = (Ganger(nom, gang.nom, n_gr))

                    self.gangers.append(n_ganger)
                    interface.initUI()
                    self.selectTab(n_ganger.getID(self.gangs))
                    fen.destroy()

        fen.mainloop()

    # ----FONCTIONS-DE-MODIFICATION--------------------------------------------------------------------------------------

    # ---MODE POST-BATAILLE
    def modePostBataille(self, gang):
        pass


    # ---MODE ADMIN
    def modeAdmin(self, gang):
        self.mod_admin = tk.Toplevel()

        tk.Label(self.mod_admin, text="Mode Admin", font=TITLE_FONT).grid()
        tk.Label(self.mod_admin, text="Modifiez les informations sans contre-partie. "
                                 "Utilisez ces fonctions pour recréer un gang existant", wraplength=310).grid()

        tk.Button(self.mod_admin, text="Infos du Gang", command=lambda :self.adminInfos(gang)).grid(sticky='nsew')
        tk.Button(self.mod_admin, text="Territoires").grid(sticky='nsew')
        tk.Button(self.mod_admin, text="Arsenal").grid(sticky='nsew')
        tk.Button(self.mod_admin, text="Gangers").grid(sticky='nsew')

        self.mod_admin.mainloop()

    def adminInfos(self, gang):
        self.mod_admin.destroy()
        admin_info = tk.Toplevel()

        # ---NOM---
        tk.Label(admin_info, text="Nom : ").grid(row=0, column=0)
        n_nom = tk.Entry(admin_info, textvariable=gang.affNom())
        n_nom.grid(row=0, column=1)

        # ---JOUEUR---
        tk.Label(admin_info, text="Joueur : ").grid(row=1, column=0)
        n_joueur = tk.Entry(admin_info, textvariable=gang.affJoueur())
        n_joueur.grid(row=1, column=1)

        # ---MAGOT---
        tk.Label(admin_info, text="Magot : ").grid(row=2, column=0)
        n_magot = tk.Entry(admin_info, textvariable=gang.affMagot())
        n_magot.grid(row=2, column=1)

        # ---BATAILLES---
        bat = tk.Frame(admin_info)
        bat.grid(row=3, column=0, columnspan=2, sticky='ew')

        nb_vict = gang.affVict()

        tk.Label(bat, text="Victoires/Batailles : ", anchor='w').grid(row=0, column=0, sticky='w')
        vict = tk.Entry(bat, textvariable=nb_vict[0], width=2)
        vict.grid(row=0, column=1)
        tk.Label(bat, text="/").grid(row=0, column=2)
        tot = tk.Entry(bat, textvariable=nb_vict[1], width=2)
        tot.grid(row=0, column=3)

        # ---CREATION---

        tk.Label(admin_info, text="Date de création").grid(row=4, column=0)
        n_date = tk.Entry(admin_info, textvariable=gang.affDateCreation())
        n_date.grid(row=4, column=1)

        # ---COMMAND---

        tk.Button(admin_info, text="Annuler", command=lambda : admin_info.destroy()).grid(row=5, column=0)
        tk.Button(admin_info, text="Valider", command=lambda : vaLInfos(gang, n_nom, n_joueur, n_magot, vict, tot,
                                                                        n_date)).grid(row=5, column=1)

        def vaLInfos(gang, nom, joueur, magot, vict, tot, date):
            n_nom = nom.get()
            n_joueur = joueur.get()
            n_magot = magot.get()
            n_nb_vict = [int(vict.get()), int(tot.get())]
            n_date = date.get()
            l_grs = self.creerListeGangers(gang)
            for gr in l_grs:
                gr.setGang(n_nom)

            gang.setNom(n_nom)
            gang.setJoueur(n_joueur)
            gang.setMagot(int(n_magot))
            gang.setNbVict(n_nb_vict)
            gang.setDateCreation(n_date)

            interface.initUI()
            self.selectTab(gang._id)
            admin_info.destroy()






        admin_info.mainloop()


    # ---LEVEL UP
    def levelUp(self, ganger):
        err=True
        while err:
            r = D6(2)
            if r in [2,12]:
                tk.messagebox.showinfo("Level Up !", "Vous pouvez choisir dans n'importe quelle"
                                                     "famille de compétence !")
                self.popComp(ganger, True)
                err = False

            elif r in [3,4,10,11]:
                tk.messagebox.showinfo("Level Up !", "Vous pouvez choisir parmi les"
                                                     "compétences autorisées !")
                self.popComp(ganger)
                err = False

            elif r == 5:
                nr = D6()
                if nr <= 3:
                    if ganger.carac[3]==donnees.stats_max[3]:
                        err=True
                    else:
                        tk.messagebox.showinfo("Level Up !", "+1 en Force ! (F)")
                        self.modCarac(ganger, 3, 1)
                        err = False
                else:
                    if ganger.carac[7] == donnees.stats_max[7]:
                        err = True
                    else:
                        tk.messagebox.showinfo("Level Up !", "+1 Attaque ! (A)")
                        self.modCarac(ganger, 7, 1)
                        err = False

            elif r in [6,8]:
                nr = D6()
                if nr <= 3:
                    if ganger.carac[1] == donnees.stats_max[1]:
                        err = True
                    else:
                        tk.messagebox.showinfo("Level Up !", "+1 en Capacité de Combat ! (CC)")
                        self.modCarac(ganger, 1, 1)
                        err = False
                else:
                    if ganger.carac[2] == donnees.stats_max[2]:
                        err = True
                    else:
                        tk.messagebox.showinfo("Level Up !", "+1 en Capacité de Tir ! (CT)")
                        self.modCarac(ganger, 2, 1)
                        err = False

            elif r == 7:
                nr = D6()
                if nr <= 3:
                    if ganger.carac[6] == donnees.stats_max[6]:
                        err = True
                    else:
                        tk.messagebox.showinfo("Level Up !", "+1 en Initiative ! (I)")
                        self.modCarac(ganger, 6, 1)
                        err = False
                else:
                    if ganger.carac[8] == donnees.stats_max[8]:
                        err = True
                    else:
                        tk.messagebox.showinfo("Level Up !", "+1 en Commandement ! (Cd)")
                        self.modCarac(ganger, 8, 1)
                        err = False

            elif r == 9:
                nr = D6()
                if nr <= 3:
                    if ganger.carac[5] == donnees.stats_max[5]:
                        err = True
                    else:
                        tk.messagebox.showinfo("Level Up !", "+1 Point de Vie ! (PV)")
                        self.modCarac(ganger, 5, 1)
                        err = False
                else:
                    if ganger.carac[4] == donnees.stats_max[4]:
                        err = True
                    else:
                        tk.messagebox.showinfo("Level Up !", "+1 en Endurance ! (E)")
                        self.modCarac(ganger, 4, 1)
                        err = False

    # ---MODIFICATION-D'UNE-CARACTERISTIQUE
    def modCarac(self, ganger, carac, modif):
        ganger.carac[carac]+=modif
        ganger.level_up+=1
        interface.initUI()
        self.selectTab(ganger.getID(self.gangs))

    # ---CHOIX-DE-LA-CARACTERISTIQUE-A-MODIFIER
    def anyCarac(self, ganger):
        fen = tk.Toplevel()

        tk.Label(fen, text="Vous pouvez choisir la caractéristique à augmenter :").grid(row=0, column=0, columnspan=9)
        li = 0
        for c in ganger.carac:
            nm = donnees.noms_stats[li]
            nom = tk.StringVar()
            nom.set(nm)

            bg_c = donnees.couleurs_stats[li][c]

            tk.Label(fen, textvariable=nom, width=2).grid(row=1, column=li)
            cac = tk.StringVar()
            cac.set(c)
            tk.Label(fen, textvariable=cac, bg=bg_c).grid(row=2, column=li)
            li += 1

        fen.mainloop()

    # ---GANGER : Ajouter une compétences
    def ajoutComp(self, parent, ganger, comp_type):
        list_comp=[]
        for comp in donnees.competences[comp_type]:
            if comp not in ganger.comp:
                list_comp.append(comp)

        n_comp = choice(list_comp)
        if n_comp == "Tir rapide":
            parent.destroy()
            pop = tk.Toplevel()

            tk.Label(pop, text="Tir rapide !").grid(row=0, column=0, columnspan=2)
            tk.Label(pop, text="Cette compétence doit être assignée à une arme :").grid(row=0, column=0, columnspan=2)


            tk.Label(pop, text="Pistolets").grid(row=2, column=0)
            li=3
            for key, value in donnees.arsenal.items():
                if value[3] == "Pistolets":
                    n_value = tk.StringVar()
                    n_value.set(key)
                    tk.Button(pop, textvariable=n_value, command=lambda key=key:validTR(ganger, key)).grid(row=li, column=0)
                    li+=1

            li=3
            tk.Label(pop, text="Armes de base").grid(row=2, column=1)
            for key, value in donnees.arsenal.items():
                if value[3] == "Armes de base":
                    n_value = tk.StringVar()
                    n_value.set(key)
                    tk.Button(pop, textvariable=n_value, command=lambda key=key:validTR(ganger, key)).grid(row=li, column=1)
                    li+=1
            def validTR(ganger, arme):
                ganger.comp.append("Tir rapide ({})".format(arme))
                ganger.level_up+=1
                interface.initUI()
                self.selectTab(ganger.getID(self.gangs))
                pop.destroy()

            pop.mainloop()
        else:
            ganger.comp.append(n_comp)
            tk.messagebox.showinfo(n_comp, texts.comp_text[n_comp])
            ganger.level_up+=1
            interface.initUI()
            self.selectTab(ganger.getID(self.gangs))

        parent.destroy()

    # ----FONCTION-DE-L'ARSENAL------------------------------------------------------------------------------------------

    def acheterEqu(self, gang, equ):
        prix = donnees.arsenal[equ][0]
        if gang.depenser(prix):
            gang.arsenal.append(equ)

    def affecterEqu(self, gang, equ, ganger):
        if equ in gang.arsenal:
            gang.arsenal.remove(equ)
            ganger.equip.append(equ)

    def desequip(self, ganger):
        for gg in self.gangs:
            if gg.nom == ganger.gang:
                gang = gg
        for equ in ganger.equip:
            ganger.equip.remove(equ)
            gang.arsenal.append(equ)

        interface.initUI()
        self.selectTab(gang._id)

    # ----FONCTION-D'AFFICHAGE-------------------------------------------------------------------------------------------

    def modListe(self, gang, liste):
        liste = liste
        interface.initUI(liste)
        self.selectTab(gang._id)

    # ---AFFICHER LES CARACTERISTIQUES
    def affCarac(self, parent, ganger, couleur=False):
        li = 0
        for c in ganger.carac:
            nm = donnees.noms_stats[li]
            nom = tk.StringVar()
            nom.set(nm)
            if couleur:
                bg_c = donnees.couleurs_stats[li][c]
            else:
                bg_c = 'white'

            tk.Label(parent, textvariable=nom, width=2).grid(row=0, column=li)
            cac = tk.StringVar()
            cac.set(c)
            tk.Label(parent, textvariable=cac, bg=bg_c).grid(row=1, column=li)
            li += 1

    # ---AFFICHER LA LISTE DES COMPETENCES DISPONIBLES POUR UN GANGER DEFINI
    def popComp(self, ganger, all=False):
        pop = tk.Toplevel()

        maison = self.getMaison(ganger, self.gangs)
        comps = donnees.comp_dispos[maison][ganger.grade]

        tk.Label(pop, text="Listes des compétences").grid(row=0, column=0, columnspan=7)
        if debug:
            print("Compétences disponibles pour : {}".format(ganger.nom))
            print(comps)

        i = 0

        for nom in comps[0]:
            if debug:
                print(nom)
            n_nom = donnees.comp_noms[nom]
            nn_nom = tk.StringVar()
            nn_nom.set(n_nom)
            tk.Button(pop, textvariable=nn_nom, font=TITLE_FONT, width=20,
                      command=lambda n_nom=n_nom: self.ajoutComp(pop, ganger, n_nom)).grid(row=1, column=i)
            row = 2
            for valeur in donnees.competences[n_nom]:
                n_valeur = tk.StringVar()
                n_valeur.set(valeur)
                if n_valeur.get() in ganger.comp:
                    tk.Label(pop, textvariable=n_valeur, width=20).grid(row=row, column=i)
                else:
                    tk.Button(pop, textvariable=n_valeur, width=20, command=lambda n_valeur=n_valeur: self.getCompText(n_valeur.get())).grid(row=row, column=i)
                row += 1
            i += 1
        if all:
            for nom in comps[1]:
                n_nom = donnees.comp_noms[nom]
                nn_nom = tk.StringVar()
                nn_nom.set(n_nom)
                aff_nom = tk.StringVar()

                aff_nom.set(nn_nom.get()+' *')

                tk.Button(pop, textvariable=aff_nom, font=TITLE_FONT, width=20, bg="blue",
                          command=lambda n_nom=n_nom: self.ajoutComp(pop, ganger, n_nom)).grid(row=1, column=i)
                row = 2
                for valeur in donnees.competences[n_nom]:
                    n_valeur = tk.StringVar()
                    n_valeur.set(valeur)
                    tk.Button(pop, textvariable=n_valeur, width=20, fg="green", command=lambda n_valeur=n_valeur: self.getCompText(n_valeur.get())).grid(row=row, column=i)
                    row += 1
                i += 1
            tk.Label(pop, text="* = Domaine de compétence normalement verrouillé").grid(row=i+1, column=4, columnspan=3)

        pop.mainloop()

    # ---AFFICHER LA DESCRIPTION D'UNE COMPETENCES (POP UP)
    def getCompText(self, comp):
        fen = tk.Toplevel(padx=20, pady=20)
        n_comp = tk.StringVar()
        n_comp.set(comp)

        tk.Label(fen, textvariable = n_comp, font=TITLE_FONT).grid()
        txt = texts.comp_text[comp]
        pg = tk.Text(fen, wrap="word")
        pg.insert(tk.INSERT, txt)
        pg.grid()

        tk.Button(fen, text="Retour", command=fen.destroy).grid()

        fen.mainloop()

    # ---AFFICHER LA DESCRIPTION D'UNE MAISON
    def getMaisonText(self, maison):
        top = tk.Toplevel()

        side = choice(['dr', 'gh'])

        if side == 'dr':
            img_s = 0
            txt_s = 1
        else:
            img_s = 1
            txt_s = 0

        txt_m = texts.maison_text[maison]

        chemin = txt_m[0]
        img = tk.PhotoImage(file=chemin)
        photo_label = tk.Label(top, image=img)
        photo_label.grid(row=0, column=img_s, rowspan=3)
        photo_label.image = img

        var = maison
        tk.Label(top, text=var).grid(row=0, column=txt_s, ipadx=10, ipady=10)

        par1 = tk.Text(top, wrap="word", height=10)
        par1.insert(tk.INSERT, txt_m[1])
        par1.grid(row=1, column=txt_s, padx=30, ipady=10)

        par2 = tk.Text(top, wrap="word", height=10)
        par2.insert(tk.END, txt_m[2])
        par2.grid(row=2, column=txt_s, padx=30, ipady=10)

        top.mainloop()

    # ----FONCTIONS-DE-SUPPRESSION---------------------------------------------------------------------------------------

    def supprGang(self, gang):

        rep = tk.messagebox.askokcancel("Suppression",
                                            "Êtes-vous sûr de vouloir supprimer {} et tous ses gangers ?".format(gang.nom))
        if rep:
            for gg in self.gangers:
                if gg.gang == gang.nom:
                    self.gangers.remove(gg)
            self.gangs.remove(gang)

            interface.initUI()

    def supprGanger(self, parent, ganger):
        rep = tk.messagebox.askokcancel("Suppresion",
                                        "Êtes-vous sûr de vouloir supprimer {} ?".format(ganger.nom))
        if rep:
            self.gangers.remove(ganger)
            for gg in self.gangs:
                if ganger.gang == gg.nom:
                    gg.l_gangers.remove(ganger.nom)

            interface.initUI()
            self.selectTab(ganger.getID())
            parent.destroy()

    # ----FONCTIONS-D'ACCES_AUX_FICHIERS---------------------------------------------------------------------------------

    # Fonction permettant la reconstruction
    def preprocessGang(self, dict_, authorized, ban):
        dict_args, dict_others = {}, {}
        for key, value in dict_.items():
            if key in authorized:
                dict_args[key] = value
            elif key not in ban:
                dict_others[key] = value

        gang = Gang(**dict_args)
        gang.__dict__.update(dict_others)

        return gang

    def preprocessGanger(self, dict_, authorized, ban):
        dict_args, dict_others = {}, {}
        for key, value in dict_.items():
            if key in authorized:
                dict_args[key] = value
            elif key not in ban:
                dict_others[key] = value

        ganger = Ganger(**dict_args)
        ganger.__dict__.update(dict_others)

        return ganger

    def enregistrer(self):
        try :
            l_gg=[]
            for gg in self.gangs:
                n_gg = gg.__dict__
                l_gg.append(n_gg)

            l_gr=[]
            for gr in self.gangers:
                n_gr = gr.__dict__
                l_gr.append(n_gr)

            with open('save/gangs.txt', 'w') as fichier:
                json.dump(l_gg, fichier, indent=4)

            with open('save/gangers.txt', 'w') as fichier:
                json.dump(l_gr, fichier, indent=4)
            print("Sauvegarde réussie")
        except:
            print("Erreur de sauvegarde")

    def chargerSave(self):
        try:
            with open('save/gangs.txt', 'r') as fichier:
                l_gg = json.load(fichier)
            with open('save/gangers.txt', 'r') as fichier:
                l_gr = json.load(fichier)

            gangs = []
            for gg in l_gg:
                n_gg = self.preprocessGang(gg, {"nom", "joueur", "maison", "magot"}, {"l_gangers", "_id"})
                gangs.append(n_gg)
            gangers = []
            for gr in l_gr:
                n_gr = self.preprocessGanger(gr, {"nom", "gang", "grade"}, {})
                gangers.append(n_gr)
            return [gangs, gangers]
        except:
            print("Erreur au chargement de la sauvegarde")

    # ----TERRITOIRES----------------------------------------------------------------------------------------------------
    def newTerritoire(self, gang):
        de = D6()*10+D6()

        if de == 11:
            terr = "Fosse chimique"
        elif de in range(12, 17):
            terr = "Champ de ruines"
        elif de in range(21, 26):
            terr = "Scories"
        elif de == 26:
            terr = "Gisement Minéral"
        elif de in range(31, 36):
            terr = "Colonie"
        elif de == 36:
            terr = "Mine"
        elif de in range(41, 43):
            terr = "Tunnels"
        elif de in range(43, 45):
            terr = "Conduits de ventilation"
        elif de in range(45, 47):
            terr = "Ferme"
        elif de in range(51, 53):
            terr = "Pompe à eau"
        elif de in range(53, 55):
            terr = "Taverne"
        elif de in range(55, 57):
            terr = "Relations Commerciales"
        elif de == 61:
            terr = "Toubib"
        elif de == 62:
            terr = "Atelier"
        elif de == 63:
            terr = "Tripot"
        elif de == 64:
            terr = "Champignonnère"
        elif de == 65:
            terr = "Archéotechnologie"
        elif de == 66:
            terr = "Pieds-tendres"
        else:
            pass

        txt = texts.territ_descr[terr]
        tk.messagebox.showinfo(terr, txt)
        if terr == "Pieds-tendres":
            pieds = tk.Toplevel()
            pieds.title("Pieds-tendres")
            tk.Label(pieds, text="Choisissez un territoire :", font=TITLE_FONT).grid(row=0, column=0, columnspan=2)
            tk.Label(pieds, text="Territoire").grid(row=1, column=0)
            tk.Label(pieds, text="Revenu").grid(row=1, column=1)
            ro=2
            for terr in donnees.territ_list:
                n_terr = tk.StringVar()
                n_terr.set(terr)
                tk.Button(pieds, textvariable=n_terr, command=lambda terr=terr:validPieds(terr)).grid(row=ro, column=0)
                revenu = tk.StringVar()
                revenu.set(donnees.territ_revenu[terr])
                tk.Label(pieds, textvariable=revenu).grid(row=ro, column=1)
                ro+=1

            def validPieds(terr):
                gang.territoires.append(terr)
                interface.initUI()
                self.selectTab(gang._id)
                pieds.destroy()

            pieds.mainloop()
        else:
            gang.territoires.append(terr)

# ----FONCTIONS-DU-JEU---------------------------------------------------------------------------------------------------

    def blessure(self, ganger, multi=False):
        if multi:
            nb_bless = D6()
        else:
            nb_bless = 1

        while nb_bless != 0:
            if multi == True:
                while de in range(11,17) or de in range(41-55):
                    de = D6() * 10 + D6()
            else:
                de = D6()*10+D6()

            if de in range(11, 17):
                self.blessMort()

            elif de == 21:
                self.blessMulti()

            elif de == 22:
                self.blessTorse()

            elif de == 23:
                self.blessJambe()

            elif de == 24:
                self.blessBras()

            elif de == 25:
                self.blessTete()

            elif de == 26:
                self.blessBorgne()

            elif de == 31:
                self.blessSourd()

            elif de == 32:
                self.blessChoc()

            elif de == 33:
                self.blessMain()

            elif de in range(34, 37):
                self.blessVieille()

            elif de in range(41, 56):
                self.blessRecup()

            elif de == 56:
                self.blessRancune()

            elif de in range(61, 64):
                self.blessCapture()

            elif de == 64:
                self.blessHorr()

            elif de == 65:
                self.blessImpr()

            elif de == 66:
                self.blessSurvie()

            else:
                pass

        def blessBorgne():
            oeil = choice('Oeil droit', 'Oeil gauche')
            pass

        def blessBras():
            pass

        def blessCapture():
            pass

        def blessChoc():
            pass

        def blessHorr():
            pass

        def blessImpr():
            pass

        def blessJambe():
            pass

        def blessMain():
            pass

        def blessMort():
            pass

        def blessMulti():
            pass

        def blessRancune():
            pass

        def blessRecup():
            pass

        def blessSourd():
            pass

        def blessSurvie():
            pass

        def blessTete():
            pass

        def blessTorse():
            pass

        def blessVieille():
            pass



# ----INTERFACE-----------------------------------------------------------------------------------------------------------

debug = True
if debug:
    print("Mode : Debug")
fichier_svg = True
if debug and fichier_svg:
    print("Mode : Accès aux fichiers")

creation = fichier_svg==False
if debug and creation:
    print("Mode : Génération auto")

debut = time.time()
print("Initialisation")

version = '0.9.0'

interface = App()
interface.title("Necrosoft v.{}".format(version))
interface.geometry('{}x{}'.format(largeur, hauteur))

fin = time.time()
temps = fin-debut
print("Programme lancé en {} secondes".format(temps.__round__(3)))

interface.mainloop()

interface.enregistrer()




