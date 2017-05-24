from instance import Instance
from heuristique import best_fit

def relax_lagrange(instance):
# variables
	p = 0 #variable de traitement, parcour des objets
	b = 0 #variable de traitement, parcour des bin
	acc = 0 #variable de traitement
	tmp = 0 #variable de traitement
	val = 0 #variable de traitement

	n = 0 #nombre d'objet a placer
	for i in range(0,instance.nb_obj):
		n += instance.obj_nb[i]
	m = best_fit(instance) #nombre de bin maximal
	c = instance.cap #taille des bin
	x = [[0] * m for _ in range(n)] #matrice d'association objet/bin
	s = [0] * n #poid/taille des objets
	for i in range(0, instance.nb_obj):
		for j in range(0, instance.obj_nb[i]):
			s[acc] = instance.obj_taille[i]
			acc +=1
	u = [0] * m #vecteur d'ouverture des bin
	mu = [0] * m #coeficient de lagrange de la contrainte de capacite
	gamma = [0] * n #coeficient de lagrange de la contrainte tout objet
	nu_mu = 1 #taille du pas de mu
	nu_gamma = 1 #taille du pas de gamma
	epsilon_mu = 1 #facteur de reglage de la taille des pas de mu
	epsilon_gamma = 0.001 #facteur de reglage de la taille des pas de gamma
#debut
	#si tout les coeficients lagrangiens sont nul alors rien n'est ouvert/assigné
	#on a donc deja initialisé les variables comme après cette première resolution
	#calcul du score
	val = 0

	#mise a jour de la taille des pas
	acc = 0
	for b in range(0,m):
		tmp = c
		for p in range(0,n):
			tmp -= s[p]*x[p][b]
		acc += tmp*tmp
	nu_mu = epsilon_mu * (m - val)/acc


	acc = 0
	for p in range(0,n):
		tmp = 1
		for b in range(0,m):
			tmp -= x[p][b]
		acc += tmp*tmp
	nu_gamma = epsilon_gamma * (m-val)/acc

	#mise a jour des coeficient de lagrange
	for b in range(0,m):
		acc = c
		for p in range(0,n):
			acc -= s[p]*x[p][b]
		mu[b] = maxOftwo(mu[b] - nu_mu*acc, 0)

	for p in range(0,n):
		acc = 1
		for b in range(1,m):
			acc -= x[p][b]
		gamma[p] = gamma[p] - nu_gamma*acc

	print("premier reglages : ")
	print("nu_mu = "+str(nu_mu))
	print("nu_gamma = "+str(nu_gamma))
	print("mu : "+str(mu))
	print("gamma : "+str(gamma)+"\n")

	#boucle principale de descente de gradient
	while (nu_mu > 0.0001) or (nu_gamma > 0.0001):
		#resolution des sous-problèmes
		for b in range(1,m): #un problème par bin
			for p in range(1,n):
				if (mu[b]*s[p]-gamma[p] < 0):
					x[p][b] = 1
				else:
					x[p][b] = 0
			acc = 0
			for p in range(1,n):
				acc += x[p][b]*(mu[b]*s[p] - gamma[p])
			if (acc < -1):
				u[b] = 1
			else:
				u[b] = 0
				for p in range(1,n):
					x[p][b] = 0

		#calcul du score
		acc = 0
		for p in range(0, n):
			acc += gamma[p]
			for b in range(0,m):
				acc += x[p][b]*(mu[b]*s[p] - gamma[p])
		for b in range(0,m):
			acc += u[b] - mu[b]*c
		val = acc #valeur de la fonction objectif

		#mise a jour de la taille des pas
		acc = 0
		for b in range(0,m):
			tmp = c
			for p in range(0,n):
				tmp -= s[p]*x[p][b]
			acc += tmp*tmp
		nu_mu = (m - val)/acc


		acc = 0
		for p in range(0,n):
			tmp = 1
			for b in range(0,m):
				tmp -= x[p][b]
			acc += tmp*tmp
		nu_gamma = (m-val)/acc

		#mise a jour des coeficient de lagrange
		for b in range(0,m):
			acc = c
			for p in range(0,n):
				acc -= s[p]*x[p][b]
			mu[b] = maxOftwo(mu[b] - nu_mu*acc, 0)

		for p in range(0,n):
			acc = 1
			for b in range(1,m):
				acc -= x[p][b]
			gamma[p] = gamma[p] - nu_gamma*acc

		print("nu_mu = "+str(nu_mu))
		print("nu_gamma = "+str(nu_gamma))
		print("mu : "+str(mu))
		print("gamma : "+str(gamma))
		print("val = "+str(val))
		print("ouverture : "+str(u))
		print("associations : "+str(x)+"\n")

#fin
#calcul du score
	acc = 0
	for p in range(0, n):
		acc += gamma[p]
		for b in range(0,m):
			acc += x[i][j]*(mu[b]*s[p] - gamma[p])
		for b in range(0,m):
			acc += u[b] - mu[b]*c
	return acc




def maxOftwo(a,b):
	if a > b:
		return a
	else:
		return b
