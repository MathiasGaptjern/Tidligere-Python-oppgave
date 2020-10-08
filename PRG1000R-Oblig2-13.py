# Trenger for "fjerne og endre" funksjonene
import os

gyldigMenyvalg = [1, 2, 3, 4, 5]
harValgt = False
studentFil = "Student13.txt"
emneFil = "Emne13.txt"
resultatFil = "Eksamensresultat13.txt"
studenter = []
studentInfo = []
finnes = False
brukerValg = input("Meny\n1. Registrering\n2. Sletting\n3. Skriv ut karakterliste for student\n4. Skriv ut sensurliste for emne\n5. Avslutt\n\n")
harValgt = False
forsteGang = True
slett = False

regStudent = False
regEmne = False
regResultat = False

finnStudent = "finnStudent"
finnEmne = "finnEmne"
finnResultat = "finnResultat"

# Registrer student
studNummer = 0
studFornavn = ""
studEtternavn = ""
studStudium = ""

# Registrer emne
emneKode = 0
emneNavn = ""

# Registrer eksamensresultat
regEksamensresultatMeny = ["\n1. Registrer emnekode", "\n2. Registrer studentnummer", "\n3. Registrer karakter"]
eksEmneKode = 0
eksStudNummer = 0
eksKarakter = ""


def valgMeny():
    global brukerValg
    global harValgt
    global regStudent
    global regEmne
    global regResultat
    global finnStudent
    global finnEmne
    global finnResultat
    global slett

    if (brukerValg == 1):
        harValgt = False
        gyldigMenyvalg = [1, 2, 3]
        
        while not (harValgt):
            registreringsValg = int(input("\n1. Registrer student\n2. Registrer emne\n3. Registrer resultat\n\n"))
            brukerValg = int(registreringsValg)
            for i in gyldigMenyvalg:
                if (i == brukerValg):
                    harValgt = True
                    
        if (brukerValg == 1): #Registrer student
            studNummer = int(input("\n1. Registrer studentnummer\n"))
            studFornavn = input("\n2. Registrer fornavn\n")
            studEtternavn = input("\n3. Registrer etternavn\n")
            studStudium = input("\n4. Registrer studium\n")
            studentInfo = [studNummer, studFornavn, studEtternavn, studStudium]
            regEmne = False
            regResultat = False
            regStudent = True
            objektInfo = [finnStudent, studNummer]
            if (not finnesFraFor(objektInfo)):
                registrer(studentInfo)
                skrivMeny()
            else:
                print("\n\nStudenten finnes fra før. Kunne derfor ikke registrere data.")
                skrivMeny()
        elif(brukerValg == 2): #Registrer emne
            emneKode = int(input("\n1. Registrer emnekode\n"))
            emneNavn = input("\n2. Registrer emnenavn\n")
            emneInfo = [emneKode, emneNavn]
            regResultat = False
            regStudent = False
            regEmne = True
            objektInfo = [finnEmne, emneKode]
            if (not finnesFraFor(objektInfo)):
                registrer(emneInfo)
                skrivMeny()
            else:
                print("\n\nEmne finnes fra før. Kunne derfor ikke registrere data.")
                skrivMeny()
        elif(brukerValg == 3): #Registrer resultat
            emneKode = int(input("\n1. Registrer emnekode\n"))
            studentNummer = int(input("\n2. Registrer studentnummer\n"))
            karakter = input("\n3. Registrer karakter\n")
            resultatInfo = [emneKode, studentNummer, karakter]
            regEmne = False
            regStudent = False
            regResultat = True
            slett = False
            objektInfo = [finnResultat, emneKode, studentNummer]
            if (not finnesFraFor(objektInfo)):
                registrer(resultatInfo)
                skrivMeny()
            else:
                print("\n\nResultatet finnes fra før. Kunne derfor ikke registrere data.")   
                skrivMeny()
    elif (brukerValg == 2): #Slett
        studentNummer = input("\n1. Skriv inn studentnummer til studenten du vil slette\n")
        objektInfo = [finnResultat, studentNummer]
        slett = True
        if (not finnesFraFor(objektInfo)):
            slettStudent(studentNummer)
            slett = False
            skrivMeny()
        else:
            slett = False
            print("Studenten har eksamensresultater tilknyttet seg, og kan derfor ikke slettes")   
            skrivMeny()
    elif (brukerValg == 3):
        studentNummer = input("\n1. Skriv inn studentnummer til studenten du vil se på karakterlisten for\n")
        skrivUtKarakterliste(studentNummer)
        skrivMeny()
    elif (brukerValg == 4):
        emneKode = input("\n1. Skriv inn emnekode til studiet du vil se på sensurlisten for\n")
        skrivUtSensurliste(emneKode)
        skrivMeny()
    elif (brukerValg == 5):
        quit()

def skrivMeny():
    global harValgt
    global forsteGang
    global gyldigMenyvalg

    gyldigMenyvalg = [1, 2, 3, 4, 5]
    harValgt = False

    while not (harValgt):
        objektInfo = []
        global brukerValg
        if (not forsteGang):
            brukerValg = input("\nMeny\n1. Registrering\n2. Sletting\n3. Skriv ut karakterliste for student\n4. Skriv ut sensurliste for emne\n5. Avslutt\n\n")
        brukerValg = int(brukerValg)
        for i in gyldigMenyvalg:
            if (i == brukerValg):
                harValgt = True
                forsteGang = False
                valgMeny()
                

def registrer(infoListe):
    global regStudent
    global regEmne
    global regResultat
    
    if (regStudent):
        studNummer = infoListe[0]
        studFornavn = infoListe[1]
        studEtternavn = infoListe[2]
        studium = infoListe[3]

        if os.path.isfile(studentFil): #Filen eksisterer fra før
            studentListe = open(studentFil, "a")
        else: #Finnes ikke fra før
            studentListe = open(studentFil, "w+")

        studentListe.write(str(studNummer) + "\n")
        studentListe.write(str(studFornavn) + "\n")
        studentListe.write(str(studEtternavn) + "\n")
        studentListe.write(str(studium) + "\n")

        studentListe.close()
        regStudent = False
    elif(regEmne):
        emneKode = infoListe[0]
        emneNavn = infoListe[1]
        if os.path.isfile(emneFil):
            emneListe = open(emneFil, "a")
        else:
            emneListe = open(emneFil, "w+")

        emneListe.write(str(emneKode) + "\n")
        emneListe.write(str(emneNavn) + "\n")

        emneListe.close()
        regEmne = False
    elif(regResultat):
        emneKode = infoListe[0]
        studentNummer = infoListe[1]
        karakter = infoListe[2]

        if os.path.isfile(resultatFil):
            resultatListe = open(resultatFil, "a")
        else: #Finnes ikke fra før
            resultatListe = open(resultatFil, "w+")
        
        resultatListe.write(str(emneKode) + "\n")
        resultatListe.write(str(studentNummer) + "\n")
        resultatListe.write(str(karakter) + "\n")

        resultatListe.close()
        regResultat = False


def slettStudent(studentNummer):
    index = 0
    if os.path.isfile(studentFil): #Filen eksisterer fra før
        studentListe = [line.rstrip('\n') for line in open(studentFil)]
        for student in studentListe:
            if (student == studentNummer):
                del studentListe[index + 3]
                del studentListe[index + 2]
                del studentListe[index + 1]
                del studentListe[index]
            index += 1
                
        studFil = open(studentFil, "w")
        studFil.write("\n".join(studentListe))
        studFil.write("\n")
        studFil.close()
    else:
        print("\nFilen med studenter finnes ikke. Kan derfor ikke slette studenten.\n")
        
def skrivUtKarakterliste(studentNummer):
    studentListe = [line.rstrip('\n') for line in open(studentFil)]
    resultatListe = [line.rstrip('\n') for line in open(resultatFil)]
    index = 0
    for studentInfo in studentListe:
        if (studentInfo == studentNummer):
            print("\n")
            print("Studentnummer: " + studentInfo)
            print("Fornavn: " + studentListe[index + 1])
            print("Etternavn: " + studentListe[index + 2])
            print("Studium: " + studentListe[index + 3])
        index += 1

    j = 0
    funnet = False
    for resultatInfo in resultatListe:
        if (resultatInfo == studentNummer):
            if (not funnet):
                print("\n")
                print("Resultatliste for student med studentnummer: " + studentNummer)
                funnet = True
            print("Emnekode: " + resultatListe[j - 1])
            print("Eksamensresultat: " + resultatListe[j + 1])
        j += 1

def skrivUtSensurliste(emneKode):
    studentListe = [line.rstrip('\n') for line in open(studentFil)]
    resultatListe = [line.rstrip('\n') for line in open(resultatFil)]
    emneListe = [line.rstrip('\n') for line in open(emneFil)]
    alleStudenterIEmne = []

    index = 0
    for emne in emneListe:
        if (emne == emneKode):
            print("\n")
            print("Emnekode: " + emne)
            print("Emnenavn: " + emneListe[index + 1])
        index += 1

    index = 0
    for resultat in resultatListe:
        if (resultat == emneKode):
            print(resultat)
            alleStudenterIEmne.append(resultatListe[index + 1])
            alleStudenterIEmne.append(resultatListe[index + 2])
        index += 1

    i = 0
    j = 0
    funnet = False
    if (len(alleStudenterIEmne) > 0):
        for student in studentListe:
            for studentIEmne in alleStudenterIEmne:
                if (student == studentIEmne):
                    if (not funnet):
                        funnet = True
                        print("\n")
                        print("Alle studenter i emne: \n")
                    print("Studentnummer: " + studentListe[i])
                    print("Fornavn: " + studentListe[i + 1])
                    print("Etternavn: " + studentListe[i + 2])
                    print("Studium: " + studentListe[i + 3])
                    print("Karakter: " + alleStudenterIEmne[j + 1])
                    print("\n")
                    i += 4
                    j += 2


def finnesFraFor(objektInfo):
    global finnStudent
    global finnEmne
    global finnResultat
    global finnes
    global slett

    finnes = False
    
    print("\n")
    if (objektInfo[0] == finnStudent and os.path.isfile(studentFil)):
        studentListe = [line.rstrip('\n') for line in open(studentFil)]
        if (len(studentListe) > 0):
            for studentInfo in studentListe:
                if (studentInfo == str(objektInfo[1])):
                    finnes = True
                    objektInfo = []
                    return finnes
        return False
    elif(objektInfo[0] == finnEmne and os.path.isfile(emneFil)):
        emneListe = [line.rstrip('\n') for line in open(emneFil)]
        if (len(emneListe) > 0):
            for emneInfo in emneListe:
                if (str(emneInfo) == str(objektInfo[1])):
                    finnes = True
                    objektInfo = []
                    return finnes
        return False
    elif(objektInfo[0] == finnResultat and os.path.isfile(resultatFil)):
        resultatListe = [line.rstrip('\n') for line in open(resultatFil)]
        index = 0
        if (slett):
            for resultatInfo in resultatListe:
                if (resultatInfo == objektInfo[1]):
                    finnes = True
                    objektInfo = []
                    slett = False
                    return finnes
            slett = False
            return finnes
        else:
            if (len(resultatListe) > 0):
                for resultatInfo in resultatListe:
                    if (str(resultatInfo) == str(objektInfo[1]) and str(resultatListe[index + 1]) == str(objektInfo[2])):
                        finnes = True
                        return finnes
                    index += 1
            return False
    else:
        objektInfo = []
        return False



skrivMeny()
