/* 
 * File:   Blocking.h
 * Author: jorgmeister
 *
 * Created on October 29, 2012, 3:58 PM
 */

#ifndef BLOCKING_H
#define	BLOCKING_H

class Blocking : public ErrorEstimator {
public:
    Blocking(int n_c, ParParams & pp,
            std::string filename = "blocking_out",
            std::string path = "./",
            int n_b = 100,
            int maxb = 10000,
            int minb = 10,
            bool rerun = false);

    Blocking(int n_c, 
            std::string filename = "blocking_out",
            std::string path = "./",
            int n_b = 100,
            int maxb = 10000,
            int minb = 10);

    double estimate_error();
    
    void get_initial_error();

protected:

    arma::rowvec local_block;

    int min_block_size;
    int max_block_size;
    int n_block_samples;

    void block_data(int block_size, double &var, double &mean);

};

#endif	/* BLOCKING_H */

