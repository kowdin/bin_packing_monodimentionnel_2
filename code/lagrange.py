from instance import Instance
from heuristique import best_fit

def relax_lagrange(instance):
# variables
	#variable de traitement et de retour
	p = 0 #variable de traitement, parcour des objets
	b = 0 #variable de traitement, parcour des bin
	acc = 0 #variable de traitement
	tmp = 0 #variable de traitement
	val = 0 #variable de traitement
	best  = -1000 #variable de retour
	xbest = list() #variable de retour
	ubest = list() #variable de retour
	mubest = list() #variable de retour
	gammabest = list() #variable de retour

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

	#parametre de calcul
	mu = [0.1] * m #coeficient de lagrange de la contrainte de capacite
	gamma = [0.1] * n #coeficient de lagrange de la contrainte tout objet
	nu_mu = 1.0 #taille du pas de mu (valeur initiale pour decalration)
	nu_gamma = 1.0 #taille du pas de gamma (valeur initiale pour decalration)
	omega = best_fit(instance) #cible
	omega_barre = instance.relaxation_lineaire() #valeur don on dispose actuellement
	rho_nu_mu = 0.9 #facteur entre 2 epsilon_nu_mu
	rho_nu_gamma = 0.9 #facteur entre 2 epsilon_nu_gamma
	tmax_nu_mu = 20 #nombre de tour sans amelioration entre 2 reduction de epsilon_nu_mu
	tmax_nu_gamma = 20 #nombre de tour sans amelioration entre 2 reduction de epsilon_nu_gamma
	t_nu_mu = tmax_nu_mu #nombre de tour avant la prochaine reduction de epsilon_nu_mu
	t_nu_gamma = tmax_nu_gamma #nombre de tour avant la prochaine reduction de epsilon_nu_gamma
	epsilon_nu_mu = 0.3 #facteur de reglage de la taille des pas de mu
	epsilon_nu_gamma = 0.4 #facteur de reglage de la taille des pas de gamma

#debut

	#si tout les coeficients lagrangiens sont nul alors rien n'est ouvert/assigné
	#on a donc deja initialisé les variables comme après cette première resolution
	#calcul du score
	val = 0

	#calcul de la taille des pas
	acc = calc_nu_mu_acc(n,m,c,s,x)
	if 0 == acc:
		nu_mu = 0 #contrainte verifie a l'egalité donc pas de changement nécéssaire
	else:
		nu_mu = epsilon_nu_mu * (omega - val)/acc
	acc = calc_nu_gamma_acc(n,m,x)
	if 0 == acc:
		nu_gamma = 0 #contrainte verifie a l'egalité donc pas de changement nécéssaire
	else:
		nu_gamma = epsilon_nu_gamma * (omega - val)/acc

	#print("premier reglages : ")
	#print("nu_mu = "+str(nu_mu))
	#print("nu_gamma = "+str(nu_gamma))

	#boucle principale de descente de gradient
	#on s'arrete si on a converge sur une au moins aussi bonne valeur que la relaxation lineaire (sinon continuer)
	#ou si on a montré l'optimalite de notre cible (car solution entiere)
	#ou si toutes les contraintes liantes sont verifie
	while ((nu_mu > 10**-4) or (nu_gamma > 10**-4) or (val < omega_barre-1)) and (omega - val >= 1) and (0 != nu_mu or 0 != nu_gamma):
		#mise a jour des coeficient de lagrange
		mu = Majmu(n,m,c,s,x,mu,nu_mu)
		gamma = Majgamma(n,m,x,gamma,nu_gamma)

		#resolution des sous-problèmes
		for b in range(0,m): #un problème par bin
			for p in range(b,n): #on commence a b pour implementer la contrainte anti symetrie
				if (mu[b]*s[p]-gamma[p] < 0): #test si cet objet est interessant pour ce bin
					x[p][b] = 1
				else:
					x[p][b] = 0
			acc = 0
			for p in range(b,n): #calcul de la valeur des objets interessant pour ce bin
				acc += x[p][b]*(mu[b]*s[p] - gamma[p])
			if (acc < -1): #bin interessant donc on ouvre
				u[b] = 1
			else: #il ne l'est pas donc on ne le prend pas (donc par symetrie on ne prend pas les suivants)
				for tmp in range(b,m):
					u[tmp] = 0
					for p in range(tmp,n):
						x[p][tmp] = 0
				break #pour une l'autre contraine de symetrie qui conserve l'independance

		#calcul du score
		val = score(n, m, s, c, mu, gamma, u, x)

		#sauvegarde de la meilleure relaxation trouvée
		if val > best:
			best = val
			xbest = list(x)
			ubest = list(u)
			mubest = list(mu)
			gammabest = list(gamma)
			t_nu_mu = tmax_nu_mu
			t_nu_gamma = tmax_nu_gamma

		#mise a jour de la taille des pas
			#diminution des facteur si pas d'amelioration
		if t_nu_mu <= 0:
			epsilon_nu_mu *= rho_nu_mu
			t_nu_mu = tmax_nu_mu
		if t_nu_gamma <= 0:
			epsilon_nu_gamma *= rho_nu_gamma
			t_nu_gamma = tmax_nu_gamma
			#augmentation des facteur (comme un warm up) si ils sont trop bas (valeur mise a la valeur utilise sans la reduction)
		if epsilon_nu_mu < 0.005:
			epsilon_nu_mu = 0.12
		if epsilon_nu_gamma < 0.005:
			epsilon_nu_gamma = 0.15
		t_nu_mu -=1
		t_nu_gamma -=1
		acc = calc_nu_mu_acc(n,m,c,s,x)
		if 0 == acc:
			nu_mu = 0 #contrainte verifie a l'egalité donc pas de changement nécéssaire
		else:
			nu_mu = epsilon_nu_mu * (omega - val)/acc
		acc = calc_nu_gamma_acc(n,m,x)
		if 0 == acc:
			nu_gamma = 0 #contrainte verifie a l'egalité donc pas de changement nécéssaire
		else:
			nu_gamma = epsilon_nu_gamma * (omega - val)/acc

		#print("nu_mu = "+str(nu_mu))
		#print("nu_gamma = "+str(nu_gamma))
		#print("mu : "+str(mu))
		#print("gamma : "+str(gamma))
		#print("val = "+str(val))
		#print("ouverture : "+str(u))
		#print("associations : ")
		#for p in range(0,n):
		#	print(x[p])
		#print("\n")

#fin
	return (best,xbest,ubest,mubest,gammabest)




def maxOftwo(a,b):
	if a > b:
		return a
	else:
		return b

def minOftwo(a,b):
	if a < b:
		return a
	else:
		return b

def score(n, m, s, c, mu, gamma, u, x):
	acc = 0
	for p in range(0, n):
		acc += gamma[p]
		for b in range(0,minOftwo(p+1,m)):
			acc += x[p][b]*(mu[b]*s[p] - gamma[p])
	for b in range(0,m):
		acc += u[b] - mu[b]*c
	return acc

def calc_nu_mu_acc(n,m,c,s,x):
	acc = 0
	for b in range(0,m):
		tmp = c
		for p in range(b,n):
			tmp -= s[p]*x[p][b]
		acc += tmp*tmp
	return acc

def calc_nu_gamma_acc(n,m,x):
	acc = 0
	for p in range(0,n):
		tmp = 1
		for b in range(0,minOftwo(p+1,m)):
			tmp -= x[p][b]
		acc += tmp*tmp
	return acc

def Majmu(n,m,c,s,x,mu,nu_mu):
	for b in range(0,m):
		acc = -c
		for p in range(b,n):
			acc += s[p]*x[p][b]
		mu[b] = maxOftwo(mu[b] + nu_mu*acc, 0)
	return mu

def Majgamma(n,m,x,gamma,nu_gamma):
	for p in range(0,n):
		acc = 1
		for b in range(0,minOftwo(p+1,m)):
			acc -= x[p][b]
		gamma[p] = gamma[p] + nu_gamma*acc
	return gamma
