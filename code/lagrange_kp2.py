from instance import Instance
from heuristique import best_fit
from knapsack import Knapsack_solver

def relax_lagrange_kp(instance):
#variable
    # sous-problèmes de sac à dos
    kp_solver = Knapsack_solver(instance)

    #variable de traitement et de retour
    best  = -1000 #variable de retour
    xbest = list() #variable de retour
    ubest = False #variable de retour
    mubest = list() #variable de retour
    somme_mult = 0 #somme des coeficient lagrangien
    acc = 0


    #variable de solution et d'instance
    n = 0 #nombre d'objet a placer
    for i in range(0,instance.nb_obj_diff):
        n += instance.obj_nb[i]
    m = best_fit(instance) #nombre de bin maximal
    c = instance.cap #taille des bin
    x = [[0] * m for _ in range(n)] #matrice d'association objet/bin
    s = [0] * n #poid/taille des objets
    for i in range(0, instance.nb_obj_diff):
        for _ in range(0, instance.obj_nb[i]):
            s[acc] = instance.obj_taille[i]
            acc +=1
    u = [0] * m #vecteur d'ouverture des bin
    val = 0 #valeur actuel de la fonction  objectif

    #parametre de calcul
    mu = [0.001] * n #coeficient de lagrange de la contrainte dualise
    nu = 1.0 #taille du pas de mu (valeur initiale pour decalration)
    omega = best_fit(instance) #cible
    omega_barre = instance.relaxation_lineaire() #valeur don on dispose actuellement
    epsilon = 0.12 #facteur de reglage de la taille des pas
    rho = 0.9 #facteur entre 2 epsilon
    tmax = 40 #nombre de tour sans amelioration entre 2 reduction de epsilon
    t = tmax #nombre de tour avant la prochaine reduction de epsilon

#debut

    #premiere resolution
    somme_mult = sum(mu)
    (kp_val, x) = kp_solver.resoudre(mu)
    if 1 < kp_val: # si le résultat est > 1, alors le bin doit être utilisé
        val = (1-kp_val)*m + somme_mult
    else:
        val = somme_mult
        for p in range(0,n): x[p] = 0

    #calcul de la taille des pas
    acc = calc_nu_acc(n,m,x)
    if 0 == acc:
        nu = 0 #contraintes verifiées a l'egalité donc pas de changement nécéssaire
    else:
        nu = epsilon * (omega - val)/acc

    while ((nu > 10**-5) or (val < omega_barre-1)) and (omega - val >= 1) and (0 != nu):
        #mise a jour des coeficient de lagrange
        mu = Majmu(n,m,x,mu,nu)

        #resolution et calcul du score
        somme_mult = sum(mu)
        (kp_val, x) = kp_solver.resoudre(mu)
        if kp_val > 1: # si le résultat est > 1, alors le bin doit être utilisé
            val = (1-kp_val)*m + somme_mult
        else:
            val = somme_mult
            for p in range(0,n): x[p] = 0

        #sauvegarde de la meilleure relaxation trouvée
        if val > best:
            best = val
            xbest = list(x)
            ubest = (kp_val > 1)
            mubest = list(mu)
            t = tmax

        #mise a jour de la taille des pas
            #diminution des facteur si pas d'amelioration
        if t<= 0:
            epsilon *= rho
            t = tmax
        t -=1
            #augmentation des facteur (comme un warm up) si ils sont trop bas (valeur mise a la valeur maximale)
        if epsilon < 10**-5:
            epsilon = 1
            #calcul des pas en fonction des facteur precedent
        acc = calc_nu_acc(n,m,x)
        if 0 == acc:
            nu = 0 #contraintes verifiées a l'egalité donc pas de changement nécéssaire
        else:
            nu = epsilon * (omega - val)/acc

        print("nu = "+str(nu))
        print("epsilon = "+str(epsilon))
        print("mu : "+str(mu))
        print("val = "+str(val))
        print("kp_val : "+str(kp_val))
        print("associations : "+str(x))
        print("\n")

#fin
    return (best,xbest,ubest,mubest)


def maxOftwo(a,b):
    if a > b:
        return a
    else:
        return b

def calc_nu_acc(n,m,x):
    acc = 0
    for p in range(0,n):
        acc += (1 - m*x[p])**2
    return acc

def Majmu(n,m,x,mu,nu):
    for p in range(0,n):
        mu[p] = maxOftwo(mu[p] + nu*(1 - m*x[p]), 0)
    return mu