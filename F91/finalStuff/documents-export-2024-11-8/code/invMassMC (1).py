import ROOT
import math


# get data
file2 = ROOT.TFile.Open("Data/DataEgamma.root")
file = ROOT.TFile.Open("/local/fp9192/data/MC/mc_147772.Ztautau.root")
tree = file.Get("mini")
tree2 = file2.Get("mini")

# set itteration limits
max_events = 5000
event_count = 0


# create histogram

hInvariantMassLorentz = ROOT.TH1D("hInvariantMassLorentz", "Invariant Mass of Leading Leptons with Lorentzvectors; M [GeV]; Entries", 100, 0, 200)

hInvariantMassLorentzD = ROOT.TH1D("hInvariantMassLorentzD", "Invariant Mass of Leading Leptons with LorentzvectorsD; M [GeV]; Entries", 100, 0, 200)


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

    # calculation with TLorentzVector
    lep1 = ROOT.TLorentzVector()
    lep2 = ROOT.TLorentzVector()
    lep1.SetPtEtaPhiM(pT1, eta1, phi1, 0)
    lep2.SetPtEtaPhiM(pT2, eta2, phi2, 0)

    M_lorentz = (lep1 + lep2).M()
    hInvariantMassLorentz.Fill(M_lorentz)


event_count =0
for event in tree2:
    if event_count >= max_events:
        break

    if event.lep_n < 2:
        continue # skiping events with less than two leptons

    event_count += 1
    
    # assigning variables and converting to GeV
    pT1, pT2 = event.lep_pt[0]/1000.0, event.lep_pt[1]/1000.0
    eta1, eta2 = event.lep_eta[0], event.lep_eta[1]
    phi1, phi2 = event.lep_phi[0], event.lep_phi[1]

    # calculation with TLorentzVector
    lep1 = ROOT.TLorentzVector()
    lep2 = ROOT.TLorentzVector()
    lep1.SetPtEtaPhiM(pT1, eta1, phi1, 0)
    lep2.SetPtEtaPhiM(pT2, eta2, phi2, 0)

    M_lorentz = (lep1 + lep2).M()
    hInvariantMassLorentzD.Fill(M_lorentz)


# drawing
canvas = ROOT.TCanvas("c1", "Invariant Mass Comparison", 800,600)

hInvariantMassLorentz.SetLineColor(ROOT.kBlue)
hInvariantMassLorentz.SetLineWidth(2)
hInvariantMassLorentzD.SetLineColor(ROOT.kRed)
hInvariantMassLorentzD.SetLineWidth(2)

hInvariantMassLorentz.Draw()
hInvariantMassLorentzD.Draw("SAME")



canvas.SaveAs("invariant_mass_comp_MC_tau.png")
canvas.Draw()

usr_input = input ("Press any key to continue ")
