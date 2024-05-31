"""Popeanga Antonia-Maria
   Popa Jasmine
   Grupa 141"""

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
def citeste_comanda(camera,denumire_camere):
    #spunem utilizatorului unde este si il intrebam ce comanda doreste sa execute
    print()
    print('Vă aflați în camera',denumire_camere[camera])
    print('Alegeți ce vreți să faceți în continuare, menționând cifra corespunzătoare acțiunii:')
    print('0 - go [room]')
    print('1 - look')
    print('2 - inventory')
    print('3 - take [item]')
    print('4 - drop [item]')
    comanda=input().strip()
    #dupa ce am citit comanda o returnam in prgramul principal pentru a o executa
    return comanda
def gestionare_comanda(comanda,camera_curenta,fisier,inventar_jucator,denumire_camere,inventar_prestabilit):
    #aceasta functie se va comporta ca un meniu interactiv pentru utilizator
    #in functie de deciziile sale, analizam noile situatii create
    Q, E, L, F, S, T = citire(fisier)
    descrieri_camere=['The grand foyer of the Castle of Illusions.','A room with a large table filled with an everlasting feast.',
                      'A room packed with peculiar ingredients.','A chamber filled with antiquated weapons and armour.',
                      'A glittering room overflowing with gold and gemstones.','A vast repository of ancient and enchanted texts.',
                      'A storage area for the Kitchen.','The command center of the castle.','A room teeming with mystical artifacts.',
                      'The hidden passage that leads out of the Castle of Illusions.']
    #luam pe rand fiecare comanda posibila
    if comanda=='0':
        print('În ce cameră vrei să te duci?')
        print('0 : Entrance Hall')
        print('1 : Dining Room')
        print('2 : Kitchen')
        print('3 : Armoury')
        print('4 : Treasury')
        print('5 : Library')
        print('6 : Pantry')
        print('7 : Throne Room')
        print('8 : Wizards Study')
        print('9 : Secret Exit')
        #cerem utilizatorului sa aleaga in ce camera vrea sa mearga
        camera=int(input().strip())
        for t in T: #pentru fiecare tranzitie din lista de tranzitii
            t0=t[0].split() #luam partea din stanga a tranzitiei
            #verificam daca codificarea camerei in care ne aflam se afla pe pozitia corespunzatoare dintr-o tranzitie (prima pozitie din stanga adica)
            #si daca item-ul necesar trecerii in noua camera se afla in inventarul actual al jucatorului
            #si, de asemenea, daca avem aceeasi codificare a camerei alese de utilizator si pe prima pozitie din partea dreapta a tranzitiei
            if t0[0]==str(camera_curenta) and t0[-1] in inventar_jucator and t[1][0]==str(camera):
                print()
                print('Super! Ai ajuns în camera ',denumire_camere[camera])
                camera_curenta=camera #daca toate conditiile sunt respectate, suntem mutati in noua camera
                break
        else:
            print('Din păcate nu poți ajunge în camera ', denumire_camere[camera], 'din camera ',
                  denumire_camere[camera_curenta]) #daca exista vreo conditie care nu este respectata, tranzitia nu se poate face
            for t in T:
                t0 = t[0].split()
                if t0[0] == str(camera_curenta)  and t[1][0] == str(camera): #aici avertizam utilizatorul in cazul in care tranzitia sa s-ar putea face
                    print('Trebuie să iei item-ul necesar: ', t0[-1])  #daca ar avea niste item-uri in inventarul sau personal
                    break
    elif comanda=='1':
        print('Vă aflați în camera ',denumire_camere[camera_curenta],'-',descrieri_camere[camera_curenta])
        for t in T: #pentru fiecare tranzitia din lista de tranzitii
            if t[0][0]==str(camera_curenta): #afisam numele camerei curente si descrierea sa, alaturi de aceleasi info pt camerele adiacente
                print('Una dintre camerele adiacente ',denumire_camere[camera_curenta],'este ', denumire_camere[int(t[1][0])], '-',descrieri_camere[int(t[1][0])])
    elif comanda=='2':
        print('Inventarul tău conține: ')
        for elem in inventar_jucator: #afisam fiecare element din inventarul utilizatorului
            print(elem)
    elif comanda=='3': #incepem sa verificam daca exista item-uri pe care le putem lua din camera
        if len(inventar_prestabilit[camera_curenta])==0: #
            print('Nu există niciun item în această cameră.')
        else:
            print('Item-urile disponibile sunt: ', inventar_prestabilit[camera_curenta]) #daca exista, punem utilizatorul sa aleaga ce vrea sa ia
            print('Scrieți corect numele item-ului pe care vrei sa-l iei: ') #daca vrea sa ia mai multe, le va lua pe rand
            itemm=input()
            inventar_jucator.append(itemm)
            inventar_prestabilit[camera_curenta].remove(itemm)
            print('Inventarul tău actualizat este: ', inventar_jucator)  #afisam actualizarile
            print('Inventarul prestabilit acum este: ', inventar_prestabilit)
    elif comanda == '4':
        print('Inventarul tău este: ', inventar_jucator) #asemanator comenzii take, prezentam utilizatorului elementele din inventar
        print('Scrieți corect numele item-ului căruia vrei să-i dai drop: ') #si il punem sa aleaga la ce vrea sa dea drop
        itemm=input() #daca vrea sa dea drop la mai multe item-uri, o va face pe rand
        inventar_jucator.remove(itemm)
        inventar_prestabilit[camera_curenta].append(itemm)
        print('Inventarul tău actualizat este: ', inventar_jucator) #afisam actualizarile
        print('Inventarul prestabilit acum este: ', inventar_prestabilit)
    return camera_curenta, inventar_prestabilit, inventar_jucator

def verifica_gameover(camera_curenta,inventar_jucator,status_game):
    Q, E, L, F, S, T = citire(fisier)
    ok=0
    #parcurgem tranzitiile din multimea T si daca gasim o tranzitie ce porneste din camera in care se afla la momentul actual
    #verificam daca avem intemul necesar in inventar
    #daca nu reusim sa accesam nicio alta camera atunci ne aflam intr-un dead end
    #modificam statusul jocului daca nu reuism sa accesam nicio alta camera si nu suntem in stare finala atunci status_game=0
    #altfel status_game=1 si nu e game_over
    for t in T:
        t0 = t[0].split()
        if t0[0] == str(camera_curenta) and t0[-1] in inventar_jucator :
            ok=1
            break
    if ok==0 and str(camera_curenta) not in F:
        status_game=0 #gameover
        print('Ați ajuns într-un dead-end. Game over!')
    else:
        status_game=1#nu e gameover
    return status_game

def start_joc():
    Q, E, L, F, S, T = citire(fisier)
    #initial camera curenta va fi egala cu starea de start
    camera_curenta = int(S[0])
    #initial inventarul jucatorului va avea doar epsilon
    inventar_jucator = ['e']
    #fiecare pozitie reprezinta o camera
    #exemplu pozitia 0 este Entrance Hall, poz 1 este Dining Room etc
    #avem un inventar prestabilit pentru fiecare din care putem scoate si adauga item-uri
    inventar_prestabilit = [['key'], ['invitation','chefs_hat'],['spoon'],['sword','crown'],['ancient_coin'],['spell_book'],[],[],['magic_wand'],[]]
    #avem o lista cu denimiri in functie de pozitie
    denumire_camere=['Entrance Hall','Dining Room','Kitchen','Armoury','Treasury','Library','Pantry','Throne Room','Wizards Study','Secret Exit']
    #initial jocul este pornit
    status_game=1

    print()
    print("Bine ai venit în lumea magică a Castle of Illusions!")

    while status_game==1:
        #obtinem comanda de la utilizator
        comanda=citeste_comanda(camera_curenta,denumire_camere)
        #in functie de ce comanda a ales o vom gestiona separat
        camera_curenta,inventar_prestabilit,inventar_jucator=gestionare_comanda(comanda,camera_curenta,fisier,inventar_jucator,denumire_camere,inventar_prestabilit)
        #verificam daca au fost luate toate item-urile din camera in care se afla utilizatorul si daca nu este in o stare de accept
        #apelam functia de gameover pentru a vedea daca cu toate itemurile posibile pe care le are utilizatorul mai poate ajunge in vreo camera prin tranzitiile din input
        #daca nu mai poate ajunge nicaieri, statusul jocului este egal cu 0, adica s-a terminat jocul
        if len(inventar_prestabilit[camera_curenta])==0 and str(camera_curenta) not in F:
            status_game=verifica_gameover(camera_curenta,inventar_jucator,status_game)
        #verificam daca camera curenta se afla in multimea starilor de accept
        #daca suntem in stare de accept s-a aterminat jocul si utilizatorul a castigat
        if str(camera_curenta) in F:
            print('Jocul s-a terminat. Ați câștigat!')
            status_game=0
    #la final fie ca a castigat fie ca a fost gameover intrebam daca mai doreste sa se mai joace o data
    print('Doriți să mai jucați? DA sau NU?')
    raspuns=input().upper()
    #daca raspunsul este DA apelam start_joc()
    if raspuns=='DA':
        start_joc()
    else:
        print('La revedere!')
#validam fisierul LA-ului si il afisam
fisier=input('Dați numele fișierului:')
afisare(fisier)
#incepem jocul
start_joc()