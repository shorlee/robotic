# ----------------------------------------#
# Fachhochschule Bielefeld				  #
# Ingenieurinformatik - Projektmodul	  #
# Prof. Dr. rer. nat. Axel Schneider	  #
# Dipl.-Ing. Manfred Fingberg			  #
# ----------------------------------------#
# Hexapod - Team 2 - Arbeitsgruppe LEG	  #
# Marcel Bernauer						  #
# Jakob Sasmuzki						  #
# Fabian Wiescholek						  #
# ----------------------------------------#
import math
import numpy as np

try:
    from libraries.jointdrive import JointDrive
except Exception as e:
    print(e)
    # print("**********************************************")
    # print("* JOINTDRIVE KONNTE NICHT EINGEBUNDEN WERDEN *")
    # print("* >> COM Schnittstelle verfuegbar?           *")
    # print("**********************************************")

__date__ = "2016/01/22"


# -------------------------------------------------------------------- #
# Leg-Objekt - Bedienungsanleitung									   #
# -------------------------------------------------------------------- #
# 1 -- Konstruktor													   #
# 	Uebergabe der Referenz des Dictionarys von einem Bein.			   #
# 2 -- Bewegung setzen (setLegMovement)								   #
# 	Fusskoordinate (Legxyz) in das Dictionary schreiben.			   #
# 	Funktion aufrufen.												   #
# 3 -- Bewegung ausfuehren (doLegMovement)							   #
# 	Funktion aufrufen.												   #
# -------------------------------------------------------------------- #

class Leg:
    # -------- KONSTRUKTOR ------------------------------------------- #
    # ================================================================ #
    # Initialisiert ein massgeschneidertes Leg-Objekt.				   #
    # ---------------------------------------------------------------- #
    def __init__(self, leg):
        # -- Referenz zum Dictionary sichern ...
        self.legDict = leg
        # -- Index festlegen
        self.index = self.legDict["index"]
        # -- Physikalische Groessen holen
        self.a = [self.legDict["phys"][0], self.legDict["phys"][1], self.legDict["phys"][2], self.legDict["phys"][3],
                  self.legDict["phys"][4], self.legDict["phys"][5], self.legDict["phys"][6]]
        # -- Abstaende zwischen den Genlenksystemen ermitteln
        self.lc = self.a[2]
        self.lcSquare = math.pow(self.lc, 2)
        self.lf = math.sqrt(math.pow(self.a[3], 2) + math.pow(self.a[4], 2))
        self.lfSquare = math.pow(self.lf, 2)
        self.lt = math.sqrt(math.pow(self.a[5], 2) + math.pow(self.a[6], 2))
        self.ltSquare = math.pow(self.lt, 2)
        # -- Fußpunkt holen
        self.fPos = self.legDict["newLegPos"]
        # -- Berechnung durchfuehren
        self.angleSpeed()
        # -- Servomotoren initialisieren (opt)
        if self.legDict["servo"]:
            self.servoInit()

    # -------- BEWEGUNG ---------------------------------------------- #
    # ================================================================ #
    # Startet die Ausfuehrung aller Anweisungen (broadcast).		   #
    # ---------------------------------------------------------------- #
    def doLegMovement(self):
        self.servo1.startAllServos()

    # ================================================================ #
    # Uebergibt den Servos berechnete Winkel und Geschwindigkeiten.	   #
    # ---------------------------------------------------------------- #
    def setLegMovement(self):
        # -- Winkelberechnung
        self.angleSpeed()  # HERE IS THE MAGIC

        alpha, alphaSpeed = round(self.legDict["servos"][0]["angle"], 3), self.legDict["speed"]
        beta, betaSpeed = round(self.legDict["servos"][1]["angle"], 3), self.legDict["speed"]
        gamma, gammaSpeed = round(self.legDict["servos"][2]["angle"], 3), self.legDict["speed"]

        try:
            self.servo1.setDesiredAngleSpeed(angle = alpha, speed = alphaSpeed, trigger = True)
            self.servo2.setDesiredAngleSpeed(angle = beta, speed = betaSpeed, trigger = True)
            self.servo3.setDesiredAngleSpeed(angle = gamma, speed = gammaSpeed, trigger = True)
        except Exception as e:
            print(e)
            print(">>> Servo konnte nicht angesprochen werden! (leg)")

    # -------- INVERSE KINEMATIK ------------------------------------- #
    # ================================================================ #
    # Laesst die Winkel berechnen und sichert sie in self.angles.	   #
    # ---------------------------------------------------------------- #
    def invKin(self):
        # Alpha-Joint Offset
        self.afPos = self.legOffset(self.legDict["newLegPos"])
        # Winkelberechnung
        self.angles = self.invKinAlphaJoint(self.afPos)
        # Dokumentation
        self.legDict["servos"][0]["angle"] = self.angles[0]
        self.legDict["servos"][1]["angle"] = self.angles[1]
        self.legDict["servos"][2]["angle"] = self.angles[2]

    # ================================================================ #
    # Berechnet die Winkel ohne Offset.								   #
    # ---------------------------------------------------------------- #
    def invKinAlphaJoint(self, pos):
        alpha = math.atan2(pos[1], pos[0])
        footPos = np.array(pos)
        A1 = np.array([
            [math.cos(alpha), 0, math.sin(alpha), self.lc * math.cos(alpha)],
            [math.sin(alpha), 0, -math.cos(alpha), self.lc * math.sin(alpha)],
            [0, 1, 0, 0],
            [0, 0, 0, 1]])

        betaPos = np.dot(A1, np.transpose([0, 0, 0, 1]))
        lct = np.linalg.norm(footPos[0:3] - betaPos[0:3])
        lctSquare = math.pow(lct, 2)

        gamma = math.acos((self.ltSquare + self.lfSquare - lctSquare) / (2 * self.lt * self.lf)) - math.pi

        h1 = math.acos((self.lfSquare + lctSquare - self.ltSquare) / (2 * self.lf * lct))
        h2 = math.acos((lctSquare + self.lcSquare - math.pow(np.linalg.norm(footPos[0:3]), 2)) / (2 * self.lc * lct))
        if footPos[2] < 0:
            beta = (h1 + h2) - math.pi
        else:
            beta = (math.pi - h2) + h1
        return (alpha, beta, gamma)

    # -------- VORWAERTSKINEMATIK ------------------------------------ #
    # ================================================================ #
    # Berechnet die Position des Fußpunktes aus	Sicht des AJ.		   #
    # (A1 x A2 x A3)												   #
    # ---------------------------------------------------------------- #
    def forKinAlphaJointEnd(self, alpha, beta, gamma):
        pos = [0, 0, 0, 1]
        pos[0] = math.cos(alpha) * (self.lt * math.cos(beta + gamma) + self.lf * math.cos(beta) + self.lc)
        pos[1] = math.sin(alpha) * (self.lt * math.cos(beta + gamma) + self.lf * math.cos(beta) + self.lc)
        pos[2] = self.lt * math.sin(beta + gamma) + self.lf * math.sin(beta)
        return pos

    # ================================================================ #
    # Berechnet die Position des Gamma-Joint aus Sicht des AJ.		   #
    # (A1 x A2)														   #
    # ---------------------------------------------------------------- #
    def forKinAlphaJointGamma(self, alpha, beta, gamma):
        pos = [0, 0, 0, 1]
        pos[0] = self.lf * math.cos(beta) * math.cos(alpha) + self.lc * math.cos(alpha)
        pos[1] = self.lf * math.cos(beta) * math.sin(alpha) + self.lc * math.sin(alpha)
        pos[2] = self.lf * math.sin(beta)
        return pos

    # ================================================================ #
    # Berechnet die Position des Beta-Joint aus Sicht des AJ.		   #
    # (A1)															   #
    # ---------------------------------------------------------------- #
    def forKinAlphaJointBeta(self, alpha, beta, gamma):
        pos = [0, 0, 0, 1]
        pos[0] = self.lc * math.cos(alpha)
        pos[1] = self.lc * math.sin(alpha)
        return pos

    # -------- BERECHNUNGEN ------------------------------------------ #
    # ================================================================ #
    # Gibt den Offset zwischen Bein- und AJ-Koordinatensystem an.	   #
    # ---------------------------------------------------------------- #
    def legOffset(self, pos):
        O1 = np.array([
            [1, 0, 0, -self.a[0]],
            [0, 1, 0, 0],
            [0, 0, 1, self.a[1]],
            [0, 0, 0, 1]])
        return np.dot(O1, np.transpose(pos))

    # ================================================================ #
    # Berechnet synchronisierte Winkelgeschwindigkeiten.			   #
    # ---------------------------------------------------------------- #
    def angleSpeed(self):
        # Alte Winkel speichern
        oldServoAngles = list()
        for i in range(0, 3):
            oldServoAngles.append(self.legDict["servos"][i]["angle"])
        # Berechnung der inversen Kinematik
        self.invKin()
        # Winkeldistanzen berechnen
        distances = list()
        distances.append(dict(value = 1))
        for i in range(0, 3):
            distances.append(dict(
                    ref = self.legDict["servos"][i],
                    value = np.abs(oldServoAngles[i] - self.legDict["servos"][i]["angle"]),
                    rate = 1
            )
            )
        # Winkeldistanzen sortieren
        self.insertionSortLeg(distances)
        # Geschwindigkeitsrate berechnen und schreiben
        for index in range(2, 4):
            if distances[index - 1]["value"] == 0:
                distances[index - 1]["value"] = 1
            distances[index]["rate"] = distances[index]["value"] / distances[index - 1]["value"]
            distances[index]["ref"]["speed"] = int(distances[index]["rate"] * self.legDict["speed"])

    def insertionSortLeg(self, sortList):
        for i in range(1, 4):
            temp = sortList[i]["value"]
            position = i
            while position > 0 and sortList[position - 1]["value"] < temp:
                sortList[position]["value"] = sortList[position - 1]["value"]
                position -= 1
            sortList[position]["value"] = temp

    # -------- SERVO-INITIALISIERUNG --------------------------------- #
    # ================================================================ #
    # Erzeugt ein Servo-Objekt.										   #
    # 1 | self                                                         #
    # 2 | id                                                           #
    # 3 | ccw = False                                                  #
    # 4 | aOffset = 0.0                                                #
    # 5 | aMax = math.pi * 2                                           #
    # 6 | aMin = -math.pi * 2                                          #
    # ---------------------------------------------------------------- #
    def servoInit(self):
        self.servo1 = JointDrive(id = self.legDict["servos"][0]["index"], ccw = self.legDict["servos"][0]["ccw"],
                                 aOffset = self.legDict["servos"][0]["offset"])
        self.servo2 = JointDrive(id = self.legDict["servos"][1]["index"], ccw = self.legDict["servos"][1]["ccw"],
                                 aOffset = self.legDict["servos"][1]["offset"])
        self.servo3 = JointDrive(id = self.legDict["servos"][2]["index"], ccw = self.legDict["servos"][2]["ccw"],
                                 aOffset = self.legDict["servos"][2]["offset"])
