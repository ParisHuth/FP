import ROOT
import math


# get data
file = ROOT.TFile.Open("Data/DataEgamma.root")
tree = file.Get("mini")

# set itteration limits
max_events = 50000
event_count = 0


# create histogram
hInvariantMass = ROOT.TH1D("hInvariantMass", "Invariant Mass of Leading Leptons; M [GeV]; Entries", 100, 0, 200)
hInvariantMassLorentz = ROOT.TH1D("hInvariantMassLorentz", "Invariant Mass of Leading Leptons with Lorentzvectors; M [GeV]; Entries", 100, 0, 200)

for event in tree:
    if event_count >= max_events:
        break

    if event.lep_n < 2:
        continue # skiping events with less than two leptons

    event_count += 1
    
    # assigning variables and converting to GeV
    pT1, pT2 = event.lep_pt[0]/1000.0, event.lep_pt[1]/1000.0
    eta1, eta2 = event.lep_eta[0], event.lep_eta[1]
    phi1, phi2 = event.lep_phi[0], event.lep_phi[1]

    # calculating the energy
    E1 = pT1 * math.cosh(eta1)
    E2 = pT2 * math.cosh(eta2)

    # calculating the momentum
    px1, py1, pz1 = pT1 * math.cos(phi1), pT1 * math.sin(phi1), pT1 * math.sinh(eta1)
    px2, py2, pz2 = pT2 * math.cos(phi2), pT2 * math.sin(phi2), pT2 * math.sinh(eta2)

    # calculate invariant mass
    M2 = (E1 + E2)**2 - ((px1+px2)**2 + (py1+py2)**2 +(pz1+pz2)**2)

    if M2 >0:
        M = math.sqrt(M2)
        hInvariantMass.Fill(M)

    # calculation with TLorentzVector
    lep1 = ROOT.TLorentzVector()
    lep2 = ROOT.TLorentzVector()
    lep1.SetPtEtaPhiM(pT1, eta1, phi1, 0)
    lep2.SetPtEtaPhiM(pT2, eta2, phi2, 0)

    M_lorentz = (lep1 + lep2).M()
    hInvariantMassLorentz.Fill(M_lorentz)


# drawing
canvas = ROOT.TCanvas("c1", "Invariant Mass Comparison", 800,600)
hInvariantMass.SetLineColor(ROOT.kRed)
hInvariantMassLorentz.SetLineColor(ROOT.kBlue)
hInvariantMass.SetLineWidth(3)
hInvariantMassLorentz.SetLineWidth(2)

hInvariantMass.Draw()
hInvariantMassLorentz.Draw("SAME")

legend = ROOT.TLegend(0.5,0.7,0.7,0.9)
legend.AddEntry(hInvariantMass, "Manual Calculation", "1")
legend.AddEntry(hInvariantMassLorentz, "TLorentzVector Calculation", "1")
legend.Draw('SAME')


canvas.SaveAs("invariant_mass_comp.png")
canvas.Draw()

usr_input = input ("Press any key to continue ")
