#include "Instance.hpp"

#include <fstream>
#include <iostream>
#include <algorithm>

#define IL_STD

#include <ilcplex/ilocplex.h>

using namespace std;

Instance::Instance() {


}

void Instance::charger(string chemin) {

    ifstream fichier(chemin);

    if(fichier) {

        // nb obj
        fichier >> _nbObj;

        // nb boîtes
        fichier >> _tailleBin;

        _occObj.push_back(1);

        int taille;
        fichier >> taille;
        _obj.push_back(taille);

        for(int i = 1; i <= _nbObj-1; i++) {
            fichier >> taille;
            if(taille == _obj.back()) {
                _occObj.back() ++;
            } else {
                _obj.push_back(taille);
                _occObj.push_back(1);
            }
        }

        fichier.close();
    }
}

void Instance::afficher() {

    cout << "taille bins: " << _tailleBin << endl;
    cout << "objets: " << endl << endl;
    for(int i = 0; i < _obj.size(); i++) {
        cout << _obj.at(i) << " : " << _occObj.at(i) << endl;
    }

}

int Instance::bestFit() {

    vector<int> capaBin;

    for(int i = 0; i < _obj.size(); i++) {

        for(int j = 0; j < _occObj.at(i); j++) {

            // tri des bins
            sort(capaBin.begin(), capaBin.end(), [] (int& gch, int& dte) { return gch > dte; });

            int k = 0;
            bool trouve = false;
            while(!trouve && k < capaBin.size()) {
                if(capaBin.at(k) + _obj.at(i) <= _tailleBin) {
                    capaBin.at(k) += _obj.at(i);
                    trouve = true;
                } else {
                    k ++;
                }
            }

            // ouverture d'un nouveau bin
            if(!trouve) {
                capaBin.push_back(_obj.at(i));
            }

        }

    }

    return capaBin.size();
}

int Instance::nObj() {
    return _nbObj;
}


double Instance::relaxLag(int nBoite, vector<double>& mult, vector<double>& gradLG) {

    double sumLambda = 0;
    for(int i = 0; i < mult.size(); i++) {
        sumLambda += mult.at(i);
    }

    // résolution du problème de sac à dos
    IloEnv env;
    IloModel model(env);
    vector<IloBoolVar*> _var(_nbObj, nullptr);

    for(int i = 0; i < _nbObj; i++) {
        _var.at(i) = new IloBoolVar(env);
    }

    // fonction objectif
    IloExpr sumObj(env);
    for(int i = 0; i < _nbObj; i++) {
        sumObj += mult.at(i)* *_var.at(i);
    }
    model.add(IloMaximize(env, sumObj));

    // contrainte
    IloExpr sumCt(env);
    int indObj = 0;
    for(int i = 0; i < _obj.size(); i++) {
        for(int j = 0; j < _occObj.at(i); j++) {
            sumCt += *_var.at(indObj)*_obj.at(i);
            indObj ++;
        }
    }
    model.add(sumCt <= _tailleBin);

    // résolution
    double resCPX = 0;
    IloCplex cplex(model);
    cplex.setOut(env.getNullStream());
    cplex.setWarning(env.getNullStream());
    cplex.solve();
    if (cplex.getStatus() == IloAlgorithm::Infeasible) {
        env.out() << "Pas de solution" << endl;
    } else {
        resCPX = cplex.getObjValue();
    }

    // calcul du gradient lagrangien
    for(int i = 0; i < _nbObj; i++) {
        gradLG.at(i) = 1.-cplex.getValue(*_var.at(i))*nBoite;
    }

    /*cout << "valeurs variables cplex: " << endl;
    for(int i = 0; i < _nbObj; i++) {
        cout << cplex.getValue(*_var.at(i)) << " ; ";
    }
    cout << endl;*/

    for(int i = 0; i < _nbObj; i++) {
        delete _var.at(i);
    }

    // cout << "resCPX: " << resCPX << endl;

    if(resCPX >= 1.) {
        return sumLambda+(1.-resCPX)*nBoite;
    } else {
        return sumLambda;
    }
}
