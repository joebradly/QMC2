#ifndef ORBITALSFACTORY_H
#define ORBITALSFACTORY_H

#include "Orbitals.h"

#include "../structs.h"

#include "ExpandedBasis/ExpandedBasis.h"
#include "Gaussians/oxygen3-21G/oxygen3_21g.h"

enum FACTORYTYPE {EXPANDED,
                  OXYGEN3_21G};


class OrbitalsFactory {
public:
    OrbitalsFactory(FACTORYTYPE type) :
        type(type)
    {

    }

    Orbitals* create(GeneralParams & gP, VariationalParams & vP) {

        Orbitals* basis;

        switch (type) {
        case EXPANDED:
        {
            ExpandedBasis* expbasis = new ExpandedBasis(gP);
            expbasis->setBasis(basisForExpanded->create(gP, vP));
            expbasis->setCoeffs(C);

            basis = expbasis;

            break;
        }
        case OXYGEN3_21G:
        {
            basis = new Oxygen3_21G();

            break;
        }
        default:
            std::cout << "UNREGISTERED ORBITAL MET" << std::endl;
            break;
        }

        return basis;
    }

    FACTORYTYPE type;

    OrbitalsFactory* basisForExpanded;
    arma::mat C;

};

#endif // ORBITALSFACTORY_H