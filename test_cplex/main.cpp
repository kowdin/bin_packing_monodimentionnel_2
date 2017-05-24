#include <iostream>
#include <cstdlib>

#include "Instance.hpp"

using namespace std;

int main() {

    srand(42);

    Instance instance;

    instance.charger("Falkenauer_u500_09.txt");

    // génération d'un vecteur de multiplicateurs
    int nBoite = instance.bestFit();

    cout << "bestFit: " << nBoite << endl;

    vector<double> mult(instance.nObj(), -50);
    vector<double> grad(instance.nObj(), 0);

    /*for(int j = 0; j < 100; j++) {

        for(int i = 0; i < mult.size(); i++) {
            mult.at(i) = (rand()/(double)RAND_MAX)*0.2;
        }
        cout << "relaxation lagrangienne: " << instance.relaxLag(nBoite, mult, grad) << endl;
        cout << endl;
    }*/

    /*double pas = 5.2;
    double rho = 0.999;
    int it = 1;
    while(rho > 1e-12) {

        cout << "relaxation lagrangienne: " << instance.relaxLag(nBoite, mult, grad) << endl;

        // mise à jour des multiplicateurs
        for(int i = 0; i < instance.nObj(); i++) {
            mult.at(i) += grad.at(i)*pas;
        }

        pas *= rho;
        rho *= rho;
        it ++;
    }*/

    double epsilon = 1.;
    double pas = 1.;
    double relax = 0.;
    double norm;

    int k = 0;
    while(pas >= 1e-4) {

        relax = instance.relaxLag(nBoite, mult, grad);
        cout << "relaxation lagrangienne: " << relax << endl;
        norm = 0;
        for(int i = 0; i < instance.nObj(); i++) {
            norm += grad.at(i);
        }

        norm *= norm;
        pas = epsilon*( (nBoite-relax)/(norm) );

        // mise à jour des multiplicateurs
        for(int i = 0; i < instance.nObj(); i++) {
            mult.at(i) += grad.at(i)*pas;
        }

        cout << "pas " << k << " : " << pas << endl;

        k ++;
    }




    return 0;
}
