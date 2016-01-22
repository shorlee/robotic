# -------------------------------------- #
# Fachhochschule Bielefeld				 #
# Ingenieurinformatik - Projektmodul	 #
# Prof. Dr. rer. nat. Axel Schneider	 #
# Dipl.-Ing. Manfred Fingberg			 #
# -------------------------------------- #
# Hexapod - Team 2                       #
# -------------------------------------- #
from libraries.leg import Leg
import math
import numpy as np
from time import sleep
from time import time
import copy

__date__ = "2016/01/22"


class Rob:
    legDicts = ([
        # Leg 1
        dict(
                index = 1,
                servo = False,
                speed = 10,
                phys = (0.042, 0.038, 0.049, 0.059, 0.021, 0.004, 0.097),
                servos = ([
                    dict(
                            index = 1,
                            ccw = False,
                            angle = 0,
                            speed = 10,
                            offset = 0
                    ),
                    dict(
                            index = 3,
                            ccw = True,
                            angle = 0,
                            speed = 10,
                            offset = 0
                    ),
                    dict(
                            index = 5,
                            ccw = False,
                            angle = 0,
                            speed = 10,
                            offset = 0
                    )
                ]),
                oldLegPos = [0.0475, -0.0875, -0.130, 1],
                newLegPos = [0.0475, -0.0875, -0.130, 1],
                basePos = [0.0800, -0.1200, -0.130, 1],
                T = np.array([  # Translation um x = +0.0325 und y = -0.0325
                    [1, 0, 0, -0.0325],
                    [0, 1, 0, 0.0325],
                    [0, 0, 1, 0],
                    [0, 0, 0, 1]])
        ),
        # Leg 2
        dict(
                index = 2,
                servo = False,
                speed = 10,
                phys = (0.042, 0.038, 0.049, 0.059, 0.021, 0.004, 0.097),
                servos = ([
                    dict(
                            index = 2,
                            ccw = False,
                            angle = 0,
                            speed = 10,
                            offset = 0
                    ),
                    dict(
                            index = 4,
                            ccw = False,
                            angle = 0,
                            speed = 10,
                            offset = 0
                    ),
                    dict(
                            index = 6,
                            ccw = True,
                            angle = 0,
                            speed = 10,
                            offset = 0
                    )
                ]),
                oldLegPos = [0.0475, 0.0875, -0.130, 1],
                newLegPos = [0.0475, 0.0875, -0.130, 1],
                basePos = [0.0800, 0.1200, -0.130, 1],
                T = np.array([  # Translation um x = +0.0325 und y = +0.0325)
                    [1, 0, 0, -0.0325],
                    [0, 1, 0, -0.0325],
                    [0, 0, 1, 0],
                    [0, 0, 0, 1]])
        ),
        # Leg 3
        dict(
                index = 3,
                servo = False,
                speed = 10,
                phys = (0.032, 0.038, 0.049, 0.059, 0.021, 0.004, 0.097),
                servos = ([
                    dict(
                            index = 8,
                            ccw = False,
                            angle = 0,
                            speed = 10,
                            offset = 0
                    ),
                    dict(
                            index = 10,
                            ccw = True,
                            angle = 0,
                            speed = 10,
                            offset = 0
                    ),
                    dict(
                            index = 12,
                            ccw = False,
                            angle = 0,
                            speed = 10,
                            offset = 0
                    )
                ]),
                oldLegPos = [0.0950, 0.0000, -0.130, 1],
                newLegPos = [0.0950, 0.0000, -0.130, 1],
                basePos = [0.0000, 0.1400, -0.130, 1],
                T = np.array([  # Rotation um z = pi3/2 & Translation um y = +0.0450
                    [0, 1, 0, -0.0450],
                    [-1, 0, 0, 0],
                    [0, 0, 1, 0],
                    [0, 0, 0, 1]])
        ),
        # Leg 4
        dict(
                index = 4,
                servo = False,
                speed = 10,
                phys = (0.042, 0.038, 0.049, 0.059, 0.021, 0.004, 0.097),
                servos = ([
                    dict(
                            index = 14,
                            ccw = False,
                            angle = 0,
                            speed = 10,
                            offset = 0
                    ),
                    dict(
                            index = 16,
                            ccw = True,
                            angle = 0,
                            speed = 10,
                            offset = 0
                    ),
                    dict(
                            index = 18,
                            ccw = False,
                            angle = 0,
                            speed = 10,
                            offset = 0
                    )
                ]),
                oldLegPos = [0.0475, -0.0875, -0.130, 1],
                newLegPos = [0.0475, -0.0875, -0.130, 1],
                basePos = [-0.0800, 0.1200, -0.130, 1],
                T = np.array([  # Rotation um z = +pi & Translation um x = -0.0325 und y = +0.0325
                    [-1, 0, 0, -0.0325],
                    [0, -1, 0, 0.0325],
                    [0, 0, 1, 0],
                    [0, 0, 0, 1]])
        ),
        # Leg 5
        dict(
                index = 5,
                servo = False,
                speed = 10,
                phys = (0.042, 0.038, 0.049, 0.059, 0.021, 0.004, 0.097),
                servos = ([
                    dict(
                            index = 13,
                            ccw = False,
                            angle = 0,
                            speed = 10,
                            offset = 0
                    ),
                    dict(
                            index = 15,
                            ccw = False,
                            angle = 0,
                            speed = 10,
                            offset = 0
                    ),
                    dict(
                            index = 17,
                            ccw = True,
                            angle = 0,
                            speed = 10,
                            offset = 0
                    )
                ]),
                oldLegPos = [0.0475, 0.0875, -0.130, 1],
                newLegPos = [0.0475, 0.0875, -0.130, 1],
                basePos = [-0.0800, -0.1200, -0.130, 1],
                T = np.array([  # Rotation um z = +pi & Translation um x = -0.0325 und y = -0.0325
                    [-1, 0, 0, -0.0325],
                    [0, -1, 0, -0.0325],
                    [0, 0, 1, 0],
                    [0, 0, 0, 1]])
        ),
        # Leg 6
        dict(
                index = 6,
                servo = False,
                speed = 10,
                phys = (0.032, 0.038, 0.049, 0.059, 0.021, 0.004, 0.097),
                servos = ([
                    dict(
                            index = 7,
                            ccw = False,
                            angle = 0,
                            speed = 10,
                            offset = 0
                    ),
                    dict(
                            index = 9,
                            ccw = False,
                            angle = 0,
                            speed = 10,
                            offset = 0
                    ),
                    dict(
                            index = 11,
                            ccw = True,
                            angle = 0,
                            speed = 10,
                            offset = 0
                    )
                ]),
                oldLegPos = [0.0950, 0.000, -0.130, 1],
                newLegPos = [0.0950, 0.000, -0.130, 1],
                basePos = [0.0000, -0.140, -0.130, 1],
                T = np.array([  # Rotation um z = +pi/2 & Translation um y = -0.0450
                    [0, -1, 0, -0.0450],
                    [1, 0, 0, 0],
                    [0, 0, 1, 0],
                    [0, 0, 0, 1]])
        )
    ])

    # Funktionen Asmus
    #"2" in jeder liste wurde durch "1" ersetzt
    # Funktion Dreieckgang
    def gangDreieck(ausgangshoehe, schritthoehe, verschiebungX):
        xHalb = verschiebungX / 2
        listeDreieck = [[0, 0, ausgangshoehe, 1], [-xHalb, 0, ausgangshoehe, 0], [0, 0, schritthoehe, 2],
                        [xHalb, 0, ausgangshoehe, 0]]
        return (listeDreieck)

    # Funktion Rechteckgang
    def gangRechteck(ausgangshoehe, schritthoehe, verschiebungX):
        xHalb = verschiebungX / 2
        listeRechteck = [[0, 0, ausgangshoehe, 1], [-xHalb, 0, ausgangshoehe, 0], [-xHalb, 0, ausgangshoehe, 0],
                         [-xHalb, 0, schritthoehe, 0], [0, 0, schritthoehe, 2], [xHalb, 0, schritthoehe, 0],
                         [xHalb, 0, ausgangshoehe, 0], [xHalb, 0, ausgangshoehe, 0]]
        return (listeRechteck)

    # Funktion Kurve
    def gangKurve(ausgangshoehe, schritthoehe, verschiebungX):
        # Funktion nicht vorhanden
        return ()

    # Funktion zum Bewegen des Koerpers hoch und runter
    def hochUndRunter(ausgangshoehe, schritthoehe, verschiebungX):
        listeHochUndRunter = [[0, 0, ausgangshoehe, 1], [0, 0, schritthoehe, 0], [0, 0, ausgangshoehe, 2],
                              [0, 0, schritthoehe, 0]]
        return (listeHochUndRunter)

    # Liste der Gangartfunktionen
    listeGangartenfunktionen = [gangDreieck, gangRechteck, gangKurve, hochUndRunter]

    # Kurve
    def kurveZvonX(x, standHoehe, zHoehe):
        radius = zHoehe / 2
        zVonX = math.sqrt(math.fabs(radius * radius - x * x)) + standHoehe
        # zVonX = -0.1
        return (zVonX)

    # Funktion zum drehen der gesammten workList
    def drehenFunktion(self):
        listeRotiert = []
        for i in self.workList:
            vektor = np.array(i)
            transformiert = np.dot(self.Tmatrix, vektor)
            listeRotiert.append(transformiert)
        return (listeRotiert)

    # Funktion zum berechnen der Fusspunte fuer jedes Bein
    def setPos(self, positionen, legOffset):
        koordinaten = [round(positionen[0] + legOffset[0], 3), round(positionen[1] + legOffset[1], 3),
                       round(positionen[2] + legOffset[2], 3)]
        return (koordinaten)

    # Koordinaten zur verschiebung
    verschiebungX = 0
    # xHalbe = verschiebungX/2
    hoeheZ = -0.14
    ausgangshoeheZ = -0.16

    dreickeListe = gangDreieck(ausgangshoeheZ, hoeheZ, verschiebungX)
    # initialList = dreickeListe

    # Koordinaten der Ausgangsposition der Fuesse aus Basiskoordinatensystem
    # OHNE VORZEICHEN
    radius = 0.18
    fuss1245X = radius * math.cos(math.pi / 6)  # 0.13 - 0.18
    fuss1245Y = radius * math.sin(math.pi / 6)  # 0.11 - 0.1
    fuss36X = 0
    fuss36Y = radius * math.sin(math.pi / 3)  # 0.16 - 0.2

    # Liste der Ausgangspositionen der Fuesse mit vorzeichen
    initialPosFuesse = [[fuss1245X, -fuss1245Y, 0, 0], [fuss1245X, fuss1245Y, 0, 0], [fuss36X, fuss36Y, 0, 0],
                        [-fuss1245X, fuss1245Y, 0, 0], [-fuss1245X, -fuss1245Y, 0, 0], [fuss36X, -fuss36Y, 0, 0]]

    # Liste fuer korrospondierende Beine:
    # korrospndLeg = korrospondLeg = [[0,2,4],[1,3,5]]

    # Liste auf der gearbeitet wird:
    # workList = initialList
    workList = dreickeListe

    # Indices fuer Positionen in Trajektorie
    # 0 und 2 fuer Dreieck
    index1 = 0
    index2 = 2

    # Maximale Groesse der Indices
    indexRange = 0

    # Auswahl Gangart
    # 0 -> Dreieck
    # 1 -> Rechteck
    # 2 -> Kurve
    wahlGangart = 0

    # Liste der Koordinaten welche dem robot uebergeben werden
    koordList = [[], [], [], [], [], []]

    # ----------- KONSTRUKTOR ---------------------------------------- #
    # ================================================================ #
    # Initialisiert ein Rob-Objekt.									   #
    # ---------------------------------------------------------------- #
    def __init__(self, data):
        # Heartbeat
        self.heartrate = 1.0
        # Daten von Controller
        self.data = data
        # Initialisierung der Dictionaries
        for legDict in self.legDicts:
            legDict["servo"] = True
            self.servoOffset(legDict)
        # Initialisierung der Beine
        self.legObjs = list()
        for i in self.legDicts:
            self.legObjs.append(Leg(i))
        # Koordinaten zur Verschiebung
        self.verschiebungX = 0.00
        self.hoeheZ = -0.14
        self.ausgangshoeheZ = -0.16
        # Rotationswinkel
        self.phi = 0.0
        # Geschwindigkeit
        self.speed = 10
        # Gangart
        self.wahlGangart = 0
        # Beine Startposition anfahren lassen
        for i in range(0, 6):
            self.setLeg(i, [self.initialPosFuesse[i][0], self.initialPosFuesse[i][1], self.initialPosFuesse[i][2], 1],
                        self.speed)

    # -------- LEG-OFFSET -------------------------------------------- #
    # ================================================================ #
    # Berechnung der Rob-Koordinate in eine Leg-Koordinate.			   #
    # ---------------------------------------------------------------- #
    def baseToLeg(self, legDict):
        legDict["oldLegPos"] = legDict["newLegPos"]
        legDict["newLegPos"] = np.dot(legDict["T"], np.transpose(legDict["basePos"]))

    # -------- SERVO-OFFSET ------------------------------------------ #
    # ================================================================ #
    # Berechnung des Winkel-Offsets von Beta- und Gamma-Joint.		   #
    # ---------------------------------------------------------------- #
    def servoOffset(self, legDict):
        q = math.sqrt(legDict["phys"][5] ** 2 + legDict["phys"][6] ** 2)
        r = math.sqrt(legDict["phys"][3] ** 2 + legDict["phys"][4] ** 2)
        s = math.sqrt((legDict["phys"][4] + legDict["phys"][6]) ** 2 + (legDict["phys"][3] + legDict["phys"][5]) ** 2)

        legDict["servos"][0]["offset"] = 0
        legDict["servos"][1]["offset"] = math.atan2(legDict["phys"][4], legDict["phys"][3])
        legDict["servos"][2]["offset"] = math.pi - math.acos(((q ** 2) + (r ** 2) - (s ** 2)) / (2 * q * r))

    # --------- BEWEGUNG --------------------------------------------- #
    # ================================================================ #
    # Funktionen zum Setzen eines Beines und Ausfuehren der Motoren.   #
    # ---------------------------------------------------------------- #
    def action(self):
        self.legObjs[0].doLegMovement()

    def setLeg(self, index, fPos, speed=10):
        self.legObjs[index].legDict["basePos"] = fPos
        self.baseToLeg(self.legObjs[index].legDict)
        self.legObjs[index].legDict["speed"] = speed
        # self.legSpeed()
        self.legObjs[index].setLegMovement()

    # --------- BEWEGUNG --------------------------------------------- #
    # ================================================================ #
    # Berechnet angepasste Beingeschwindigkeiten.	    	    	   #
    # ---------------------------------------------------------------- #
# TODO: thinking about legSpeed
    def legSpeed(self):
        # -- Beinbewegungsdistanzen berechnen
        distances = list()
        distances.append(dict(value=1))
        for i in range(0, 6):
            distances.append(dict(
                    ref=self.legDicts[i],
                    value=np.sqrt((self.legDicts[i]["newLegPos"][0] - self.legDicts[i]["oldLegPos"][0]) ** 2
                                  + (self.legDicts[i]["newLegPos"][1] - self.legDicts[i]["oldLegPos"][1]) ** 2
                                  + (self.legDicts[i]["newLegPos"][2] - self.legDicts[i]["oldLegPos"][2]) ** 2),
                    rate=1
            )
            )
        self.insertionSortServo(distances)
        for index in range(2, 7):
            if distances[index - 1]["value"] == 0:
                distances[index - 1]["value"] = 1
            distances[index]["rate"] = distances[index]["value"] / distances[index - 1]["value"]
            distances[index]["ref"]["speed"] = int(distances[index]["rate"] * distances[index]["ref"]["speed"])

    def insertionSortServo(self, sortList):
        for i in range(1, 7):
            temp = sortList[i]["value"]
            position = i
            while position > 0 and sortList[position - 1]["value"] < temp:
                sortList[position]["value"] = sortList[position - 1]["value"]
                position -= 1
            sortList[position]["value"] = temp

    # Funktionen zum errechnen der Werte aus Data von Controller
    # Aus strings Werte von 0 bis 3 fuer Gangart
    def gangArt(self):
        self.wahlGangart = 0
        dataGang = self.data["ctrl"]["mode"]
        if self.data["ctrl"]["mode"]:
            if dataGang == "triangle":
                self.wahlGangart = 0
            if dataGang == "square":
                self.wahlGangart = 1
            if dataGang == "circle":
                self.wahlGangart = 0
            if dataGang == "cross":
                self.wahlGangart = 3

    # Aus Werten 0 bis 1 Geschwindigkeit errechnen:
    def geschwindigkeit(self):
        self.speed = int(self.data["axis"]["speed"] * 50)
        if self.speed < 10:
            self.speed = 10

    # Schrittweite errechnen
    # Werte zwischen 0 und 1
    def schrittweite(self):
        maximalWert = 0.1
        # y und x in dict vertauschen
        print("Data y ", self.data["axis"]["y"])
        verschiebungWert = self.data["axis"]["y"]
        if verschiebungWert < 0.1:
            verschiebungWert = 0.00
        self.verschiebungX = round(maximalWert * verschiebungWert, 2)

    # Drehung0
    # Winkel zwischen 0 und 2pi
    def drehung(self):
        mindestDrehung = 0.3
        winkel = self.data["axis"]["radiant"]
        if winkel > mindestDrehung:
            self.phi = winkel
        else:
            self.phi = 0.0

    # Standhoehe veraendern
    # hoch/runter = bool
    def standHoehe(self, hoch, runter):
        verschiebung = 0.01
        if hoch:
            self.ausgangshoeheZ += verschiebung
        if runter:
            self.ausgangshoeheZ -= verschiebung

    # Schritthoehe veraendern
    def schrittHoehe(self):
        if self.data["ctrl"]["height"]:
            self.hoeheZ = self.verschiebungSchritthoehe
            self.ausgangshoeheZ = self.verschiebungKoerper
        else:
            self.hoeheZ = -0.14
            self.ausgangshoeheZ = -0.16

    # Dicts abgleichen
    def dictAbgleich(self):
        self.geschwindigkeit()
        self.schrittweite()
        self.drehung()
        self.gangArt()
        self.schrittHoehe()

    # ----------- Loop ----------------------------------------------- #
    # ================================================================ #
    # Endlosschleife des laufenden Programms.			        	   #
    # ---------------------------------------------------------------- #
    def loop(self, run_event):

        # Variablen fuer spaetere:
        # Schrittweite
        self.verschiebungX = self.schrittweite()
        # Schritthoehe
        self.hoeheZ = -0.14
        # Koerperhoehe
        self.ausgangshoeheZ = -0.16
        # Verschiebung des Koerpers bei height-Taste
        self.verschiebungKoerper = -0.16
        # Verschiebung der Schritte bei height-Taste
        self.verschiebungSchritthoehe = -0.08
        # Drehung
        self.phi = self.drehung()
        # Geschwindigkeit
        self.speed = self.geschwindigkeit()
        # Gangart
        self.wahlGangart = self.gangArt()

        while run_event.is_set():
            delta1 = time()
            # START DES TAKTES
            self.geschwindigkeit()

            # Verschiedene Gangarten
            if self.workList[self.index1][3] == 1 and self.workList[self.index2][3] == 2:
                self.dictAbgleich()
                self.workList = copy.deepcopy(
                        self.listeGangartenfunktionen[self.wahlGangart](self.ausgangshoeheZ, self.hoeheZ,
                                                                        self.verschiebungX))
                self.index1 = 0
                self.index2 = int(len(self.workList) / 2)
                self.indexRange = len(self.workList)
                # Drehung
                if self.phi != 0.0:
                    self.Tmatrix = np.array([
                        [math.cos(self.phi), -math.sin(self.phi), 0, 0],
                        [math.sin(self.phi), math.cos(self.phi), 0, 0],
                        [0, 0, 1, 0],
                        [0, 0, 0, 1]
                    ])
                    self.workList = copy.deepcopy(self.drehenFunktion())

            # Erstes Trippel der Beine
            self.koordList[0] = self.setPos(self.workList[self.index1], self.initialPosFuesse[0])
            self.koordList[2] = self.setPos(self.workList[self.index1], self.initialPosFuesse[2])
            self.koordList[4] = self.setPos(self.workList[self.index1], self.initialPosFuesse[4])
            # Zweites Trippel der Beine
            self.koordList[1] = self.setPos(self.workList[self.index2], self.initialPosFuesse[1])
            self.koordList[3] = self.setPos(self.workList[self.index2], self.initialPosFuesse[3])
            self.koordList[5] = self.setPos(self.workList[self.index2], self.initialPosFuesse[5])

            print("koordList", self.koordList[0])
            print("koordList", self.koordList[1])
            print("koordList", self.koordList[2])
            print("koordList", self.koordList[3])
            print("koordList", self.koordList[4])
            print("koordList", self.koordList[5])

            # Uebergabe der Fusspositionen an den robot
            for i in range(0, 6):
                self.setLeg(i, [self.koordList[i][0], self.koordList[i][1], self.koordList[i][2], 1], self.speed)

            # Alle Servos starten
            self.action()

            # Indices erhoehen
            self.index1 += 1
            self.index2 += 1
            # Ueberpruefen ob Indices zu hoch und gegebenenfalls erniedriegen
            # ==4 fuer Dreieck
            # ==8 fuer Rechteck
            # ==12 fuer Kurve
            if self.index1 == self.indexRange:
                self.index1 = 0
            if self.index2 == self.indexRange:
                self.index2 = 0

            # ENDE DES TAKTES
            print()
            print("------------ BEAT ----------")
            print()
            delta2 = time()
            sleep(self.heartrate - (delta2 - delta1))


# ----------- Main ----------------------------------------------- #
# ================================================================ #
# Startet das Programm (Schnittstelle)							   #
# ---------------------------------------------------------------- #
def worker(data, logger, config, run_event):
    nemo = Rob(data)
    nemo.loop(run_event)
