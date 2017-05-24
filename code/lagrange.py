from instance import Instance
from heuristique import best_fit

def relax_lagrange(instance):
# variables
	p = 0 #variable de traitement, parcour des objets
	b = 0 #variable de traitement, parcour des bin
	acc = 0 #variable de traitement
	tmp = 0 #variable de traitement
	val = 0 #variable de traitement
	best  = -1000 #variable de retour

	n = 0 #nombre d'objet a placer
	for i in range(0,instance.nb_obj_diff):
		n += instance.obj_nb[i]
	m = best_fit(instance) #nombre de bin maximal
	c = instance.cap #taille des bin
	x = [[0] * m for _ in range(n)] #matrice d'association objet/bin
	s = [0] * n #poid/taille des objets
	for i in range(0, instance.nb_obj_diff):
		for j in range(0, instance.obj_nb[i]):
			s[acc] = instance.obj_taille[i]
			acc +=1
	u = [0] * m #vecteur d'ouverture des bin
	mu = [0.1] * m #coeficient de lagrange de la contrainte de capacite
	gamma = [0.1] * n #coeficient de lagrange de la contrainte tout objet
	nu_mu = 0.001 #taille initiale du pas de mu (pour b sinon calcule)
	nu_gamma = 10 #taille initiale du pas de gamma (pour b sinon calcule)

	#pour le choix de pas b
	#rho_nu_mu = 0.9 #facteur entre 2 taille de pas de mu
	#rho_nu_gamma = 0.9 #facteur entre 2 taille de pas de gamma
	#tmax_nu_mu = 5 #nombre de tour entre 2 reduction de nu_mu
	#tmax_nu_gamma = 5 #nombre de tour entre 2 reduction de nu_gamma
	#t_nu_mu = tmax_nu_mu #nombre de tour avant la prochaine reduction de nu_mu
	#t_nu_gamma = tmax_nu_gamma #nombre de tour avant la prochaine reduction de nu_gamma

	#pour le choix de pas c
	epsilon_nu_mu = 0.12 #facteur de reglage de la taille des pas de mu
	epsilon_nu_gamma = 0.15 #facteur de reglage de la taille des pas de gamma
#debut

	#si tout les coeficients lagrangiens sont nul alors rien n'est ouvert/assigné
	#on a donc deja initialisé les variables comme après cette première resolution
	#calcul du score
	val = 0

	#calcul de la taille des pas
	acc = 0
	for b in range(0,m):
		tmp = c
		for p in range(0,n):
			tmp -= s[p]*x[p][b]
		acc += tmp*tmp
	nu_mu = epsilon_nu_mu * (m - val)/acc

	acc = 0
	for p in range(0,n):
		tmp = 1
		for b in range(0,m):
			tmp -= x[p][b]
		acc += tmp*tmp
	nu_gamma = epsilon_nu_gamma * (m-val)/acc

	#calcul des coeficient de lagrange
	for b in range(0,m):
		acc = -c
		for p in range(0,n):
			acc += s[p]*x[p][b]
		mu[b] = maxOftwo(mu[b] + nu_mu*acc, 0)

	for p in range(0,n):
		acc = 1
		for b in range(0,m):
			acc -= x[p][b]
		gamma[p] = gamma[p] - nu_gamma*acc

	#print("premier reglages : ")
	#print("nu_mu = "+str(nu_mu))
	#print("nu_gamma = "+str(nu_gamma))
	#print("mu : "+str(mu))
	#print("gamma : "+str(gamma)+"\n")

	#boucle principale de descente de gradient
	while (nu_mu > 10**-4) or (nu_gamma > 10**-4):
		#resolution des sous-problèmes
		for b in range(0,m): #un problème par bin
			for p in range(b,n): #on commence a b pour implementer la contrainte anti symetrie
				if (mu[b]*s[p]-gamma[p] < 0):
					x[p][b] = 1
				else:
					x[p][b] = 0
			acc = 0
			for p in range(b,n):
				acc += x[p][b]*(mu[b]*s[p] - gamma[p])
			if (acc < -1):
				u[b] = 1
			else:
				for tmp in range(b,m):
					u[tmp] = 0
					for p in range(0,n):
						x[p][tmp] = 0
				break #pour une l'autre contraine de symetrie qui conserve l'independance

		#calcul du score
		acc = 0
		for p in range(0, n):
			acc += gamma[p]
			for b in range(0,m):
				acc += x[p][b]*(mu[b]*s[p] - gamma[p])
		for b in range(0,m):
			acc += u[b] - mu[b]*c
		val = acc #valeur de la fonction objectif

		if val > best:
			best = val
			#print(best)

		#mise a jour de la taille des pas
		#if t_nu_mu <= 0:
		#	nu_mu *= rho_nu_mu
		#	t_nu_mu = tmax_nu_mu
		#if t_nu_gamma <= 0:
		#	nu_gamma *= rho_nu_gamma
		#	t_nu_gamma = tmax_nu_gamma
		#t_nu_mu -=1
		#t_nu_gamma -=1
		acc = 0
		for b in range(0,m):
			tmp = c
			for p in range(0,n):
				tmp -= s[p]*x[p][b]
			acc += tmp*tmp
		nu_mu = epsilon_nu_mu * (m - val)/acc

		acc = 0
		for p in range(0,n):
			tmp = 1
			for b in range(0,m):
				tmp -= x[p][b]
			acc += tmp*tmp
		nu_gamma = epsilon_nu_gamma * (m-val)/acc


		#mise a jour des coeficient de lagrange
		for b in range(0,m):
			acc = -c
			for p in range(0,n):
				acc += s[p]*x[p][b]
			mu[b] = maxOftwo(mu[b] + nu_mu*acc, 0)

		for p in range(0,n):
			acc = 1
			for b in range(0,m):
				acc -= x[p][b]
			gamma[p] = gamma[p] + nu_gamma*acc

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
#calcul du score
	acc = 0
	for p in range(0, n):
		acc += gamma[p]
		for b in range(0,m):
			acc += x[i][j]*(mu[b]*s[p] - gamma[p])
		for b in range(0,m):
			acc += u[b] - mu[b]*c
	if acc > best:
		return acc
	else:
		return best




def maxOftwo(a,b):
	if a > b:
		return a
	else:
		return b
