"""Popeanga Antonia-Maria
   Popa Jasmine
   Grupa 141"""
#fisierul din input valideaza stringurile care sunt formate dintr-un numar par de 1
def parsare(fisier, Q, E, L, F,S,T):
    with open(fisier,"r") as f:
        #citim prima linie din fisier
        linie = f.readline().strip()
        #verificam daca s-a ajuns la finalul fisierului
        while linie != "":
            #verificam pe ce sectiune suntem si dupa aceea citim urmatoarea linie
            #verificam sa nu fim pe linia cu End
            #apoi adaugam datele in liste daca e satisfacuta conditia din while
            #dupa citim urmatoarea linie
            #pentru a o verifica din nou in conditia din while ca ea sa fie diferita de End
            #continuam procesul pana nu se mai satisface conditia din while
            if linie=='Alphabet:':
                linie = f.readline().strip()
                while linie!='End':
                    E.append(linie)
                    linie = f.readline().strip()
            if linie=='ListAlphabet:':
                linie = f.readline().strip()
                while linie != 'End':
                    L.append(linie)
                    linie = f.readline().strip()
            if linie=='States:':
                linie = f.readline().strip()
                while linie != 'End':
                    Q.append(linie)
                    linie = f.readline().strip()

            if linie=='Start:':
                linie = f.readline().strip()
                while linie != 'End':
                    S.append(linie)
                    linie = f.readline().strip()
            if linie=='AcceptStates:':
                linie = f.readline().strip()
                while linie != 'End':
                    F.append(linie)
                    linie = f.readline().strip()
            #pentru tranzitii vom da split dupa ' -> ' si vom face o lista de liste
            #prima pozitie din sublista adica sublista[0] este partea din stanga a tranzitiei si sublista[1] partea din dreapta
            #exemplu ['0 0 e', '0 e e']
            #si vom face o lista de astfel de subliste
            if linie == 'Transitions:':
                linie = f.readline().strip()
                while linie != 'End':
                    tranzitie = []
                    if linie != 'End':
                        t = linie.split(" -> ")
                        tranzitie.append(t[0])
                        tranzitie.append(t[1])
                        T.append(tranzitie)
                    linie = f.readline().strip()
            linie = f.readline().strip()
def citire(fisier):
    Q = list()#multime stari
    E = list()#alfabetul input
    L = list()#alfabetul listei
    F = list()#multimea starilor finale
    S = list()#starea de start
    T=list()#lista tranzitiilor
    #incepem prin parsarea fisierului de input si adunam informatiile neecsare pentru fiecare lista
    parsare(fisier, Q, E, L, F,S,T)
    #dupa ce am adaugat informatiile necesare returnam listele finale
    return Q, E, L, F,S,T
def afisare(fisier):
    #apelam functia de citire pentru a aduna informatiile despre fiecare lista
    Q, E, L, F,S,T= citire(fisier)
    #afisarea structurii LA-ului
    print("Configuratia LA-ului:")
    print("Multimea starilor: ", Q)
    print("Multimea alfabetului de input: ", E)
    print("Alfabetul listei: ", L)
    print("Multimea starilor finale: ", F)
    print("Starea de start: ", S)
    print("Multimea tranzitiilor: ", T)
    #vom valida datele LA-ului
    print(validare_LA(fisier))
def validare_LA(fisier):
    #avem doua functii de validare
    #LA-ul este valid doar daca ambele functii vor returna True
    if validare_start(fisier) == True and validare_tranzitii(fisier) == True:
        return True
    else:
        return False
def validare_start(fisier):
    Q, E, L, F,S,T= citire(fisier)
    #in aceasta functie ne asiguram ca exista o singura stare de start
    if len(S) == 1 :
        return True
    return False
def validare_tranzitii(fisier):
    Q, E, L, F, S, T = citire(fisier)
    #luam pe rand fiecare tranzitie in multimea tranzitiilor T
    #le vom da split dupa spatiu partii din stanga sagetii t0 si celei din dreapta t1
    for t in T:
        t0=t[0].split()
        t1=t[1].split()
        #verificam daca primul element din tranzitia din stanga este din multimea starilor
        #al doilea din alfabet si al treilea din alfabetul listei
        #daca nu se indeplinesc toate cele 3 conditii functia returneaza False
        if t0[0] not in Q or t0[1] not in E or t0[2] not in L:
                return False
        #verificam daca primul elemnt din tranzitia din dreapta este din multimea starilor
        #al doilea si al treilea sa fie din alfabetul listei
        #daca aceste 3 conditii nu sunt indeplinite se retruneaza False
        if t1[0] not in Q or t1[1] not in L or t1[2] not in L:
                return False
    #la final daca nu s-a returnat False, returnam True
    return True
def validare_sir(sir):
    Q, E, L, F, S, T = citire(fisier)
    #trebuie sa verificam daca stringul dat este valid
    #pentru acest lucru, avem nevoie si sa reprezentam matriceal functia de tranzitie
    matrice_LA,lista_LA,modif_lista=functie_tranzitie(fisier)
    print('Matricea LA este: ',matrice_LA, 'Lista LA este:',lista_LA,'Modificarea listei: ',modif_lista)

    #odata ce avem matricea LA, lista LA si lista ajutatoare, trebuie sa vedem daca drumul descris este valid
    drum,lista_sir=parcurgere_sir(sir,matrice_LA,lista_LA,modif_lista)
    print(drum,lista_sir)
    print(validare(drum,lista_sir))
def functie_tranzitie(fisier):
    Q, E, L, F, S, T = citire(fisier)
    #pentru inceput, realizam scheletul unei matrice de dimensiunile necesare
    matrice_LA = [[[] for x in range(len(E))] for y in range(len(Q))]

    #initializam 2 liste goale una pentru elementele din primul 3-tuplu(al treilea element)
    #exemplu 1 0 a -> 1 e e, in acest caz al treilea element din primul 3-tuplu este a
    #a doua lista este o lista de liste care va fi de forma [[ce trebuie scos din lista,ce trebuie adaugat in lista]...[]...]
    lista_LA=[]
    modif_lista=[]

    #pentru fiecare tranzitie din lista de tranzitii, preluam fiecare element din acestea
    for i in T:
        ls=[]
        #facem lista cu al treilea element din trpimul 3-tuplu
        lista_LA.append(i[0][-1])
        #selectam cele 2 elemente din al doilea 3-tuplu care reprezinta ce trebuie adaugat si scos din lista
        ls.append(i[1][2])
        ls.append(i[1][4])
        #dupa ce am adaugat in lista cele 2 elemente il aduagam in lista mare modif_lista
        modif_lista.append(ls)
        #formam matricea LA-ului are drept linii starile si drep coloane inputurile
        #folosim index pentru a vedea ce pozitie ocupa simbolul in lista alfabetului
        #si dam append starii in care ajungem care se afla in al doilea 3-tuplu pe prima pozitie i[1][0]
        #matricea va fi de exemplu
        #0 1
        #1 0
        #2 0
        #unde cele 3 linii sunt cele 3 stari 0,1,2 cele doua coloane sunt inputurile 0,1
        #si valorile din matrice starile unde ajungem in functie de stare si input
        matrice_LA[int(i[0][0])][E.index(i[0][2])].append(int(i[1][0]))
    return matrice_LA, lista_LA,modif_lista
def parcurgere_sir(sir,matrice_LA,lista_LA,modif_lista):
    Q, E, L, F, S, T = citire(fisier)
    #initializam drumul cu starea de start si lista pe care vrem sa o construim cu epsilon
    drum=[int(S[0])]
    lista_sir=['e']
    #vom lua pe rand fiecare simbol din sir
    #aceasta formula calculeaza la al catelea element din matruce am ajuns len(Q)*int(drum[-1])+E.index(simbol)
    #len(Q) este nr de linii
    #int(drum[-1]) reprezinta ultima stare din drum
    #E.index(simbol) reprezinta numarul coloanei
    #de exemplu aceasta formula va da pentru elementul de pe linia 3 coloana 2 valoarea 5
    #este a 5 a valoare din matrice intrucat incepem de la 0

    for simbol in sir:
        #verificam daca al treilea element din primul 3-tuplu corespunzator starii si inputului
        #curent se afla in lista sirului pe care o construim
        if lista_LA[len(Q)*int(drum[-1])+E.index(simbol)] in lista_sir:
            #daca elementul corespunzator starii si inputului din lista
            #care aduce modificari listei pe care o construim pentru sir
            #care se afla pe prima pozitie adica [0](trebuie scos)
            #este diferit de epsilon si e in lista sirului il scoatem din lista
            if modif_lista[len(Q)*int(drum[-1])+E.index(simbol)][0]!='e' and modif_lista[len(Q)*int(drum[-1])+E.index(simbol)][0] in lista_sir:
                lista_sir.remove(modif_lista[len(Q)*int(drum[-1])+E.index(simbol)][0])
            #daca elementul corespunzator starii si inputului din lista care aduce
            #modificari listei pe care o construim pentru sir
            # care se afla pe a doua pozitie adica [1](trebuie adaugat)
            # este diferit de epsilon si nu e inca in lista sirului il vom adauga in lista
            if modif_lista[len(Q)*int(drum[-1])+E.index(simbol)][1]!='e'and modif_lista[len(Q)*int(drum[-1])+E.index(simbol)][1] not in lista_sir:
                lista_sir.append(modif_lista[len(Q)*int(drum[-1])+E.index(simbol)][1])
            #la final dam append drumului starii in care am ajuns in functie de ultima stare din drum si inpuutl citit
            drum.append(matrice_LA[int(drum[-1])][E.index(simbol)][0])
        else:
            #in cazul in care nu se afla in lista curenta a sirului vom efectua aceleasi operatii
            if modif_lista[len(Q)*int(drum[-1])+E.index(simbol)][0]!='e' and modif_lista[len(Q)*int(drum[-1])+E.index(simbol)][0] in lista_sir:
                lista_sir.remove(modif_lista[len(Q)*int(drum[-1])+E.index(simbol)][0])
            if modif_lista[len(Q)*int(drum[-1])+E.index(simbol)][1]!='e'and modif_lista[len(Q)*int(drum[-1])+E.index(simbol)][1] not in lista_sir:
                lista_sir.append(modif_lista[len(Q)*int(drum[-1])+E.index(simbol)][1])
            drum.append(matrice_LA[int(drum[-1])][E.index(simbol)][0])
    return drum,lista_sir
def validare(drum,lista_sir):
    Q, E, L, F, S, T = citire(fisier)
    #verificam daca ultima valoare din drumul parcurs al stringului este una de accept
    #si daca lungimea listei construite din parcurgearea sirului are lungimea 1 si acel element este epsilon
    #adica s-a golit lista
    if str(drum[-1]) in F and len(lista_sir)==1 and lista_sir[0]=='e':
        return True
    return False

fisier=input("Dati numele fiserului: ")
afisare(fisier)
sir=input("Dati un sir de validat:")
validare_sir(sir)