/* 
 * File:   Harmonic_osc.cpp
 * Author: jorgmeister
 * 
 * Created on October 12, 2012, 2:42 PM
 */


#include "Harmonic_osc.h"

#include "../../structs.h"
#include "../../Walker/Walker.h"


Harmonic_osc::Harmonic_osc(GeneralParams & gP)
: Potential(gP.n_p, gP.dim) {

    this->w = gP.systemConstant;
    name = "Oscillator";
    
}


double Harmonic_osc::get_pot_E(const Walker* walker) const {

    double e_potential = 0;

    for (int i = 0; i < n_p; i++) {
        e_potential += walker->get_r_i2(i);
    }

    return 0.5 * w * w * e_potential;
}
