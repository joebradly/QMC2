# -*- coding: utf-8 -*-

import sys, re, subprocess, os
from os.path import join as pjoin
from pyLibQMC import parseCML, paths, misc

try:
    import DCVizWrapper as viz
    canViz = True
except:
    print "Displaying results not available: No DCViz installation found."
    canViz = False


def initRun(n_p, path, name, N, bin_edge, n_cores, mpiFlag, openGUI):
    exe = pjoin(paths.programPath, misc.QMC2programName)
    
    mpi = ""
    if mpiFlag:
        mpi = "mpiexec -n %d" % n_cores
    
    args = mpi.split() + [exe, "redist", n_p, path, name, N, bin_edge]

    subprocess.call(args)
    
    ending = "arma"
    if "Diatom" in name or "QDots3D" in name or "Atoms" in name:
        ending = "arma3D"

        
    outPath = "%swalker_positions/__type___out_%s_edge%s.__end__" % (path, name, bin_edge)
    dist_path = outPath.replace("__type__", "dist").replace("__end__", ending)
    radial_path = outPath.replace("__type__", "radial").replace("__end__", "arma")
    
    if not os.path.exists(dist_path):
        print dist_path
        outPath = outPath.replace("_xy", "")
        
        dist_path = outPath.replace("__type__", "dist")
        radial_path = outPath.replace("__type__", "radial")
        
        if not os.path.exists(dist_path):
            print dist_path
            print "something went wrong..."
    

    if canViz and openGUI:
        if ending != "arma3D": viz.main(dist_path, False)
        viz.main(radial_path, False)


def main():
    
    stdoutToFile, mpiFlag, openGUI, n_cores = parseCML(sys.argv)
    print "MPI Nodes: ", n_cores
    
    #path N binEdge
    if len(sys.argv) < 3 or len(sys.argv) > 6:
        print "Error in command line arguments. [rawdata, N, bin egdes ...]"
        sys.exit(1)    
        
    rawfile = sys.argv[1]

    if 'rawdata' not in rawfile:
        print "Selected file is not a distribution data file."
        sys.exit(1)
    
    N = sys.argv[2]
    bin_edge = sys.argv[3]
    
    name = re.findall("dist_rawdata_(.+).arma", rawfile)[0]
    n_p = re.findall("(\d+)c\d", name)[0]
    path = rawfile.split("walker_positions")[0]

    initRun(n_p, path, name, N, bin_edge, n_cores, mpiFlag, openGUI)

if __name__ == "__main__":
    main()

