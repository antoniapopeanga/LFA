def formatare_fisier(fisier, comentarii=[], Q=set(), E=list(), S=set(), F=set(), T=list()):
    input=[]
    #prima data impart fisierul in comentarii si input
    with open(fisier, "r") as f:
        linie=f.readline().strip()
        while linie!="":
            if linie[0]=='#': #daca suntem pe o linie care e comentariu, o adaugam la lista de comentarii
                comentarii.append(linie)
            else:
                input.append(linie)
            linie=f.readline().strip()
    #apoi formatez input-ul in functie de tipul continutului
    q=[]
    t=[]
    cnt = 0
    for elem in input:
        if elem != 'End' and cnt == 0 and elem != 'Sigma :':
            E.append(elem)
        elif elem != 'End' and cnt == 1 and elem != 'States :':
            q.append(elem)
        elif elem != 'End' and cnt == 2 and elem != 'Transitions :':
            t.append(elem)
        elif elem == 'End':
            cnt += 1
    #formatez Multimea Starilor = Q
    for elem in q:
        lista=elem.split(",")
        if len(lista)==1:
            Q.add(lista[0])
        elif len(lista)==2 and lista[1]=='S':
            Q.add(lista[0].rstrip())
            S.add(lista[0].rstrip())
        elif len(lista)==3 and lista[1]=='S ' and lista[2]=='F':
            Q.add(lista[0].rstrip())
            S.add(lista[0].rstrip())
            F.add(lista[0].rstrip())
        else:
            Q.add(lista[0].rstrip())
            F.add(lista[0].rstrip())
    #formatez Lista Tranzitiilor = T
    for elem in t:
        tranzitie=elem.split(", ")
        T.append(tranzitie)
def citire_din_fisier(fisier):
    comentarii = []  # lista de comentarii care se regaseste in fisierul citit, aici pot fi instructinile pt DFA/NFA
    Q = set()  # multimea starilor
    E = list()  # alfabet
    S = set()  # q0 - start
    F = set()  # multimea starilor acceptate, finish
    T = list()
    formatare_fisier(fisier,comentarii,Q,E,S,F,T)
    return comentarii,Q,E,S,F,T
def afisare(fisier):
    comentarii, Q, E, S, F, T = citire_din_fisier(fisier)
    print("Comentarii: ", comentarii)
    print("Multimea starilor este: ", Q)
    print("Alfabet: ", E)
    print("Starea initiala: ", S)
    print("Multimea starilor finale: ", F)
    print("Lista de tranzitii: ", T)
def validare_fisier(fisier):
    comentarii, Q, E, S, F, T = citire_din_fisier(fisier)
    if validare_T(fisier)==True and validare_S(fisier)==True:
        return True
    else:
        return False
def validare_S(fisier):
    comentarii, Q, E, S, F, T = citire_din_fisier(fisier)
    if len(S)==1:
        return True
    else:
        return False
def validare_T(fisier):
    comentarii, Q, E, S, F, T = citire_din_fisier(fisier)
    for i in range(len(T)):
        if (T[i][0] and T[i][2]) in Q and (T[i][1]=="epsilon" or T[i][1] in E )and len(T[i])==3:
            ok=1
        else:
            ok=0
            break
    if ok==0:
        return False
    else:
        return True
def stare_start_NFA_DFA(fisier):
    comentarii, Q, E, S, F, T = citire_din_fisier(fisier)
    inchidere=inchidere_epsilon(fisier)
    stare_start=[]
    S=list(S)
    for s in inchidere[int(S[0])]:
        stare_start.append(s)
    return stare_start
def stari_finale_NFA_DFA(fisier):
    comentarii, Q, E, S, F, T = citire_din_fisier(fisier)
    stari_finale=list(F)
    multime_stari_f=[]
    multime_stari=generare_submultimi(Q)
    for s in multime_stari:
        for f in stari_finale:
            if int(f) in s:
                multime_stari_f.append(s)
    return multime_stari_f
def functie_tranzitie(fisier):
    comentarii, Q, E, S, F, T = citire_din_fisier(fisier)

    #facem o matrice de forma stari x litere
    matrice = [[[] for x in range(len(E))] for y in range(len(Q))]
    E=list(E)

    #umplem matricea conform tabelului de tranzitie
    for i in T:
        if i[1]!="epsilon":#completam matricea doar pentru literele din alfabet fara epsilon
            matrice[int(i[0])][E.index(i[1])].append(int(i[2]))
    for i in range (len(matrice)):
        for j in range (len(matrice[0])):
            if len(matrice[i][j])==0:
                matrice[i][j].append('')#umplem spatiile goale din matrice cu sirul vid
    return matrice
def generare_submultimi(s):
    if not s:
        return [[]]

    x = s.pop()
    subsets = generare_submultimi(s)
    new_subsets = []
    for subset in subsets:
        new_subsets.append(subset)
        new_subsets.append(subset + [x])
    submultimi=[]
    for mult in new_subsets:
        l=[]
        for x in mult:
            if len(mult)!=0:
                l.append(int(x))
        submultimi.append(l)
    return submultimi
def tabel_tranzitii_NFA_DFA(fisier):
    comentarii, Q, E, S, F, T = citire_din_fisier(fisier)
    matrice = functie_tranzitie(fisier)
    submultimi=generare_submultimi(list(Q))
    a=[]
    for s in submultimi:
        if s!=[]:
            l = [s]
            for simbol in E:
                if len(s)>1:
                    lista=[]
                    for x in s:
                       lista.append(matrice[x][int(simbol)])
                    ls=[]
                    for subl in lista:
                        for x in subl:
                            if x not in ls and x!='':
                                ls.append(x)
                    l.append(ls)
                else:
                    l.append(matrice[s[0]][int(simbol)])

            a.append(l)
    return a
def validare_string(fisier,stari_curente):
    comentarii, Q, E, S, F, T = citire_din_fisier(fisier)
    if len(stari_curente)>1:
        for s in stari_curente:
            if str(s) in F:
                return True
        else:
            return False
    else:
        if str(stari_curente[0]) in F:
            return True
        else:
            return False
def inchidere_epsilon(fisier):
    comentarii, Q, E, S, F, T = citire_din_fisier(fisier)#vrem sa vedem pentru fiecare stare cu sirul vid(epsilon) in ce stari se poate ajunge
    inchidere_epsilon = [[x] for x in range(len(Q))]#initializam fiecare lista cu starile initiale
    for t in T:
        if t[1]=="epsilon":
            inchidere_epsilon[int(t[0])].append(int(t[2]))#daca gasim o tranzitie cu epsilon adauagam la inchiderea starii raspective starea in care ajunge cu epsilon
    return inchidere_epsilon
def stari_finale(fisier,stari_curente, inchidere):
    comentarii, Q, E, S, F, T = citire_din_fisier(fisier)
    stari_finale=[]
    for s in stari_curente:
        for x in inchidere[s]:
            stari_finale.append(x)#adaugam in lista starilor finale atat starile in care a ajuns automatul dar si inchiderea lor cu epsilon
    stari_finale=set(stari_finale)
    stari_finale=list(stari_finale)
    print(validare_string(fisier,stari_finale))
def parcurgere_string(fisier,cuvant):
    comentarii, Q, E, S, F, T = citire_din_fisier(fisier)
    matrice=functie_tranzitie(fisier)
    inchidere=inchidere_epsilon(fisier)
    S=list(S)
    F=list(F)
    #lista in care punem drumul cuvantului in automat
    stari_curente=[]
    for i in inchidere[int(S[0])]:
        stari_curente.append(i)#facem lista cu inchidere starii de start
    for litera in cuvant:
        urmatoarele_stari = set()#facem un set cu urmatoarele stari
        for stare in stari_curente:
            if matrice[stare][E.index(litera)]!='':#daca exista o tranzitie de la stare cu simbolul citit o adaugam in multimea urmatoarelor stari
                urmatoarele_stari.update(matrice[stare][E.index(litera)])
        stari_curente=[]
        for s in urmatoarele_stari:#parcurgem urmatoarele stari si adaugam la starile curente atat starile cat si inchiderea lor
            if s!='':
                stari_curente.append(inchidere[s])
        s_curente=[]
        for s in stari_curente:
            for x in s:
                s_curente.append(x)#parcurgem lista de liste a starilor curente si facem o singura lista cu toate elementele din stari_curente
        stari_curente=set(s_curente)#eliminam duplicatele
        stari_curente=list(stari_curente)#o facem iar lista
    stari_finale(fisier,stari_curente,inchidere)
def transformare_NFA_in_DFA(fisier):
    comentarii, Q, E, S, F, T = citire_din_fisier(fisier)
    new_stare_start = stare_start_NFA_DFA(fisier)
    functie_tranzitie = tabel_tranzitii_NFA_DFA(fisier)
    multime_stari = generare_submultimi(Q)
    stari_finale = stari_finale_NFA_DFA(fisier)
    print("Multimea starii de start a DFA-ului este: ",new_stare_start )
    print("Multimea starilor a DFA-ului este: ", multime_stari )
    print("Multimea starilor finale este: ",stari_finale )
    print("Tabelul functiei de tranzitie a DFA-ului este: ",functie_tranzitie)
fisier=input("Numele fisierului: ")
afisare(fisier)
print(validare_fisier(fisier))
functie_tranzitie(fisier)
cuvant=input("Dati un string: ")
parcurgere_string(fisier,cuvant)
transformare_NFA_in_DFA(fisier)