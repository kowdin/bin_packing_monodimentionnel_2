
def poids(s, bin):
	pds = 0
	for obj in bin:
		pds = pds + s[obj]

	return pds

def reparation(instance, ouvert, sac, coef):

	s = list()

	for i in range(instance.nb_obj_diff):
		for j in range(instance.obj_nb[i]):
			s.append(instance.obj_taille[i])

	bins = list()

	objMis = [False for _ in range(instance.nb_obj_tot)]

	if(ouvert):
		tailleDict = {i : [] for i in instance.obj_taille}
		for ind, obj in enumerate(s):
			tailleDict[obj].append(ind)

		bin = [ind for ind, obj in enumerate(sac) if obj == True]

		tailleBin = {i : 0 for i in instance.obj_taille}

		for obj in bin:
			tailleBin[s[obj]] += 1

		temp = {taille: 0 for taille in instance.obj_taille}
		for obj in bin:
			temp[s[obj]] = int(len(tailleDict[s[obj]])/tailleBin[s[obj]])

		minimum = min([temp[i] for i in temp if temp[i] > 0])
		bins.append(bin)

		for obj in bin:
			objMis[obj] = True
			ind = tailleDict[s[obj]].index(obj)
			tailleDict[s[obj]].pop(ind)

		for i in range(minimum - 1):
			newBin = list()
			for obj in bin:
				o = tailleDict[s[obj]].pop(0)
				newBin.append(o)
				objMis[o] = True
			bins.append(newBin)

	objTrie = sorted(range(instance.nb_obj_tot), key=lambda k: coef[k], reverse=True)

	for obj in objTrie:
		if(not(objMis[obj])):
			for b in bins:
				if(s[obj] + poids(s, b) <= instance.cap):
					b.append(obj)
					objMis[obj] = True
					break
			if(not(objMis[obj])):
				bins.append([obj])
			objMis[obj] = True

	return bins


def reparation2(instance):

    nb_bin = 0 # nombre de bins ouverts
    bins = list() # liste des capacités des bins en cours de remplissage

    # pour tous les types d'objets à ranger, ajout des objets du plus grand au plus petit
    for ind_obj in range(instance.nb_obj_diff):

        # ajout des objets pour cette taille
        for nb in range(instance.obj_nb[ind_obj]):

            trouve = False
            ind_bin = 0

            # recherche d'un bin pouvant accueillir l'objet
            while ind_bin < nb_bin and not trouve:
                if bins[ind_bin]+instance.obj_taille[ind_obj] <= instance.cap:
                    trouve = True
                    bins[ind_bin] += instance.obj_taille[ind_obj]
                else:
                    ind_bin += 1

            # ouverture d'un nouveau bin si nécessaire
            if not trouve:
                bins.append(instance.obj_taille[ind_obj])
                nb_bin += 1

    return nb_bin
