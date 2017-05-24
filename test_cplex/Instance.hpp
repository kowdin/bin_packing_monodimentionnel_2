#ifndef INSTANCE_HPP
#define INSTANCE_HPP

#include <vector>
#include <string>

class Instance {

    public:
        Instance();
        void charger(std::string chemin);
        void afficher();
        int bestFit();
        double relaxLag(int nBoite, std::vector<double>& mult, std::vector<double>& gradLG);
        int nObj();

    private:
        int _tailleBin;
        int _nbObj;
        std::vector<int> _obj;
        std::vector<int> _occObj;

};

#endif
