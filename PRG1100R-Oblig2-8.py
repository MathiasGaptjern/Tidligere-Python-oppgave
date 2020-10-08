from tkinter import *
from tkinter import font
from datetime import date
import pymysql

# Kobler mot databasen 
mindatabase = pymysql.connect(host='localhost',
                              port=3306,
                              user='Biblioteksjef',
                              passwd='bibliotek2018',
                              db='Fagbokbibliotek')

def main():
    mainwindow = Tk()
    mainwindow.title("Hovedmeny")

    btn_administrere = Button(mainwindow, text='Administrere bøker', width = 15, command=administrere_vindu)
    btn_administrere.grid(row=0, column=0, padx=5, pady=5)

    btn_oversikt = Button(mainwindow, text='Oversikt over bøker', width = 15, command=oversikt_vindu)
    btn_oversikt.grid(row=1, column=0, padx=30, pady=5)

    btn_avslutt = Button(mainwindow, text='Avslutt', width = 20, command=mainwindow.destroy)
    btn_avslutt.grid(row=2, column=0, padx=30, pady=20)

    mainwindow.mainloop()

# Lager funksjon å finne dagens dato
def finndato():
    dato = str(date.today())
    return dato

def administrere_vindu():
    def legg_til_bok_vindu():
        def hent_bok():

            markor=mindatabase.cursor()

            markor.execute("SELECT * FROM Bok;")
            
            #Setter utdata til tomme linjer, hvis man søker på ingen bøker eller boken ikke finnes
            status.set('')
            bok_tittel.set('')
            bok_forfatter.set('')
            bok_forlag.set('')
            bok_utgittaar.set('')
            bok_antallsider.set('')
            eksemplr.set('')

            isbn=bok_isbn.get()
            boker_finnes=False

            #Sjekker om bok finnes
            for row in markor:
                if row[0]==isbn:
                    boker_finnes=True

            #Henter info om bok og setter utdata hvis boken finnes            
            if boker_finnes==True:
                eksemplar_markor=mindatabase.cursor()
                eksemplar_markor.execute("SELECT Bok.ISBN, Tittel, Forfatter, Forlag, UtgittAar, AntallSider, COUNT(EksNr) AS AntallEksemplarer FROM Bok, Eksemplar WHERE Bok.ISBN=Eksemplar.ISBN Group by ISBN;")
                for row in eksemplar_markor:
                    if isbn==row[0]:
                        bok_tittel.set(row[1])
                        bok_forfatter.set(row[2])
                        bok_forlag.set(row[3])
                        bok_utgittaar.set(row[4])
                        bok_antallsider.set(row[5])
                        eksemplr.set(row[6])
                
                eksemplar_markor.close()
            else:
                status.set('Bok Finnes ikke')
            
        def legg_til_bok():

            #Henter inndata fra gui
            isbn=bok_isbn.get()
            eksemplarnr=int(eksemplar.get())

            bok_finnes=False
            
            markor=mindatabase.cursor()
            settinn_markor=mindatabase.cursor()

            markor.execute("SELECT * FROM Bok;")

            #Sjekker om boken finnes
            for row in markor:
                if row[0]==isbn:
                    status.set('ISBN Finnes fra før')
                    bok_finnes=True
                    
            #Sjekker hvor mange eksemplarer som boken har
            markor.execute("SELECT Bok.ISBN, COUNT(EksNr) AS AntallEksemplarer FROM Bok, Eksemplar WHERE Bok.ISBN=Eksemplar.ISBN Group by ISBN;")
            for row in markor:
                if row[0]==isbn:
                    eksemplarnr1=int(row[1])+1
            
            #Henter resten av inndata og legger inn data om boken hvis den ikke finnes fra før
            if bok_finnes==False:
                tittel=bok_tittel.get()
                forfatter=bok_forfatter.get()
                forlag=bok_forlag.get()
                utgitt_aar=int(bok_utgittaar.get())
                antall_sider=int(bok_antallsider.get())
                
                settinn_bok=("INSERT INTO Bok"
                             "(ISBN, Tittel, Forfatter, Forlag, UtgittAar, AntallSider)"
                             "VALUES(%s, %s, %s, %s, %s, %s);")
                datany_bok=(isbn, tittel, forfatter, forlag, utgitt_aar, antall_sider)
                settinn_markor.execute(settinn_bok, datany_bok)
                mindatabase.commit()

                #Legger til eksemplarer
                for antall_eksemplarer in range(eksemplarnr):
                    settinn_eksemplar=("INSERT INTO Eksemplar"
                                       "(ISBN, EksNr)"
                                       "VALUES(%s, %s);")
                    datany_eksemplar=(isbn, eksemplarnr)
                    settinn_markor.execute(settinn_eksemplar, datany_eksemplar)
                    mindatabase.commit()
                    eksemplarnr=eksemplarnr-1

                status.set('Bok lagret')
                
            #Legger til eksemplarer hvis boken finnes
            else:
                if eksemplarnr+eksemplarnr1<=10:
                    for antall_eksemplarer in range(eksemplarnr):
                        settinn_eksemplar=("INSERT INTO Eksemplar"
                                           "(ISBN, EksNr)"
                                           "VALUES(%s, %s);")
                        datany_eksemplar=(isbn, eksemplarnr1)
                        settinn_markor.execute(settinn_eksemplar, datany_eksemplar)
                        mindatabase.commit()
                        eksemplarnr1=eksemplarnr1+1
                        status.set('Eksemplar lagret')
                else:
                    status.set('Maks antall eksplarer er 9')

        
        legg_til_bok_vindu = Toplevel()
        legg_til_bok_vindu.title("Legg til bok")
        bold = font.Font(size=16,weight="bold")


        #Legger til labels
        lbl_registrere=Label(legg_til_bok_vindu, text='Legg til bok', font=bold)
        lbl_registrere.grid(row=0, column=0, columnspan=3, padx=10, pady=10)
        
        bok_isbn=StringVar()
        lbl_isbn=Label(legg_til_bok_vindu, text='ISBN:')
        lbl_isbn.grid(row=1, column=0, padx=10, pady=5, sticky=W)
        ent_isbn=Entry(legg_til_bok_vindu, width=20, textvariable=bok_isbn)
        ent_isbn.grid(row=1, column=1, padx=10, pady=5, sticky=W)
        
        bok_tittel=StringVar()
        lbl_tittel=Label(legg_til_bok_vindu, text='Tittel:')
        lbl_tittel.grid(row=2, column=0, padx=10, pady=5, sticky=W)
        ent_tittel=Entry(legg_til_bok_vindu, width=20, textvariable=bok_tittel)
        ent_tittel.grid(row=2, column=1, padx=10, pady=5, sticky=W)

        bok_forfatter=StringVar()
        lbl_forfatter=Label(legg_til_bok_vindu, text='Forfatter:')
        lbl_forfatter.grid(row=3, column=0, padx=10, pady=5, sticky=W)
        ent_forfatter=Entry(legg_til_bok_vindu, width=20, textvariable=bok_forfatter)
        ent_forfatter.grid(row=3, column=1, padx=10, pady=5, sticky=W)

        bok_forlag=StringVar()
        lbl_forlag=Label(legg_til_bok_vindu, text='Forlag:')
        lbl_forlag.grid(row=4, column=0, padx=10, pady=5, sticky=W)
        ent_forlag=Entry(legg_til_bok_vindu, width=20, textvariable=bok_forlag)
        ent_forlag.grid(row=4, column=1, padx=10, pady=5, sticky=W)

        bok_utgittaar=StringVar()
        lbl_utgittaar=Label(legg_til_bok_vindu, text='Utgitt år:')
        lbl_utgittaar.grid(row=5, column=0, padx=10, pady=5, sticky=W)
        ent_utgittaar=Entry(legg_til_bok_vindu, width=5, textvariable=bok_utgittaar)
        ent_utgittaar.grid(row=5, column=1, padx=10, pady=5, sticky=W)

        bok_antallsider=StringVar()
        lbl_antallsider=Label(legg_til_bok_vindu, text='Antall sider:')
        lbl_antallsider.grid(row=6, column=0, padx=10, pady=5, sticky=W)
        ent_antallsider=Entry(legg_til_bok_vindu, width=5, textvariable=bok_antallsider)
        ent_antallsider.grid(row=6, column=1, padx=10, pady=5, sticky=W)

        eksemplar=StringVar()
        lbl_eksemplar=Label(legg_til_bok_vindu, text='Antall eksemplarer: ')
        lbl_eksemplar.grid(row=7, column=0, padx=10, pady=5, sticky=W)
        ent_eksemplar=Entry(legg_til_bok_vindu, width=2, textvariable=eksemplar)
        ent_eksemplar.grid(row=7, column=1, padx=10, pady=5, sticky=W)

        eksemplr=StringVar()
        lbl_eksemplr=Label(legg_til_bok_vindu, text='Antall eksemplarer:')
        lbl_eksemplr.grid(row=8, column=0, padx=10, pady=5, sticky=W)
        ent_eksemplr=Entry(legg_til_bok_vindu, width=2, state="readonly", textvariable=eksemplr, justify='center')
        ent_eksemplr.grid(row=8, column=1, padx=10, pady=5, sticky=W)

        #Legger til knapp for funksjon
        btn_lagre=Button(legg_til_bok_vindu, width=10, text='Lagre bok', command=legg_til_bok)
        btn_lagre.grid(row=9, column=0, columnspan=3, padx=5, pady=10)

        btn_søk=Button(legg_til_bok_vindu, width=10, text='Søk ISBN', command=hent_bok)
        btn_søk.grid(row=1, column=2, sticky=E)
        
        #Lager utdata
        status=StringVar()
        lbl_status=Label(legg_til_bok_vindu, text='Status:')
        lbl_status.grid(row=10, column=0, columnspan=3, padx=10, pady=5)
        ent_status=Entry(legg_til_bok_vindu, width=25, state='readonly', textvariable=status, justify='center')
        ent_status.grid(row=11, column=0, columnspan=3, padx=10, pady=5)
       

        #knapp for å avslutte
        btn_tilbake=Button(legg_til_bok_vindu, width=10, text='Tilbake', command=legg_til_bok_vindu.destroy)
        btn_tilbake.grid(row=12, column=2, padx=5, pady=5, sticky=E)
        
    def legg_til_lanetager_vindu():
        def laner():
            try:
                sett_ny_markor = mindatabase.cursor()

                # Henter informasjon fra GUI
                var_lnr = int(lnr.get())
                var_fornavn = fornavn.get()
                var_etternavn = etternavn.get()

                # Oppdaterer tabell med hentet informasjon
                sett_ny_laner = ("INSERT INTO Laaner"
                                "(LNr, Fornavn, Etternavn)"
                                "VALUES(%s, %s, %s)")
                
                ny_laner = (var_lnr, var_fornavn, var_etternavn)
                sett_ny_markor.execute(sett_ny_laner, ny_laner) 
                mindatabase.commit()
                    
                sett_ny_markor.close()
                status.set('Bruker opprettet')
            except pymysql.IntegrityError:
                status.set('Lånenr finnes fra før')
            except pymysql.OperationalError:
                status.set('Ikke tilgang')
                
        legg_til_lanetager_vindu = Toplevel()
        legg_til_lanetager_vindu.title("Legg til lånetager")
        bold = font.Font(size=16,weight="bold")

        lbl_laaner=Label(legg_til_lanetager_vindu, text='Legg til lånetager', font=bold)
        lbl_laaner.grid(row=0, column=1, columnspan=2, padx=10, pady=10)

        lnr = StringVar()
        lbl_lnr = Label(legg_til_lanetager_vindu, text='Lånenr:' )
        lbl_lnr.grid(row = 1, column = 1, padx = 10, pady = 5, sticky=W)
        ent_lnr = Entry(legg_til_lanetager_vindu, width=4, textvariable=lnr)
        ent_lnr.grid(row = 1, column = 2, padx = 5, pady = 5, sticky=W)

        fornavn = StringVar()
        lbl_fornavn = Label(legg_til_lanetager_vindu, text='Fornavn:')
        lbl_fornavn.grid(row = 2, column = 1, padx = 10, pady = 5, sticky=W)
        ent_fornavn = Entry(legg_til_lanetager_vindu, width = 15, textvariable = fornavn)
        ent_fornavn.grid(row=2, column = 2, padx = 5, pady = 5, sticky=W)

        etternavn = StringVar()
        lbl_etternavn = Label(legg_til_lanetager_vindu, text='Etternavn:')
        lbl_etternavn.grid(row = 3, column = 1, padx = 10, pady = 5, sticky=W)
        ent_etternavn = Entry(legg_til_lanetager_vindu, width = 15, textvariable = etternavn)
        ent_etternavn.grid(row = 3, column = 2, padx = 5, pady = 5, sticky=W)

        btn_lagre = Button(legg_til_lanetager_vindu, text = 'Legg til', width=10, command=laner) 
        btn_lagre.grid(row = 4,column=1, columnspan = 2, padx = 5, pady = 5)

        status = StringVar()
        lbl_status=Label(legg_til_lanetager_vindu, text='Status:')
        lbl_status.grid(row = 5, column = 1, columnspan = 2, padx = 5, pady = 5)
        ent_status = Entry(legg_til_lanetager_vindu, width = 25, state='readonly', textvariable=status, justify='center')
        ent_status.grid(row = 6, column = 1, columnspan = 2, padx = 5, pady = 5)
        
        btn_tilbake = Button(legg_til_lanetager_vindu, text='Tilbake', width=10, command=legg_til_lanetager_vindu.destroy)
        btn_tilbake.grid(row=7, column=2, padx=5, pady=5, sticky=E)

    def utlaan():                               
        def registrer():
            # Henter informasjon fra GUI
            risbn = isbn.get()
            reksnr = eksnr.get()
            rlnr = lnr.get()
            
            markor = mindatabase.cursor()
            
            # Sjekker om lånetager eksisterer
            markor.execute("SELECT * FROM Laaner")
            laaner_finnes = False

            for row in markor:
                if row[0] == rlnr:
                    laaner_finnes = True

            if laaner_finnes:
                # Oppretter utlånsnr
                utlaansnr = 1000
                markor.execute("SELECT * FROM Utlaan")
                for row in markor:
                    if int(row[0]) == int(utlaansnr):
                        utlaansnr += 1

                # Sjekk om isbn finnes
                markor.execute("SELECT ISBN FROM Bok")

                isbn_finnes = False
                row = markor.fetchone()
                while row is not None:
                    if risbn == row[0]:
                        isbn_finnes = True
                        row = None
                    else:
                        row = markor.fetchone()
                        
                if isbn_finnes:
                    # Sjekk om isbn og eksnr er utlånt fra før
                    markor.execute("SELECT ISBN, EksNr FROM Utlaan WHERE Innleveringsdato IS NULL")

                    laanbar = True
                    row = markor.fetchone()
                    while row is not None:
                        if risbn == row[0] and reksnr == row[1]:
                            laanbar = False
                            row = None
                        else:
                            row = markor.fetchone()

                    if laanbar:
                        # Henter dagens dato fra finndato funksjon
                        dato = finndato()
                        # Registrer bok med eksemplarnr
                        registrer_lan = ("INSERT INTO Utlaan"
                                         "(UtlaansNr, LNr, ISBN, EksNR, Utlaansdato)"
                                         "VALUES(%s, %s, %s, %s, %s);")
                        registrer_var = (utlaansnr, rlnr, risbn, reksnr, dato)
                        markor.execute(registrer_lan, registrer_var)
                        mindatabase.commit()
                        status.set('Utlån er registrert')
                    else:
                        status.set('Allerede utlånt')
                else:
                    status.set('ISBN finnes ikke')
            else:
                status.set('Lånetager finnes ikke')
    
            markor.close()
            
        utlaan_vindu = Toplevel()
        utlaan_vindu.title('Utlån')
        bold = font.Font(size=16,weight="bold")

        lbl_utlaan=Label(utlaan_vindu, text='Utlån av bok', font=bold)
        lbl_utlaan.grid(row=0, column=0, columnspan=2, padx=10, pady=10)
        
        isbn = StringVar()
        lbl_isbn=Label(utlaan_vindu, text='ISBN:')
        lbl_isbn.grid(row=1, column=0, padx=10, pady=5, sticky=W)
        ent_isbn=Entry(utlaan_vindu, width=14, textvariable=isbn, justify='center')
        ent_isbn.grid(row=1, column=1, padx=10, pady=5)

        eksnr = StringVar()
        lbl_eksnr=Label(utlaan_vindu, text='Eksemplarnr:')
        lbl_eksnr.grid(row=2, column=0, padx=10, pady=5, sticky=W)
        ent_eksnr=Entry(utlaan_vindu, width=2, textvariable=eksnr, justify='center')
        ent_eksnr.grid(row=2, column=1, padx=10, pady=5, sticky=W)

        lnr = StringVar()
        lbl_lnr=Label(utlaan_vindu, text='LNR:')
        lbl_lnr.grid(row=4, column=0, padx=10, pady=5, sticky=W)
        ent_lnr=Entry(utlaan_vindu, width=5, textvariable=lnr, justify='center')
        ent_lnr.grid(row=4, column=1, padx=10, pady=5, sticky=W)

        btn_registrer = Button(utlaan_vindu, text='Registrer lån', width = 10, command = registrer) 
        btn_registrer.grid(row=6, column=0, columnspan = 2, padx=5, pady=5)

        status = StringVar()
        lbl_status=Label(utlaan_vindu, text='Status:')
        lbl_status.grid(row=7, column=0, columnspan=2, padx=10, pady=5)
        ent_status=Entry(utlaan_vindu, width = 30, state='readonly', textvariable=status, justify = 'center')
        ent_status.grid(row=8, column=0, columnspan=2, padx=10, pady=5)

        btn_tilbake = Button(utlaan_vindu, text='Tilbake', width = 10, command=utlaan_vindu.destroy)
        btn_tilbake.grid(row=9, column=1, padx=5, pady=5, sticky=E)

    def innlevering_vindu():
        def lever_sok():
            levering_markor = mindatabase.cursor()
            settinn_markor = mindatabase.cursor()

            isbn_lokal = isbn.get()
            eksnr_lokal = eksnr.get()

            # Henter ut utlaansnummer fra utlaans tabellen
            utlaan_sok = ("SELECT * FROM Utlaan WHERE ISBN = %s AND EksNr=%s AND Innleveringsdato IS NULL")
            utlaan_var = (isbn_lokal, eksnr_lokal)
            levering_markor.execute(utlaan_sok,utlaan_var)
            utlaans_nr = ''

            for row in levering_markor:
                utlaans_nr = row[0]

            if utlaans_nr != '':
                #Oppdaterer databasen med dagens dato som innleveringsdato
                dato = finndato()
                settinn_sok = ("UPDATE Utlaan SET Innleveringsdato=%s WHERE UtlaansNr =%s")
                settinn_var = (dato,utlaans_nr)
                settinn_markor.execute(settinn_sok,settinn_var)
                mindatabase.commit()

                levering_markor.close()
                settinn_markor.close()
                status.set('Bok er levert')
            else:
                status.set('Bok er ikke på utlån')

        innlevering_vindu = Toplevel()
        innlevering_vindu.title('Innlevering')
        bold = font.Font(size=16,weight="bold")

        lbl_innlevering=Label(innlevering_vindu, text='Innlevering av bok', font=bold)
        lbl_innlevering.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

        isbn=StringVar()
        lbl_isbn=Label(innlevering_vindu, text='ISBN:')
        lbl_isbn.grid(row=1,column=0,padx=10,pady=5, sticky=W)
        ent_isbn=Entry(innlevering_vindu,width=14,textvariable=isbn)
        ent_isbn.grid(row=1,column=1,padx=10,pady=5, sticky=W)

        eksnr=StringVar()
        lbl_eksnr=Label(innlevering_vindu, text='Eksemplarnr:')
        lbl_eksnr.grid(row=2, column=0, padx=10, pady=5,sticky=W)
        ent_eksnr=Entry(innlevering_vindu, width=2,textvariable=eksnr)
        ent_eksnr.grid(row=2, column=1, padx=10, pady=5, sticky=W)

        btn_lever=Button(innlevering_vindu, text='Lever bok', width=10, command=lever_sok)
        btn_lever.grid(row=3, column=0,columnspan=2, padx=5, pady=5)

        status=StringVar()
        lbl_status=Label(innlevering_vindu, text='Status:')
        lbl_status.grid(row=4, column=0, columnspan=2, padx=10, pady=5)
        ent_status=Entry(innlevering_vindu, width=30, state='readonly', textvariable=status, justify='center')
        ent_status.grid(row=5, column=0, columnspan=2, padx=10, pady=5)

        btn_tilbake=Button(innlevering_vindu, text='Tilbake', width=10, command=innlevering_vindu.destroy)
        btn_tilbake.grid(row=6, column=1, padx=5, pady=5)


    window2 = Toplevel()
    window2.title("Bøker")

    #Knapper for funksjoner
    btn_registrere = Button(window2, text='Legg til bok', width = 15, command=legg_til_bok_vindu)
    btn_registrere.grid(row=0, column=0, padx=30, pady=5)

    btn_registrere_lanetaker = Button(window2, text='Legg til lånetager', width = 15, command=legg_til_lanetager_vindu)
    btn_registrere_lanetaker.grid(row=1, column=0, padx=30, pady=5,)

    btn_utlan = Button(window2, text='Lån ut bok', width = 15, command=utlaan)
    btn_utlan.grid(row=2, column=0, padx=30, pady=5)

    btn_levere = Button(window2, text='Lever inn bok', width = 15, command=innlevering_vindu)
    btn_levere.grid(row=3, column=0, padx=30, pady=5)

    btn_tilbake = Button(window2, text='Tilbake til hovedmeny', width = 20, command=window2.destroy)
    btn_tilbake.grid(row=4, column=0, padx=30, pady=20)
    
def oversikt_vindu():
    def boker_utlaan_vindu():
        # Lager en funksjon for å skrolle på alle listebokser
        def yview(*args):
            lst_utlaansnr.yview(*args)
            lst_tittel.yview(*args)
            lst_forfatter.yview(*args)
            lst_eksnr.yview(*args)
            lst_laanenr.yview(*args)
            lst_navn.yview(*args)
            lst_utlaansdato.yview(*args)

        # Går inn i database for å hente ut informasjon
        oversikt_markor = mindatabase.cursor()
        oversikt_markor.execute("SELECT UtlaansNr, Tittel, Forfatter, EksNr, Utlaan.LNr, Fornavn, Etternavn, Utlaansdato FROM Utlaan, Laaner, Bok WHERE Utlaan.LNr = Laaner.LNr AND Utlaan.ISBN = Bok.ISBN AND Innleveringsdato IS NULL ORDER BY Tittel")

        # Oppretter lister for hver listbox
        utlaansnr_liste = []
        tittel_liste = []
        forfatter_liste = []
        eksnr_liste = []
        laanenr_liste = []
        navn_liste = []
        utlaansdato_liste = []

        # Fyller listene med informasjon               
        for row in oversikt_markor:
            utlaansnr_liste += [row[0]]
            tittel_liste += [row[1]]
            forfatter_liste += [row[2]]
            eksnr_liste += [row[3]]
            laanenr_liste += [row[4]]
            navn_liste += [row[5] + ' ' + row[6]]
            utlaansdato_liste += [row[7]]
        
        boker_utlaan_vindu = Toplevel()
        boker_utlaan_vindu.title("Bøker utlånt")
        bold = font.Font(size=16,weight="bold")

        # Oppretter scroll-variablen og legger til command yview(som refererer til yview funksjonen ovenfor)
        y_scroll = Scrollbar(boker_utlaan_vindu,orient=VERTICAL, command=yview)
        y_scroll.grid(row=2, column=7, padx=(0,10), pady=5, sticky=(NS,W))

        lbl_overskrift=Label(boker_utlaan_vindu, text='Oversikt over utlånte bøker', font=bold)
        lbl_overskrift.grid(row=0, columnspan=7)

        utlaansnr = StringVar()
        lbl_utlaansnr=Label(boker_utlaan_vindu, text='Utlånsr')
        lbl_utlaansnr.grid(row=1, column=0, padx=(20,0))
        lst_utlaansnr=Listbox(boker_utlaan_vindu, width=8, height=25, listvariable=utlaansnr,borderwidth=0, highlightthickness=0,yscrollcommand = y_scroll.set, justify='center')
        lst_utlaansnr.grid(row=2,column=0, padx=(20,0))
        utlaansnr.set(tuple(utlaansnr_liste))

        tittel = StringVar()
        lbl_tittel=Label(boker_utlaan_vindu, text='Tittel')        
        lbl_tittel.grid(row=1, column=1)
        lst_tittel=Listbox(boker_utlaan_vindu, height=25, listvariable=tittel,borderwidth=0, highlightthickness=0,yscrollcommand = y_scroll.set, justify='center')
        lst_tittel.grid(row=2,column=1, padx=0)
        tittel.set(tuple(tittel_liste))

        forfatter = StringVar()
        lbl_forfatter=Label(boker_utlaan_vindu, text='Forfatter')        
        lbl_forfatter.grid(row=1, column=2)
        lst_forfatter=Listbox(boker_utlaan_vindu, height=25, listvariable=forfatter,borderwidth=0, highlightthickness=0,yscrollcommand = y_scroll.set, justify='center')
        lst_forfatter.grid(row=2,column=2, padx=0)
        forfatter.set(tuple(forfatter_liste))

        eksnr = StringVar()
        lbl_eksnr=Label(boker_utlaan_vindu, text='EksNr')        
        lbl_eksnr.grid(row=1, column=3)
        lst_eksnr=Listbox(boker_utlaan_vindu, height=25, width=4, listvariable=eksnr,borderwidth=0, highlightthickness=0,yscrollcommand = y_scroll.set, justify='center')
        lst_eksnr.grid(row=2,column=3, padx=0, sticky=(W,E))
        eksnr.set(tuple(eksnr_liste))

        laanenr = StringVar()
        lbl_laanenr=Label(boker_utlaan_vindu, text='Lånenr')        
        lbl_laanenr.grid(row=1, column=4)
        lst_laanenr=Listbox(boker_utlaan_vindu, height=25, width=8, listvariable=laanenr,borderwidth=0, highlightthickness=0,yscrollcommand = y_scroll.set, justify='center')
        lst_laanenr.grid(row=2,column=4, padx=0)
        laanenr.set(tuple(laanenr_liste))

        navn = StringVar()
        lbl_navn=Label(boker_utlaan_vindu, text='Navn')        
        lbl_navn.grid(row=1, column=5)
        lst_navn=Listbox(boker_utlaan_vindu, height=25, listvariable=navn,borderwidth=0, highlightthickness=0,yscrollcommand = y_scroll.set, justify='center')
        lst_navn.grid(row=2,column=5, padx=0)
        navn.set(tuple(navn_liste))

        utlaansdato = StringVar()
        lbl_utlaansdato=Label(boker_utlaan_vindu, text='Utlånsdato')
        lbl_utlaansdato.grid(row=1, column=6)
        lst_utlaansdato=Listbox(boker_utlaan_vindu, height=25, listvariable=utlaansdato,borderwidth=0, highlightthickness=0,yscrollcommand = y_scroll.set, justify='center')
        lst_utlaansdato.grid(row=2, column=6, padx=0, sticky=E)
        utlaansdato.set(tuple(utlaansdato_liste))

        btn_tilbake = Button(boker_utlaan_vindu, text='Tilbake', width = 10, command=boker_utlaan_vindu.destroy)
        btn_tilbake.grid(row=3, column=6,columnspan=2, padx=5, pady=5, sticky=E)

    def aldri_utlaant():
        def utlaant(event):
            markert = lst_oversikt.get(lst_oversikt.curselection())
            # Søker i Bok-tabellen etter riktig informasjon
            info_markor = mindatabase.cursor()
            info_markor.execute(
                "SELECT Tittel, ISBN, Forfatter, Forlag, UtgittAar, AntallSider FROM Bok GROUP BY ISBN, Tittel, Forfatter, Forlag, UtgittAar, AntallSider")
            # Fyller inn riktig informasjon i listen
            for row in info_markor:
                if markert == row[0]:
                    isbn.set(row[1])
                    forfatter.set(row[2])
                    forlag.set(row[3])
                    utgitt.set(row[4])
                    sider.set(row[5])
            info_markor.close()

        # Sjekker om Boken ikke er lånt ut noen gang
        oversikt_utlaant_liste = []
        oversikt_markor = mindatabase.cursor()
        oversikt_markor.execute('SELECT Tittel FROM Bok WHERE ISBN NOT IN (SELECT ISBN FROM Utlaan)')
        # Fyller listen med riktig informasjon fra markøren
        for r in oversikt_markor:
            oversikt_utlaant_liste += [r[0]]

        oversikt_markor.close()

        aldri_utlaant = Toplevel()
        aldri_utlaant.title("Aldri Utlånt")
        bold = font.Font(size=16,weight="bold")


        y_scroll_overskrift = Scrollbar(aldri_utlaant, orient=VERTICAL)
        y_scroll_overskrift.grid(row=1, rowspan=9,padx=(0,10), pady=5, column = 1,sticky=NS)

        oversikt = StringVar()
        lbl_oversikt=Label(aldri_utlaant, text='Oversikt over aldri utlånte bøker', font=bold, justify='center')
        lbl_oversikt.grid(row=0, column=0, columnspan=4, padx=5,pady=5)
        
        lst_oversikt=Listbox(aldri_utlaant, width=40, listvariable=oversikt, yscrollcommand = y_scroll_overskrift.set)
        lst_oversikt.grid(row=1, rowspan=9,column=0,padx=(10,0),pady=5,sticky=E)
        oversikt.set(tuple(oversikt_utlaant_liste))
        y_scroll_overskrift['command'] = lst_oversikt.yview

        isbn = StringVar()
        ent_isbn=Entry(aldri_utlaant,state='readonly',textvariable=isbn, justify='center')
        ent_isbn.grid(row=1, column=3,padx=10,pady=5,sticky=E)
        lbl_isbn = Label(aldri_utlaant, text='ISBN:')
        lbl_isbn.grid(row=1, column=2, padx=10, pady=5, sticky=W)

        forfatter = StringVar()
        ent_forfatter=Entry(aldri_utlaant,state='readonly',textvariable=forfatter, justify='center')
        ent_forfatter.grid(row=3,column=3,padx=10,pady=5,sticky=E)
        lbl_forfatter=Label(aldri_utlaant,text='Forfatter:')
        lbl_forfatter.grid(row=3,column=2,padx=10,pady=5,sticky=W)

        forlag = StringVar()
        ent_forlag=Entry(aldri_utlaant,state='readonly',textvariable=forlag, justify='center')
        ent_forlag.grid(row=4,column=3,padx=10,pady=5,sticky=E)
        lbl_forlag=Label(aldri_utlaant,text='Forlag:')
        lbl_forlag.grid(row=4,column=2,padx=10,pady=5,sticky=W)

        utgitt = StringVar()
        ent_utgitt=Entry(aldri_utlaant, width=5, state='readonly',textvariable=utgitt, justify='center')
        ent_utgitt.grid(row=5,column=3,padx=10,pady=5,sticky=W)
        lbl_utgitt=Label(aldri_utlaant,text='Utgitt:')
        lbl_utgitt.grid(row=5,column=2,padx=10,pady=5,sticky=W)

        sider = StringVar()
        ent_sider=Entry(aldri_utlaant,width=5, state='readonly',textvariable=sider, justify='center')
        ent_sider.grid(row=6,column=3,padx=10,pady=5,sticky=W)
        lbl_sider=Label(aldri_utlaant,text='Antall sider:')
        lbl_sider.grid(row=6,column=2,padx=10,pady=5,sticky=W)

        btn_tilbake = Button(aldri_utlaant, width=10, text='Tilbake', command=aldri_utlaant.destroy)
        btn_tilbake.grid(row=11, column=3, padx=5, pady=5, sticky=E)

        lst_oversikt.bind('<<ListboxSelect>>',utlaant)

    def boker_statistikk():
        def statistikk(event):
            valgt = lst_oversikt.get(lst_oversikt.curselection())         

            # Henter informasjon fra database
            info_markor = mindatabase.cursor()
            info_markor.execute("SELECT Tittel, Bok.ISBN, Forfatter, Forlag, UtgittAar, AntallSider, COUNT(Utlaan.ISBN) AS AntallUtlaan FROM Bok LEFT JOIN Utlaan ON Bok.ISBN = Utlaan.ISBN GROUP BY Bok.ISBN, Tittel, Forfatter, Forlag, UtgittAar, AntallSider")

            for row in info_markor:                
                if valgt == row[0]:
                    isbn.set(row[1])
                    forfatter.set(row[2])
                    forlag.set(row[3])
                    utgitt.set(row[4])
                    sider.set(row[5])
                    utlaan.set(row[6])

            info_markor.close()

        oversikt_markor = mindatabase.cursor()

        oversikt_markor.execute("SELECT Tittel FROM Bok")

        # Legger informasjon inn i liste
        boker = []
        for row in oversikt_markor:
            boker += [row[0]]

        boker_statistikk = Toplevel()
        boker_statistikk.title("Oversikt")

        # Oppretter scroll-variablen
        y_scroll = Scrollbar(boker_statistikk,orient=VERTICAL)
        y_scroll.grid(row=1, column=1, rowspan=6, padx=(0,10), pady=5, sticky=NS)

        oversikt_statistikk = StringVar()
        lbl_oversikt=Label(boker_statistikk, text='Oversikt over alle bøker', font=bold)
        lbl_oversikt.grid(row=0, column=0, columnspan=4, padx=5,pady=5)
        lst_oversikt=Listbox(boker_statistikk, width=40, listvariable=oversikt_statistikk, justify='left',yscrollcommand = y_scroll.set)
        lst_oversikt.grid(row=1,column=0, rowspan=6,padx=(10,0),pady=5, sticky=E)
        oversikt_statistikk.set(tuple(boker))
        y_scroll['command'] = lst_oversikt.yview

        isbn = StringVar()
        lbl_isbn=Label(boker_statistikk, text='ISBN:')
        lbl_isbn.grid(row=1, column=2, padx=10, pady=5, sticky=W)
        ent_isbn=Entry(boker_statistikk, state='readonly', textvariable=isbn, justify='center')
        ent_isbn.grid(row=1, column=3, padx=10, pady=5, sticky=W)

        forfatter = StringVar()
        lbl_forfatter=Label(boker_statistikk, text='Forfatter:')
        lbl_forfatter.grid(row=2, column=2, padx=10, pady=5, sticky=W)
        ent_forfatter=Entry(boker_statistikk, state='readonly', textvariable=forfatter, justify='center')
        ent_forfatter.grid(row=2, column=3, padx=10, pady=5, sticky=W)

        forlag = StringVar()
        lbl_forlag=Label(boker_statistikk, text='Forlag:')
        lbl_forlag.grid(row=3, column=2, padx=10, pady=5, sticky=W)
        ent_forlag=Entry(boker_statistikk, state='readonly', textvariable=forlag, justify='center')
        ent_forlag.grid(row=3, column=3, padx=10, pady=5, sticky=W)

        utgitt = StringVar()
        lbl_utgitt=Label(boker_statistikk, text='Utgitt år:')
        lbl_utgitt.grid(row=4, column=2, padx=10, pady=5, sticky=W)
        ent_utgitt=Entry(boker_statistikk, width=4, state='readonly', textvariable=utgitt, justify='center')
        ent_utgitt.grid(row=4, column=3, padx=10, pady=5, sticky=W)

        sider = StringVar()
        lbl_sider=Label(boker_statistikk, text='Antall sider:')
        lbl_sider.grid(row=5, column=2, padx=10, pady=5, sticky=W)
        ent_sider=Entry(boker_statistikk, width=4, state='readonly', textvariable=sider, justify='center')
        ent_sider.grid(row=5, column=3, padx=10, pady=5, sticky=W)

        utlaan = StringVar()
        lbl_utlaan=Label(boker_statistikk, text='Antall utlån:')
        lbl_utlaan.grid(row=6, column=2, padx=10, pady=5, sticky=W)
        ent_utlaan=Entry(boker_statistikk, width=4, state='readonly', textvariable=utlaan, justify='center')
        ent_utlaan.grid(row=6, column=3, padx=10, pady=5, sticky=W)

        btn_tilbake = Button(boker_statistikk, text='Tilbake', width = 10, command=boker_statistikk.destroy)
        btn_tilbake.grid(row=7, column=3, padx=5, pady=5, sticky=E)

        lst_oversikt.bind('<<ListboxSelect>>', statistikk)

    window3 = Toplevel()
    window3.title("Oversikt")
    bold = font.Font(size=16,weight="bold")

    btn_utlant = Button(window3, text='Bøker utlånt', width = 15, command=boker_utlaan_vindu)
    btn_utlant.grid(row=0, column=0, padx=30, pady=5)

    btn_aldri_utlant = Button(window3, text='Aldri utlånte bøker', width = 15, command=aldri_utlaant)
    btn_aldri_utlant.grid(row=1, column=0, padx=30, pady=5)

    btn_statistikk = Button(window3, text='Statistikk over bøker', width = 15, command=boker_statistikk)
    btn_statistikk.grid(row=2, column=0, padx=30, pady=5)

    btn_tilbake = Button(window3, text='Tilbake til hovedmeny', width = 20, command=window3.destroy)
    btn_tilbake.grid(row=3, column=0, padx=30, pady=30)

main()

mindatabase.close()
