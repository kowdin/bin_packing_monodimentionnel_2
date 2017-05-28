#!/bin/bash


for f in ../Instances/*/*.txt
do

    name=$(printf "$f" | grep -o -E 'Falkenauer.*')

    printf "$name\n"

done

# python3 ../code/bin_packing.py ../code/jouet2.txt > output
#
# # récupérations des valeurs dans le fichier output
#
# str=$(cat output)
#
# printf "$str\n\n"
#
# best_fit=$(printf "$str" | grep -o -E 'best fit : [-+0-9.e]+' | cut -d ':' -f2 | tr -d ' ' )
# relax_lin=$(printf "$str" | grep -o -E 'relaxation lineaire : [-+0-9.e]+' | cut -d ':' -f2 | tr -d ' ' )
# relax_lag=$(printf "$str" | grep -o -E 'relaxation lagrangienne : [-+0-9.e]+' | cut -d ':' -f2 | tr -d ' ' )
#
# printf "$best_fit\n"
# printf "$relax_lin\n"
# printf "$relax_lag\n"
#
# printf "instance;$best_fit;$relax_lin;$relax_lag" >> res.txt
