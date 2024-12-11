# Lines beginning with "#" are comments in python.
# Start your program by importing Root and some other handy modules
import ROOT 
import math
import sys
import os
import os.path

# The argparse module makes it easy to write user-friendly command-line interfaces. 
import argparse



# we add the flags -f and -n to the scripts, so we can pass arguments in the command line:
# e.g.   python eventloop.py -f someFile.root -n 10
parser = argparse.ArgumentParser(description='Analysis of Z events.')
parser.add_argument('-f', metavar='inputFile', type=str, nargs=1, help='Input ROOT file', required=True)
parser.add_argument('-n', metavar='numEvents', type=int, nargs=1, help='Number of events to process (default all)')

args = parser.parse_args()
fileName = str(args.f[0])
numEvents = -1
if args.n != None :
    numEvents = int(args.n[0])

# from now on, fileName contains the string with the path to our input file and 
# numEvents the integer of events we want to process



# Some ROOT global settings and styling
ROOT.TH1.SetDefaultSumw2()

# The execution starts here
print("Starting the analysis")

# Open the input file. The name can be hardcoded, or given from commandline as argument
myfile = None
if os.path.isfile(fileName) and os.access(fileName, os.R_OK):
    myfile = ROOT.TFile(fileName)
else:
    sys.exit("Error: Input file does not exist or is not readable")

print("Opened file %s"%myfile.GetName())

# Now you have access to everything you can also see by using the TBrowser
# Load the tree containing all the variables
myChain = ROOT.gDirectory.Get( 'mini' )



# Open an output file to save your histograms in (we build the filename such that it contains the name of the input file)
# RECREATE means, that an already existing file with this name would be overwritten
outfile = ROOT.TFile.Open("analysis_"+myfile.GetName().split('/')[-1], "RECREATE")
outfile.cd()

# Book histograms within the output file
hVertexDist        = ROOT.TH1D("hVertexDist",   "Distribution of the interaction vertex along the z-axis; z [mm]; Entries", 1000, -500, 500)



# To look at each entry in the tree, loop over it.
# Either loop over a fixed amount of events, or over all entries (nEntries)
if numEvents<0:
    nEntries = myChain.GetEntriesFast()
else:
    nEntries = numEvents 

for jentry in range(0, nEntries):
    # python uses indention to show which code belongs into the loop. Thus, every line that should be executed within this loop should 
    # start with at least two spaces

    # print some info about already processed events
    if jentry % 100000 == 0:
        print("Processed", jentry, "/", nEntries, "events")
    
    nb = myChain.GetEntry(jentry)
    if nb <= 0: continue

    # will need to be changed for Monte Carlo events
    weight = 1

    
    # Read a variable from the input
    vertexZ = myChain.vxp_z
    hVertexDist.Fill(vertexZ, weight)

    # printing some of the variables
    #print('vpx_z:', myChain.vxp_z)
    #print('vpx_n: ', myChain.lep_n)
    print('vpx_pt:', [pt/1000.0 for pt in myChain.lep_pt])
    #print('vpx_eta:', myChain.lep_eta)
    


    # Some entries are stored in vectors, meaning they have several entries themselves
    # another loop is needed for these objects
    # e.g.:
#    print "lep_pt:", myChain.lep_pt
#    print "lep_n:",   myChain.lep_n


    # might be helpful, to access all 32 bits of a 32 bit integer flag individually:

    # for bit in range ( 32 ):
    #     flagBit = lep_flag & (1 << bit)
    #     print flagBit


##########################################################################
#end of the event loop
##########################################################################


### The Wrap-up code (writing the files, etc) goes here
# Let's look at the histogram; create a canvas to draw it on
canvas = ROOT.TCanvas("myCanvas", 'Analysis Plots', 200, 10, 700, 500 )
canvas.cd()
hVertexDist.Draw()

#########################################################################

outfile.cd()
print("Writing output to %s"%outfile.GetName())
outfile.Write()

#useful command to pause the execution of the code. Allows to see the plot before python finishes
#ROOT.TPython.Prompt()
# MW: 1/9/2022: Caution here. In a multi-python build, libROOTTPython is only built for the highest 
# Python version. Bottomline: if you run TPython from Python, make sure your Python version is the 
# one that TPython was built for. Hence, instead we use standard python now instead.
usr_input = input ("Press any key to continue ")



