
# -*- coding: utf-8 -*-

import sys, re, os, inspect

try:
    import numpy
except:
    print "\n"
    print "You need numpy in order to run this library!"
    print "sudo apt-get install python-numpy-dev"
    print "\n" 
    sys.exit(1)

from matplotlib import rc, pylab, colors, ticker, cm
from mpl_toolkits.mplot3d import Axes3D

#~ Paths include
classes_thisDir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
sys.path.append(classes_thisDir)

from DCViz_sup import DCVizPlotter, dataGenerator

try:
    rc('text', usetex=True)
    rc('font', family='serif')
    pylab.title("$\LaTeX$")
    pylab.draw()
    pylab.clf()
    
except:
    print "Neccessary latex packages not installed. Disabling latex support."
    rc('text', usetex=False)   



class myTestClass(DCVizPlotter):
    nametag =  'testcase\d\.dat' #filename with regex support
    
    #1 figure with 1 subfigure
    figMap = {'fig1': ['subfig1']}
    
    #skip first row. (the function __str__ is printed here)
    skipRows = 1    
    
    def plot(self, data):
        column1 = data[0]

        self.subfig1.set_title('I have $\LaTeX$ support!')
              
        self.subfig1.set_ylim([-1,1])
          
        self.subfig1.plot(column1)
  

class myTestClassFamily(DCVizPlotter):
    nametag =  'testcaseFamily\d\.dat' #filename with regex support
    
    #1 figure with 3 subfigures
    figMap = {'fig1': ['subfig1', 'subfig2', 'subfig3']}
    
    #skip first row. (the function __str__ is printed here)
    skipRows = 1    

    #Using this flag will read all the files matching the nametag
    #(in the same folder.) and make them aviable in the data arg    
    isFamilyMember = True
    familyName = "testcase"
    
    def plot(self, data):
        
        #figures[0] is 'fig1' figures. the 0'th element is the
        #self.fig1 itself. Subfigures are always index [1:]
        mainFig = self.figures[0][0]  
        mainFig.suptitle('I have $\LaTeX$ support!')        
        subfigs = self.figures[0][1:]
    
        #Notice we plot fileData.data and not fileData alone.
        #The dataGenerator class is used to speed up file reading;
        #looping over family members and directly plotting means
        #we send a dataGenerator instance to matplotlib.
        #in order to get the numpy object, we send the data.
        #Alternatively, we could send data[:]
        for subfig, fileData in zip(subfigs, data):
            subfig.plot(fileData.data)
            subfig.set_ylim([-1,1])
        

class EnergyTrail(DCVizPlotter):
    
    nametag = "\w+.trailingE.arma"
    
    armaBin=True
    isFamilyMember=True
    
    figMap = {"fig1": ['eFig']}
    c = ["#C0C0C0", '#008000', '#008000'] 
    l = ["-", "--", "-"]
    
    def plot(self, data):

        eDMC = 65.7
        
        for i, data_ in enumerate(data):
            name = self.familyFileNames[i].split(".")[0].replace("_", " ")[1:]
            self.eFig.plot(numpy.cumsum(data_.data)/numpy.linspace(1,data_.m,data_.m),
                           self.l[i], c=self.c[i], label=name)
                           
        self.eFig.plot([1,data_.m], [eDMC, eDMC], 'k-.', label="DMC Energy")
        self.eFig.legend()
        
        self.eFig.set_xlabel('Cycle')
        self.eFig.set_ylabel(r'$\langle E\rangle $', rotation=0)
        
        self.eFig.axes.get_yaxis().get_label().set_fontsize(20)
        self.eFig.axes.get_xaxis().get_label().set_fontsize(20)

        formatter = ticker.ScalarFormatter(useOffset=True)
        formatter.set_scientific(True)
        formatter.set_powerlimits((-3, 2))
        self.eFig.axes.get_xaxis().set_major_formatter(formatter)


class Blocking(DCVizPlotter):
    
    nametag = "blocking_\w+_out\d*\.dat"
    figMap = {"Fig": ["blockFig"]}
    
    nameMap = {"0": r"$\alpha$", "1": r"$\beta$", "": ""}
    
    def plot(self, data):
        
        Fig, blockFig = self.Fig, self.blockFig
        blockSize, error = data
        
#        fileName = os.path.basename(self.filepath)
#        title = "Blocking data %s" % (fileName.split("_")[1] + " %s" % \
#              (self.nameMap[re.findall("blocking_\w+_out(\d*)\.dat", self.filepath)[0]]))
        blockFig.plot(blockSize, error, 
                      '*', color='#008000', markersize=10)  
        
        formatter = ticker.ScalarFormatter(useOffset=True)
        formatter.set_scientific(True)
        formatter.set_powerlimits((-3, 4))
        blockFig.axes.get_yaxis().set_major_formatter(formatter)
        blockFig.axes.get_yaxis().get_label().set_fontsize(30)
        blockFig.axes.get_yaxis().offsetText.set_size(20)
        blockFig.axes.get_xaxis().get_label().set_fontsize(20)

        
#        blockFig.set_title(title)
        blockFig.set_xlabel(r'Block size')
        blockFig.set_ylabel(r'$\sigma$', rotation=0)
        

class DMC_OUT(DCVizPlotter):
    
    nametag = "DMC_out\.dat"
    figMap = {"Fig": ["N_plot"], "Fig2": ["E_plot"]}
    dt = 0.001
        
        
    def plot(self, data):
        
        E, Eavg, N, Navg, ET = data
        
        t = numpy.linspace(0, self.dt*(len(E) - 1), len(E))
        N_plot, E_plot = self.N_plot, self.E_plot
        
        lw=2
        
        # E PLOTS
        E_plot.plot(t, E, 'k--', label="dmc E", linewidth=lw)
        E_plot.plot(t, ET, color="#008000", label="trial E", aa=True
        )
        
        E_plot.legend()
#        E_plot.set_title('Energy convergeance')
        E_plot.set_xlabel(r'$\tau = n*\delta \tau$ [s]')
        E_plot.set_ylabel(r'E [Ha]')
        E_plot.ticklabel_format(useOffset=False, axis='y')
        
        E_plot.axes.get_yaxis().get_label().set_fontsize(20)
        E_plot.axes.get_xaxis().get_label().set_fontsize(20)
        
        # N PLOTS
        N_plot.plot(t, N, '#008000')
        N_plot.plot(t, Navg, 'k--', linewidth=lw)
        
        N_plot.set_ylabel(r"N_W($\tau$)")
        N_plot.axes.get_xaxis().set_visible(False)
#        N_plot.set_title('Walker population')
        N_plot.ticklabel_format(useOffset=False, axis='y')
        
        N_plot.axes.get_yaxis().get_label().set_fontsize(20)

class radial_out(DCVizPlotter):
    
    nametag = "radial_out.+\.arma"
    figMap = {"fig1": ["radialFig"]}
    
    armaBin = True
    isFamilyMember=True
    
    def plot(self, data):
             
        cut=0
        xScale = 0.75
        print data[0].n
        
        color = ['#008000', "0.5", "k", '#008000']
        style = ['-', '-.', '--', '.']
        max_edge = 0   
        maxCut = 0
        j = 0
        
        path, name = os.path.split(self.filepath)
        
        try:
            yFile = open(os.path.join(path, "yMin.dat"), 'r')
            yMax = float(yFile.read())
        except:
            yMax = None
        
        vmc=None
        dmc=None
        
        pureOnly = False
        superPose = False
        
        proj = "yz"
        
        data2 = []    
        for i in range(len(data)):
            if proj in self.familyFileNames[i]:
                data2.append(data[i])
        data = data2
        
        if proj == "":
            proj = "xy"
            
        
        if superPose:
            yMax = 1.2

        for i in range(len(data)):
            
            if superPose:
                edge = 1
            else:
                edge = float(re.findall("edge(\d+\.?\d*)\.arma", self.familyFileNames[i])[0])
            
            if edge > max_edge:
                max_edge = edge;
            
            if "dmc" in self.familyFileNames[i]:
                method = "dmc"
                dmc = data[i].data

                if superPose:
                    dmc = dmc/dmc[cut:].max()
                
                last = dmc
                
            elif "vmc" in self.familyFileNames[i]:
                method = "vmc"
                vmc = data[i].data

                if superPose:
                    vmc = vmc/vmc[cut:].max()
                
                last = vmc
                
  
            r = numpy.linspace(0, edge, data[i].n)
            
            if r[cut] > maxCut:
                maxCut = r[cut]            
            
            if not pureOnly:
                self.radialFig.plot(r, last, style[i%2], label=method.upper(), color=color[i%2]);
           
            if vmc is not None and dmc is not None:
                if pureOnly:
                    pureC = color[j%len(color)]
                    pureS = style[j%len(color)]
                    j += 1
                    pLabel=None

                    if superPose:
                        pLabel = re.findall("out_(.+?)[vd]mc", self.familyFileNames[i])[0]
                        pLabel = re.sub("(\d)c(\d)", "\g<1> \g<2>", pLabel)
                        pLabel = re.sub("QDots\d+", "", pLabel)
                    
                else:
                    pureC = 'k'
                    pureS = "--"
                    pLabel= "Pure"
                    
                pure = 2*dmc - vmc

                if superPose:
                    pure = pure/pure[cut:].max()
                
                self.radialFig.plot(r, pure, pureS, color=pureC, label=pLabel)
                vmc = None
                dmc = None
        
#        if not pureOnly:
        self.radialFig.legend()    
        self.radialFig.axes.set_xlim(maxCut, xScale*max_edge)
        self.radialFig.set_xlabel('$r = \sqrt(%s^2 + %s^2)$' % (proj[0], proj[1]))
        self.radialFig.set_ylabel(r'$\rho(r)$')
#        locator = self.radialFig.axes.get_yaxis().get_major_locator()
#        self.radialFig.axes.set_ylim(locator.autoscale()/2)
        if yMax is not None:
            self.radialFig.set_ylim(0, yMax)
        self.radialFig.axes.set_ybound(0)
        
        self.radialFig.axes.get_yaxis().get_label().set_fontsize(30)
        self.radialFig.axes.get_xaxis().get_label().set_fontsize(30)
        
        

class dist_out(DCVizPlotter):
    
    nametag = "dist_out.+\.arma"
#    figMap = {"fig1": ["subfig0", "subfig1"]}
    figMap = {"fig_xy": [], "fig_xz": [], "fig_yz": [], 
              "s_fig_xy": ["subfig_xy"], 
              "s_fig_xz": ["subfig_xz"], 
              "s_fig_yz": ["subfig_yz"]}

    armaBin = True
    isFamilyMember = True
        
    stack = "H"
    
    dmcOnly = False
    vmcOnly = False
    
    def plot(self, data):

        PROJ = []        
        for proj in ["xy", "xz", "yz"]:
            for name in self.familyFileNames:
                if proj in name and proj not in PROJ:
                    PROJ.append(proj)
        
        oldData = False
        if len(PROJ) == 0:
            print "Assuming old xy data"
            PROJ = "xy"
            oldData = True
        
        figures = []
        for proj in ["xy", "xz", "yz"]:
                if proj in PROJ:
                    print "running proj: ", proj
                    self.plot_proj(data, proj, oldData)
                    figures.append([eval("self.fig_%s" % proj)])
                    figures.append([eval("self.s_fig_%s" % proj)])
                else:
                    print "Skipping proj: ", proj 
                    
        self.figures = figures
        
    def plot_proj(self, all_data, proj, oldData=False):
        
        
        data = []    
        
        if oldData:
            proj = ""
            
        for i in range(len(all_data)):
            if proj in self.familyFileNames[i]:
                data.append(all_data[i])

        if oldData:
            proj = "xy"

        fig1 = eval("self.fig_%s" % proj)
        subfig1 = eval("self.subfig_%s" % proj)

#        self.fig1.set_size_inches(self.fig1.get_size_inches()*numpy.array([2, 1]), forward=True)        
        
        edge = float(re.findall("_edge(.+?)\.arma", self.familyFileNames[0])[0])    
    
        if len(data) == 1:
            print "length 1 data"
            dist = data[0].data
        elif len(data) == 2:
            print "len2 data"
            edge_2 = float(re.findall("_edge(.+?)\.arma", self.familyFileNames[1])[0])
        
            if edge != edge_2:
                print "Bin edges does not match. %s != %s" % (edge, edge_2)
                self.dmcOnly = True
            
            for i in range(2):
                if "vmc" in self.familyFileNames[i]:
                    vmcDist = data[i].data
                elif "dmc" in self.familyFileNames[i]:
                    dmcDist = data[i].data
            
#            try:
            if self.dmcOnly:
                dist = dmcDist
            elif self.vmcOnly:
                dist = vmcDist
            else:
                try:
                    dist = 2*dmcDist - vmcDist
                    print "pure success!", dmcDist.sum()*(edge/100)**2, vmcDist.sum()*(edge/100)**2 
                except:
                    raise Exception("Supplied dist files does not match a VMC+DMC pair.")
        else:
            raise Exception("More than two distributions loaded in given folder.")
        
        
        origLen = len(dist)
        distMid = dist[origLen/2, :]
        crit = numpy.where(distMid > 0.1*distMid.max())[0]

        x, y = numpy.meshgrid(crit, crit)
        dist = dist[x, y]
        
        ax = Axes3D(fig1)#, self.subfig0.get_position())
        
        r = numpy.linspace(-edge, edge, origLen)
        
        X, Y = numpy.meshgrid(r, r)
        X = X[x, y]
        Y = Y[x, y]
        C = cm.Greens

        ax.plot_surface(X, Y, dist, rstride=1, cstride=1, cmap=C, linewidth=0)

        cset = ax.contour(X, Y, dist, zdir='x', offset=ax.get_xlim()[0]*1.05, color='#008000', levels=[0])        
        
        ax.set_zlim(0, dist.max())

        ax.set_ylabel(proj[0])
        ax.set_xlabel(proj[1])
        ax.view_init(30, -65)
#        ax.view_init(0, 90)
        
#        print dist.shape
#        dist = zoom(dist, 3)
#        extent = [-newEdge, newEdge, -newEdge, newEdge]
        subfig1.axes.contourf(X, Y, dist, zdir='z', cmap=C)
        subfig1.set_xlabel(proj[0])
        subfig1.set_ylabel(proj[1], rotation=0)
        subfig1.axes.get_yaxis().get_label().set_fontsize(20)
        subfig1.axes.get_xaxis().get_label().set_fontsize(20)
        
#        self.subfig0.axes.get_xaxis().set_visible(False)
#        self.subfig0.axes.get_yaxis().set_visible(False)
        
        
#        self.subfigHist3D.set_ylabel(r'y')
#        self.subfigHist3D.set_xlabel(r'x')
#        self.fig1.colorbar(im)

#        self.subfigDist1d.set_ylabel(r'$|P(r)|^2$')


class E_vs_w(DCVizPlotter):
    
    stack = "H"    
    
    nametag = "E\_vs\_w\.dat"
    figMap = {"f2":["s2", "se2"], 
              "f6":["s6", "se6"], 
            "f12":["s12", "se12"], 
            "f20":["s20", "se20"], 
            "f30":["s30", "se30"], 
            "f42":["s42", "se42"]}
 
    def plot(self, data):
        
        N, W, E, E_K, E_O, E_C = data
        
        I = {"2": [-1, -1], "6": [-1, -1], "12": [-1, -1], "20": [-1, -1], "30": [-1, -1], "42": [-1, -1]}
        
        k = 0
        for n_p in N:
            i = str(int(n_p))
            if I[i][0] == -1:
                I[i][0] = k
           
            I[i][1] = k
            
            k+=1
         
        for N in ["2", "6", "12", "20", "30", "42"]:
            i1 = I[N][0]
            i2 = I[N][1]+1

            w = W[i1:i2][numpy.where(E[i1:i2] < 1000)]
            e = E[i1:i2][numpy.where(E[i1:i2] < 1000)]
            ek =E_K[i1:i2][numpy.where(E[i1:i2] < 1000)]
            eo = E_O[i1:i2][numpy.where(E[i1:i2] < 1000)]
            ec = E_C[i1:i2][numpy.where(E[i1:i2] < 1000)]

            subfig = eval("self.s%s" % N)
            subfig2 = eval("self.se%s" % N)

            subfig.plot(w, ek/e, "*", color='#008000', label="Ekin/E")
            subfig.plot(w, eo/e, "^", color='#008000', label="Eosc/E")
            subfig.plot(w, ec/e, ".", color='#008000', label="Ecol/E")
            subfig.set_title("N = %s" % N)     
            subfig.legend()
            subfig.set_ylim([0, 1])
            subfig.set_ylabel("$\omega$")
            
            subfig2.plot(w, e/w, "+", color='#008000', label="E/$\omega$")
            subfig2.plot(w, ek/w, "*", color='#008000', label="Ekin/$\omega$")
            subfig2.plot(w, eo/w, "^", color='#008000', label="Eosc/$\omega$")
            subfig2.plot(w, ec/w, ".", color='#008000', label="Ecol/$\omega$")
            subfig2.legend()
            subfig2.axes.set_ybound(0)
            subfig.set_ylabel("$\omega$")
 
class testBinFile(DCVizPlotter):
    
    nametag = "testBin.+\.arma"
    figMap = {"fig": ["subfig"]}

    fileBin = True
    Ncols = 2
    
    skipRows = 2    

    def plot(self, data):
        x, y = data
        self.subfig.plot(x, y, '*')
        
class MIN_OUT(DCVizPlotter):
    
    nametag = "ASGD_out\.dat"
    figMap = {"E_fig"    : ["E_plot"], 
              "step_fig" : ["step_plot"],
              "param_fig": ["param_plot", "grad_plot"]}
    
    indexmap = {0: r"\alpha", 1: r"\beta"}
    l = ["-", "--"]
    c = ['#008000', 'k']    
    
    def plot(self, data):

        n_params = (self.Ncols - 3)/2

        E, Eavg, step = dataGenerator(data[:3])
        
        E_plot, step_plot, param_plot, grad_plot = self.E_plot, self.step_plot, \
                                                    self.param_plot, self.grad_plot
        
        #~ E PLOTS
        E_plot.plot(E, self.l[0], c=self.c[0], label="E")
        E_plot.plot(Eavg, self.l[1], c=self.c[1], label="average E")
        
        E_plot.legend()
        #E_plot.set_title('Energy convergeance')
        E_plot.set_xlabel(r'Cycle')
        E_plot.set_ylabel(r'E [Ha]')
        E_plot.axes.get_yaxis().get_label().set_fontsize(30)
        E_plot.axes.get_xaxis().get_label().set_fontsize(30)
        E_plot.ticklabel_format(useOffset=False, axis='y')
        
        #~ Step plot
        step_plot.plot(step, self.l[0], c=self.c[0])
        #step_plot.set_title('Step length')
        step_plot.set_xlabel('Cycle')
        step_plot.set_ylabel('Step')
        step_plot.axes.get_yaxis().get_label().set_fontsize(30)
        step_plot.axes.get_xaxis().get_label().set_fontsize(30)

        lw = 2
        #~ Param plots
        for i in range(0, 2*n_params, 2):
            param_plot.plot(data[3 + i], self.l[i/2], c=self.c[i/2],label=r'$%s$' % self.indexmap[i/2], linewidth=lw)    
            grad_plot.plot(data[4 + i], self.l[i/2], c=self.c[i/2], linewidth=lw)
        
        param_plot.set_ylabel(r'$\alpha_i$')
        #param_plot.set_title('Variational parameters')
        param_plot.axes.get_xaxis().set_visible(False)
        
        if n_params > 1:
            param_plot.legend()
        param_plot.axes.get_yaxis().get_label().set_fontsize(30)
        param_plot.axes.get_xaxis().get_label().set_fontsize(30)
        param_plot.axes.get_yaxis().labelpad = 20
        
        #grad_plot.set_title('Energy derivatives')
        grad_plot.set_ylabel(r'$\frac{\partial E}{\partial \alpha_i}$', rotation=0)
        grad_plot.set_xlabel('Cycle')
        grad_plot.axes.get_yaxis().get_label().set_fontsize(30)
        grad_plot.axes.get_xaxis().get_label().set_fontsize(30)
            
            
        
def testbedJorgen(dynamic):
    
    from pyLibQMC import paths
    path = os.path.join(paths.scratchPath, "QMC_SCRATCH")

    setting = "MIN"

    if setting == "MIN" or setting == "ALL":
        filepath = os.path.join(path, "ASGD_out.dat")
        plot_tool = MIN_OUT(filepath, dynamic)
    
        if setting == "ALL":
            print "MIN OUTPUT STARTING"
            plot_tool.mainloop()

    if setting == "DMC" or setting == "ALL":
        dt = 0.001
        filepath = os.path.join(path, "DMC_out.dat")
        plot_tool = DMC_OUT(filepath, dynamic)
        plot_tool.dt = dt
    
        if setting == "ALL":
            print "DMC OUTPUT STARTING"
            plot_tool.mainloop()

    if setting != "ALL":
        plot_tool.mainloop()
        
if __name__ == "__main__":
    print "Dynamic = FALSE"
    testbedJorgen(False)
    print "Dynamic = TRUE"
    testbedJorgen(True)
