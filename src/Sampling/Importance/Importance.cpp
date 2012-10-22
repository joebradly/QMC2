/* 
 * File:   Importance.cpp
 * Author: jorgmeister
 * 
 * Created on October 12, 2012, 2:43 PM
 */

#include "../../QMCheaders.h"

Importance::Importance(GeneralParams & gP)
: Sampling(gP.n_p, gP.dim) {
    diffusion = new Fokker_Planck(n_p, dim, 0, gP.random_seed, gP.D);

}

void Importance::calculate_energy_necessities_CF(Walker* walker) const {
    //CF IS has no spesific necessities
}

void Importance::copy_walker(const Walker* parent, Walker* child) const {
    child->jast_grad = parent->jast_grad;
    child->spatial_grad = parent->spatial_grad;

    //done in QMC
//    qmc->get_system_ptr()->copy_walker(parent, child);
    //    qmc->get_kinetics_ptr()->copy_walker_IS(parent, child);

    child->qforce = parent->qforce;
}

void Importance::update_necessities(const Walker* walker_pre, Walker* walker_post, int particle) {
    //    qmc->get_kinetics_ptr()->update_necessities_IS(walker_pre, walker_post, particle);

    //done in QMC
//    walker_post->spatial_ratio = qmc->get_system_ptr()->get_spatial_ratio(walker_pre, walker_post, particle);
//    qmc->get_system_ptr()->calc_for_newpos(walker_pre, walker_post, particle);

    qmc->get_gradients(walker_pre, walker_post, particle);
    qmc->get_QF(walker_post);
}

void Importance::update_walker(Walker* walker_pre, const Walker* walker_post, int particle) const {
    using namespace arma;

    //    qmc->get_kinetics_ptr()->update_walker_IS(walker_pre, walker_post, particle);

    int start = n2 * (particle >= n2);
    int end = start + n2 - 1;

    qmc->get_system_ptr()->update_walker(walker_pre, walker_post, particle);

    walker_pre->spatial_grad(span(start, end), span()) = walker_post->spatial_grad(span(start, end), span());
    walker_pre->jast_grad = walker_post->jast_grad;

    walker_pre->qforce = walker_post->qforce;

}

void Importance::reset_walker(const Walker* walker_pre, Walker* walker_post, int particle) const {
    using namespace arma;

    int start = n2 * (particle >= n2);
    int end = start + n2 - 1;

//    qmc->get_system_ptr()->reset_walker_ISCF(walker_pre, walker_post, particle);
    walker_post->spatial_grad(span(start, end), span()) = walker_pre->spatial_grad(span(start, end), span());
    walker_post->jast_grad = walker_pre->jast_grad;
    //    qmc->get_kinetics_ptr()->reset_walker_IS(walker_pre, walker_post, particle);
}

//INLINED in SAMPLING superclass
//double Importance::get_spatialjast_ratio(const Walker* walker_post, const Walker* walker_pre, int particle) const {
////    return qmc->get_kinetics_ptr()->get_spatial_ratio_IS(walker_post, walker_pre, particle);
//    return walker_post->spatial_ratio * qmc->get_jastrow_ptr()->get_j_ratio(walker_post, walker_pre, particle);
//}

//calc inverse in trial pos
void Importance::get_necessities(Walker* walker) {
    qmc->get_gradients(walker);
//    qmc->get_kinetics_ptr()->get_necessities_IS(walker);
    qmc->get_QF(walker);
}
