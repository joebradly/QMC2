/* 
 * File:   DMC.h
 * Author: jorgmeister
 *
 * Created on October 12, 2012, 2:42 PM
 */

#ifndef DMC_H
#define	DMC_H

class DMC : public QMC {
protected:

    int K; //Factor of empty space for walkers over initial walkers

    int n_w;
    int n_w_last;

    int deaths;

    int block_size;
    int samples;

    double dmc_E;
    double E_T;
    double E;

    bool dist_from_file;
    std::string dist_in_path;

    Walker **original_walkers;
    Walker *trial_walker;

    void initialize();

    virtual bool move_autherized(double A);

    void iterate_walker(int k, int n_b = 1);

    void Evolve_walker(int k, double GB);

    void bury_the_dead();

    void update_energies();

    void reset_parameters() {
        n_w_last = n_w;
        E = samples = deaths = 0;
    }

public:

    DMC(GeneralParams &, DMCparams &, SystemObjects &);

    virtual void run_method();

    virtual void user_output() const;

    friend class stdoutDMC;

};

#endif	/* DMC_H */