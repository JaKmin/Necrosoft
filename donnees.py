__author__ = 'Jamin'
# -*-coding:utf-8 -*

"""GANGS"""
noms_maison=("Cawdor","Escher","Delaque","Goliath","Orlock","Van Saar")



"""GANGER"""
"""GRADES : Kid -> 0 // Ganger -> 1 // Balèze -> 2 // Chef de gang -> 3"""
nom_grades=("Kid","Ganger","Balèze","Chef de Gang")
noms_stats=("M","CC","CT","F","E","PV","I","A","Cd")
stats_type=([4,2,2,3,3,1,3,1,6],[4,3,3,3,3,1,3,1,7],[4,3,3,3,3,1,3,1,7],[4,4,4,3,3,1,4,1,8])
cout_recrut=(25,50,60,120)
exp_recrut=((0,0),(1,20),(1,60),(1,60))
stats_max=(4,6,6,4,4,3,6,3,9)

couleurs_stats = {0:{1:"red", 2:"red", 3:"orange", 4:"green"},
                  1:{1:"red", 2:"red", 3:"orange", 4:"orange", 5:"green", 6:"green"},
                  2:{1:"red", 2:"red", 3:"orange", 4:"orange", 5:"green", 6:"green"},
                  3:{1:"red", 2:"orange", 3:"green", 4:"green"},
                  4:{1:"red", 2:"orange", 3:"green", 4:"green"},
                  5:{1:"orange", 2:"green", 3:"green"},
                  6:{1:"red", 2:"orange", 3:"orange", 4:"green", 5:"green", 6:"green"},
                  7:{1:"orange", 2:"green", 3:"green"},
                  8:{3:"red", 4:"red", 5:"red", 6:"orange", 7:"orange", 8:"green", 9:"green"}}

rangs = ((5, 'Bleu'),
         (10, 'Kid'),
         (15, 'Kid'),
         (20, 'Super Kid'),
         (30, 'Ganger Novice'),
         (40, 'Ganger'),
         (50, 'Ganger'),
         (60, 'Ganger'),
         (80, 'Champion'),
         (100, 'Champion'),
         (120, 'Champion'),
         (140, 'Champion'),
         (160, 'Champion'),
         (180, 'Champion'),
         (200, 'Champion'),
         (240, 'Héros'),
         (280, 'Héros'),
         (320, 'Héros'),
         (360, 'Héros'),
         (400, 'Héros'),
         (401, 'Légende Vivante'))

"""COMPETENCES"""

comp_noms = ["Agilité","Combat","Discrétion","Muscle","Férocité","Techno","Tir"]

competences = {"Agilité":["Agilité féline","Esquive","Saut en arrière","Bond","Réflexes foudroyants","Sprint"],
               "Combat":["Maître combatant","Désarmer","Feinte","Parade","Contre-attaque","Saut de côté"],
               "Discrétion":["Embuscade","Plongeon","Roi de l'évasion","Zigzag","Infiltration","Dissimulation"],
               "Muscle":["Bulldozer","Gros bras","Coup fatal","Coup d'boule","Projection","Dur à cuire"],
               "Férocité":["Charge berserk","Impétuosité","Volonté de fer","Réputation de tueur","Nerfs d'acier","Vrai brave"],
               "Techno":["Armurier","Débrouillard","Inventeur","Guérisseur","Spécialiste","Expert en armement"],
               "Tir":["Tir d'expert","Tir éclair","Pistolero","Tir au jugé","Œil de lynx","Tir rapide"]}

comp_dispos = {"Cawdor":(([1,4,],[0,2,3,5,6],),
                         ([0,1,4,],[2,3,5,6],),
                         ([3,4,5,6],[0,1,2,],),
                         ([0,1,3,4,5,6],[2,])),
               "Escher":(([0,1,],[2,3,4,5,6],),
                         ([0,1,2,],[3,4,5,6],),
                         ([0,3,5,6],[1,2,4,],),
                         ([0,1,2,4,5,6],[3,])),
               "Delaque":(([2,6],[0,1,3,4,5,],),
                          ([0,2,6],[1,3,4,5,],),
                          ([2,3,5,6],[0,1,4,],),
                          ([0,1,2,4,5,6],[3,])),
               "Goliath":(([3,4,],[0,1,2,5,6],),
                           ([1,3,4,],[0,2,5,6],),
                           ([1,3,5,6],[0,2,4,],),
                           ([1,2,3,4,5,6],[0,])),
               "Orlock":(([4,6],[0,1,2,3,5,],),
                          ([1,4,6],[0,2,3,5,],),
                          ([1,3,5,6],[0,2,4,],),
                          ([0,1,2,4,5,6],[3,])),
               "Van Saar":(([5,6],[0,1,2,3,4,],),
                           ([1,5,6],[0,2,3,4,],),
                           ([1,3,5,6],[0,2,4,],),
                           ([0,1,2,4,5,6],[3,]))}

levelup = {2:"any_comp",
           3:"disp_comp (maison)",
           4:"disp_comp	(maison)",
           5:"carac_FA",
           6:"carac_CCCT",
           7:"carac_ICd",
           8:"carac_CCCT",
           9:"carac_PVE",
           10:"disp_comp (maison)",
           11:"disp_comp (maison)",
           12:"any_comp"}

"""ARMES"""

armes_debut = {"Goliath":{"Armes de corps à corps":["Poignard","Massue","Matraque","Hache"],
                          "Pistolets":["Pistolet Mitrailleur","Pistolet Laser","Pistolet Automatique"],
                          "Armes de Base":["Fusil d’Assaut","Fusil Laser","Fusil"],
                          "Armes Spéciales":["Lance-flammes","Lance-grenades"],
                          "Armes Lourdes":["Autocanon","Mitrailleuse","Bolter Lourd"],
                          "Réservé au Chef":["Épée Tronçonneuse","Fuseur","Pistolet Bolter"]},
               "Orlock":{"Armes de corps à corps":["Poignard","Chaîne","Fléau"],
                         "Pistolets":["Pistolet Mitrailleur","Pistolet Laser","Pistolet Automatique"],
                         "Armes de Base":["Fusil d’Assaut","Fusil Laser","Fusil"],
                         "Armes Spéciales":["Lance-flammes","Lance-grenades"],
                         "Armes Lourdes":["Lance-missiles","Mitrailleuse","Bolter Lourd"],
                         "Réservé au Chef":["Épée Tronçonneuse","Fuseur","Pistolet Bolter"]},
               "Van Saar":{"Armes de corps à corps":["Poignard","Massue","Matraque","Hache"],
                           "Pistolets":["Pistolet Mitrailleur","Pistolet Bolter","Pistolet Laser","Pistolet Automatique"],
                           "Armes de Base":["Fusil d’Assaut","Fusil Laser","Fusil"],
                           "Armes Spéciales":["Lance-flammes","Lance-plasma"],
                           "Armes Lourdes":["Mitrailleuse","Lance-plasma lourd"],
                           "Réservé au Chef":["Épée Tronçonneuse","Fuseur","Pistolet à Plasma"]},
               "Delaque":{"Armes de corps à corps":["Poignard","Massue", "Matraque","Hache"],
                          "Pistolets":["Pistolet Mitrailleur","Pistolet Laser","Pistolet Automatique"],
                          "Armes de Base":["Fusil d’Assaut","Fusil Laser","Fusil"],
                          "Armes Spéciales":["Lance-flammes"],
                          "Armes Lourdes":["Mitrailleuse","Canon Laser"],
                          "Réservé au Chef":["Pistolet Bolter","Bolter","Épée Tronçonneuse","Fuseur"]},
               "Cawdor":{"Armes de corps à corps":["Poignard"],
                         "Pistolets":["Pistolet Mitrailleur","Pistolet Laser","Pistolet Automatique"],
                         "Armes de Base":["Fusil d’Assaut","Bolter","Fusil Laser","Fusil"],
                         "Armes Spéciales":["Lance-flammes","Lance-grenades"],
                         "Armes Lourdes":["Mitrailleuse","Bolter Lourd"],
                         "Réservé au Chef":["Épée Tronçonneuse","Pistolet Bolter"]},
               "Escher":{"Armes de corps à corps":["Poignard","Épée","Massue","Matraque","Hache"],
                         "Pistolets":["Pistolet Mitrailleur","Pistolet Laser","Pistolet Automatique"],
                         "Armes de Base":["Fusil d’Assaut","Fusil Laser","Fusil"],
                         "Armes Spéciales":["Lance-flammes"],
                         "Armes Lourdes":["Mitrailleuse","Lance-plasma lourd"],
                         "Réservé au Chef":["Pistolet Bolter","Bolter","Épée Tronçonneuse","Pistolet à Plasma"]}}

armes_grade = {0:["Armes de corps à corps","Pistolets"],
               1:["Armes de corps à corps","Pistolets","Armes de Base"],
               2:["Armes de corps à corps","Pistolets","Armes de Base","Armes Spéciales","Armes Lourdes"],
               3:["Armes de corps à corps","Pistolets","Armes de Base","Armes Spéciales","Réservé au Chef"]}

arsenal={"Épée":(10, 0, "Commune","Armes de corps à corps"),
         "Épée Tronçonneuse":(25, 0, "Commune","Armes de corps à corps"),
         "Hache":(10, 0, "Commune","Armes de corps à corps"),
         "Masse":(10, 0, "Commune","Armes de corps à corps"),
         "Massue":(10, 0, "Commune","Armes de corps à corps"),
         "Matraque":(10, 0, "Commune","Armes de corps à corps"),
         "Gourdin":(10, 0, "Commune","Armes de corps à corps"),
         "Chaîne":(10, 0, "Commune","Armes de corps à corps"),
         "Fléau": (10, 0, "Commune", "Armes de corps à corps"),
         "Poignard":(5, 0, "Commune","Armes de corps à corps"),
         "Arme à deux mains":(15, 0, "Commune","Armes de corps à corps"),
         "Hache énergétique":(35, 3, "Rare","Armes de corps à corps"),
         "Gantelet énergétique":(85, 3, "Rare","Armes de corps à corps"),
         "Matraque énergétique":(35, 3, "Rare","Armes de corps à corps"),
         "Epée énergétique":(40, 3, "Rare","Armes de corps à corps"),
         "Pistolet Mitrailleur":(15, 0, "Commune","Pistolets"),
         "Pistolet Bolter":(20, 0, "Commune","Pistolets"),
         "Lance-flammes léger":(20, 0, "Commune","Pistolets"),
         "Pistolet Laser":(15, 0, "Commune","Pistolets"),
         "Pistolet à aiguilles":(100, 4, "Rare","Pistolets"),
         "Pistolet à Plasma":(25, 0, "Commune","Pistolets"),
         "Pistolet Automatique":(10, 0, "Commune","Pistolets"),
         "Lance-toile":(120, 4, "Rare","Pistolets"),
         "Fusil d’Assaut":(20, 0, "Commune","Armes de base"),
         "Bolter":(35, 0, "Commune","Armes de base"),
         "Fusil Laser":(25, 0, "Commune","Armes de base"),
         "Fusil":(20, 0, "Commune","Armes de base"),
         "Lance-flammes":(40, 0, "Commune","Armes spéciales"),
         "Lance-grenades":(130, 0, "Commune","Armes spéciales"),
         "Fuseur":(95, 0, "Commune","Armes spéciales"),
         "Fusil à aiguilles":(230, 4, "Rare","Armes spéciales"),
         "Lance-plasma":(70, 0, "Commune","Armes spéciales"),
         "Autocanon":(300, 0, "Commune","Armes lourdes"),
         "Mitrailleuse":(120, 0, "Commune","Armes lourdes"),
         "Bolter Lourd":(180, 0, "Commune","Armes lourdes"),
         "Lance-plasma lourd":(285, 0, "Commune","Armes lourdes"),
         "Canon Laser":(400, 0, "Commune","Armes lourdes"),
         "Lance-missiles":(185, 0, "Commune","Armes lourdes"),
         "Missile à fragmentation":(35, 0, "Commune","Missiles"),
         "Missile Antichar":(115, 0, "Commune","Missiles"),
         "Grenade asphyxiante":(15, 2, "Rare","Grenades"),
         "Grenade à fragmentation":(30, 0, "Commune","Grenades"),
         "Grenade hallucinogène":(40, 4, "Rare","Grenades"),
         "Grenade antichar":(50, 0, "Commune","Grenades"),
         "Grenade à fusion":(40, 3, "Rare","Grenades"),
         "Grenade photonique":(20, 2, "Rare","Grenades"),
         "Grenade à plasma":(30, 3, "Rare","Grenades"),
         "Grenade Cauchemar":(20, 2, "Rare","Grenades"),
         "Grenade fumigène":(10, 3, "Rare","Grenades")}

"""TERRITOIRES"""

territ_list = ["Fosse chimique","Champ de ruines","Scories","Gisement Minéral","Colonie","Mine","Tunnels",
               "Conduits de ventilation","Ferme","Pompe à eau","Taverne","Relations Commerciales","Toubib",
               "Atelier","Tripot","Champignonnère","Archéotechnologie"]

territ_revenu={"Fosse chimique":"2D6*",
               "Champ de ruines":"10",
               "Scories":"15",
               "Gisement Minéral":"1D6 x 10",
               "Colonie":"30*",
               "Mine":"1D6 x 10*",
               "Tunnels":"10*",
               "Conduits de ventilation":"10*",
               "Ferme":"1D6 x 10",
               "Pompe à eau":"1D6 x 10",
               "Taverne":"1D6 x 10",
               "Relations Commerciales":"1D6 x 10*",
               "Toubib":"1D6 x 10*",
               "Atelier":"1D6 x 10*",
               "Tripot":"2D6 x 10*",
               "Champignonnère":"2D6 x 10*",
               "Archéotechnologie":"2D6 x 10*"}

argent_cass = {range(1,50):5,
range(50,100):10,
range(100,150):15,
range(150,200):20,
range(200,250):25,
range(250,500):50,
range(500,750):100,
range(750,1000):150,
range(1000,1500):200,
range(1500,10000):250}

bonus_cass = {range(1,50):[1,0],
range(50,100):[2,1],
range(100,150):[3,2],
range(150,200):[4,3],
range(200,250):[5,4],
range(250,500):[6,5],
range(500,750):[7,6],
range(750,1000):[8,7],
range(1000,1500):[9,8],
range(1500,10000):[10,9]}