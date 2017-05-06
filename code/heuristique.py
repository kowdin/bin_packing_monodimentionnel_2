from instance import Instance

def best_fit(instance):

    nb_bin = 0 # nombre de bins ouverts
    bins = list() # liste des capacités des bins en cours de remplissage

    # pour tous les types d'objets à ranger, ajout des objets du plus grand au plus petit
    for ind_obj in range(0,instance.nb_obj):

        # ajout des objets pour cette taille
        for nb in range(0,instance.obj_nb[ind_obj]):

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
                bins.append(0)
                nb_bin += 1

    return nb_bin
