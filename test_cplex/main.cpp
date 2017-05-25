#include <iostream>
#include <cstdlib>

#include "Instance.hpp"

using namespace std;

int main() {

    srand(42);

    Instance instance;

    // instance.charger("Falkenauer_u500_09.txt");
    instance.charger("jouet2.txt");

    // génération d'un vecteur de multiplicateurs
    int nBoite = instance.bestFit();

    cout << "bestFit: " << nBoite << endl;

    // instance.resoudreCPLEX();

    vector<double> mult(instance.nObj(), 0.24);
    /*for(int i = 0; i < mult.size(); i++) {
        mult.at(i) = mult.size()-i;
    }*/
    vector<double> grad(instance.nObj(), 0);

    cout << "relaxation lagrangienne: " << instance.relaxLag(nBoite, mult, grad) << endl;
    cout << "grad: " << grad.at(0) << endl;

    /*double pas = 0.000000005;
    double rho = 0.00001;
    int it = 1;
    while(rho > 1e-15) {

        cout << "relaxation lagrangienne: " << instance.relaxLag(nBoite, mult, grad) << endl;

        // mise à jour des multiplicateurs
        for(int i = 0; i < instance.nObj(); i++) {
            mult.at(i) += grad.at(i)*pas;
        }

        // pas *= rho;
        // rho *= rho;
        it ++;
    }*/

    /*double epsilon = 1e-10;
    double pas = 1.;
    double relax = 0.;
    double norm;

    int k = 0;
    while(pas >= 1e-16) {

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
    }*/




    return 0;
}
