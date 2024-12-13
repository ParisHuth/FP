# script to determine the Z boson mass
import ROOT
import math
import sys


def gauss(x,par):
    N = par[0]
    m = par[1]
    s = par[2]

    try:
        chi2 = (x[0]-m)*(x[0]-m) / (s*s)

        return N / math.sqrt(2*math.pi*s*s) * math.exp(-0.5*chi2)
    except:
        return 0

# you can use https://en.wikipedia.org/wiki/Relativistic_Breit%E2%80%93Wigner_distribution
# with two free parameters: M and Gamma.
# You will need an additional one N for normalization like in the Gaussian
def bw(x,par):
    return 0



mMin = 70.
mMax = 110.

# this removes the statics box from the plot
ROOT.gStyle.SetOptStat(0)

# Create a canvas to draw on later
canvas = ROOT.TCanvas("myCanvas", 'Analysis Plots', 200, 10, 700, 500 )
canvas.cd()

#open the input histogram
rootfile = ROOT.TFile.Open(sys.argv[1], "READ")
tmpHist = rootfile.Get("hInvMassFin") 
tmpHist.GetXaxis().SetRangeUser(mMin,mMax)
tmpHist.Draw("")

# Create a legend to label the different components of the plot
# https://root.cern.ch/doc/master/classTLegend.html
legend = ROOT.TLegend(0.15, 0.65, 0.4, 0.88)
legend.SetFillColor(0)
legend.SetLineColor(0)

# define a TF1 Gaussian according to our own python function gauss
# https://root.cern.ch/doc/master/classTF1.html
fGauss = ROOT.TF1("fGauss", gauss, mMin, mMax, 3)


fGauss.SetParameter(0,tmpHist.Integral())
fGauss.SetParameter(1,90.0)  
fGauss.SetParameter(2,4.0)

fGauss.SetLineColor(ROOT.kMagenta)
fGauss.SetNpx(1000) # sets the amount of sampling points in x range. Do not choose too small for convolution later on
legend.AddEntry(fGauss, "Gauss", "l")


# do the same thing for a Breit-Wigner distribution
fBw = ROOT.TF1("fBw", bw, mMin, mMax, 3)




# let root perform a convolution of the two functions. It does so by a Fourier transform
# need to set negative x minimum, because Gauss will be centered at 0 and the same range is used on both functions in the convolution
# in principle the order would not matter, but the fit will converge more easily if the distribution centered at 0 comes second
conv = ROOT.TF1Convolution(fBw, fGauss)
conv.SetRange(-20.,mMax)

# convert the TF1Convolution back into a regular TF1 to continue our fitting
# it now has 6 parameters: 0,1,2 from bw and 3,4,5 from gauss
# for the fitting it can make sense to fix some parameters. Both 
# parameters for the mean will shift the result along the x axis
# and both for the normalization will scale it along the y axis.
fConv = ROOT.TF1("fConv", conv, mMin, mMax, conv.GetNpar())

fConv.FixParameter(3,1.0) # this would be the normalization of the gauss
fConv.FixParameter(4,0.0) # this would be the mean of the gauss



tmpHist.SetLineWidth(3)
tmpHist.Draw("E")

tmpHist.Fit(fGauss)
print(("chi2/NDF = %f / %f = %f")%(fGauss.GetChisquare(), fGauss.GetNDF(), fGauss.GetChisquare()/fGauss.GetNDF()))
fGauss.Draw("SAME")




tex = ROOT.TLatex(); tex.SetNDC(True); tex.SetTextSize(0.035); tex.SetTextColor(ROOT.kBlack)

tex.DrawLatex(0.65, 0.85, "Gauss Fit")
tex.DrawLatex(0.65, 0.80, "M_{Z} = %.3f #pm %.3f" %  (fGauss.GetParameter(1), fGauss.GetParError(1)))
tex.DrawLatex(0.65, 0.75, "#sigma = %.3f #pm %.3f" % (fGauss.GetParameter(2), fGauss.GetParError(2)))
tex.DrawLatex(0.65, 0.70, "#chi^{2}_{red} = %.1f" %  (fGauss.GetChisquare() / fGauss.GetNDF()))

legend.AddEntry(tmpHist, "Data")
legend.Draw("SAME")        


canvas.Update()      
#ROOT.TPython.Prompt()  
usr_input = input ("Press any key to continue ")

rootfile.Close()
