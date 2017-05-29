#!/bin/bash

# for f in ../Instances/*/*.txt
for f in ../Instances/c150/*.txt
do

    nom=$(printf "$f" | grep -o -E 'Falkenauer.*')

    printf "$nom\n"

    python3 ../code/bin_packing.py $f > output2

    # récupérations des valeurs dans le fichier output

    str=$(cat output2)

    printf "$str\n\n"

    best_fit=$(printf "$str" | grep -o -E 'best fit : [-+0-9.e]+' | cut -d ':' -f2 | tr -d ' ' )
    relax_lin=$(printf "$str" | grep -o -E 'relaxation lineaire : [-+0-9.e]+' | cut -d ':' -f2 | tr -d ' ' )
    relax_lag=$(printf "$str" | grep -o -E 'relaxation lagrangienne : [-+0-9.e]+' | cut -d ':' -f2 | tr -d ' ' )
    recons=$(printf "$str" | grep -o -E 'reconstruction : [-+0-9.e]+' | cut -d ':' -f2 | tr -d ' ' )
    temps=$(printf "$str" | grep -o -E 'temps : [-+0-9.e]+' | cut -d ':' -f2 | tr -d ' ' )

    printf "$nom;$best_fit;$recons;$relax_lin;$relax_lag;$temps\n" >> res2.txt

done
