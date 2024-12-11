import ROOT

#file = ROOT.TFile.Open("Data/DataMuons.root")
file = ROOT.TFile.Open("/local/fp9192/data/MC/mc_147771.Zmumu.root")
tree = file.Get("mini")

outfile = ROOT.TFile.Open("analysis_Zmumu.root", "RECREATE")
outfile.cd()


max_count = 1000000000000000
current_count = 0
weight = 1
# Create a histogram for the cut flow
cutFlowHist = ROOT.TH1D("cutFlowHist", "Cut Flow Histogram; Selection Criterion; Remaining Events", 11, 0, 11)
invMass_cut = ROOT.TH1D("invMasscut", "Invariant Mass using filltered events", 100,75,105)

cutFlowHist.GetXaxis().SetBinLabel(1, "Total Events")
cutFlowHist.GetXaxis().SetBinLabel(2, "Trigger Fired")
cutFlowHist.GetXaxis().SetBinLabel(3, "GRL Passed")
cutFlowHist.GetXaxis().SetBinLabel(4, "Primary Vertex")
cutFlowHist.GetXaxis().SetBinLabel(5, "2 Leptons")
cutFlowHist.GetXaxis().SetBinLabel(6, "Lepton PDGID")
cutFlowHist.GetXaxis().SetBinLabel(7, "Opposite Charge")
cutFlowHist.GetXaxis().SetBinLabel(8, "pT > 25 GeV")
cutFlowHist.GetXaxis().SetBinLabel(9, "Isolation")
cutFlowHist.GetXaxis().SetBinLabel(10, "Tight ID")
cutFlowHist.GetXaxis().SetBinLabel(11, "Z Mass Window")


# Fill the first bin with the total number of events
cutFlowHist.Fill(0, tree.GetEntries())


for event in tree:
    if current_count >= max_count:
        break
    
    current_count +=1
    
#weight = event.mcWeight if hasattr(event, 'mcWeight') and event.mcWeight != 0 else 1

    # Start with the total events bin
    cutFlowHist.Fill(1, weight)

    # Trigger requirement
    if not event.trigM:
        continue
    cutFlowHist.Fill(2, weight)

    # Good Run List
    if not event.passGRL:
        continue
    cutFlowHist.Fill(3, weight)

    # Primary vertex requirement
    if not event.hasGoodVertex:
        continue
    cutFlowHist.Fill(4, weight)

    # Require at least 2 leptons
    if event.lep_n < 2:
        continue
    cutFlowHist.Fill(5, weight)

    # Check PDGID of leptons
    if event.lep_type[0] not in [11, 13] or event.lep_type[1] not in [11, 13]:
        continue
    cutFlowHist.Fill(6, weight)

    # Opposite charge requirement
    if event.lep_charge[0] * event.lep_charge[1] >= 0:
        continue
    cutFlowHist.Fill(7, weight)

    # pT cut for both leptons
    if event.lep_pt[0] / 1000.0 <= 25 or event.lep_pt[1] / 1000.0 <= 25:
        continue
    cutFlowHist.Fill(8, weight)

    # Isolation cut
    isolation1 = event.lep_etcone20[0] / event.lep_pt[0]
    isolation2 = event.lep_etcone20[1] / event.lep_pt[1]
    if isolation1 > 0.1 or isolation2 > 0.1:
        continue
    cutFlowHist.Fill(9, weight)

    # Tight ID check
    if (event.lep_flag[0] & 512 == 0) or (event.lep_flag[1] & 512 == 0):
        continue
    cutFlowHist.Fill(10, weight)

    # Z Mass Window
    
    lep1 = ROOT.TLorentzVector()
    lep2 = ROOT.TLorentzVector()
    lep1.SetPtEtaPhiM(event.lep_pt[0] / 1000.0, event.lep_eta[0], event.lep_phi[0], 0)
    lep2.SetPtEtaPhiM(event.lep_pt[1] / 1000.0, event.lep_eta[1], event.lep_phi[1], 0)
    inv_mass = (lep1 + lep2).M()
    if not (80 <= inv_mass <= 100):
        continue
    cutFlowHist.Fill(11, weight)
    invMass_cut.Fill(inv_mass)

#HE DIED FOR YOUR SINS

canvas = ROOT.TCanvas("c1", "Cut Flow Histogram", 800,600)
cutFlowHist.SetFillColor(ROOT.kBlue-10)
cutFlowHist.SetLineColor(ROOT.kBlue)
cutFlowHist.SetLineWidth(2)
cutFlowHist.SetBarWidth(0.8)
cutFlowHist.Draw("B")
canvas.SetLogy()
canvas.Draw()
canvas.SaveAs("ZmumucutFlowHist.png")

c2 = ROOT.TCanvas("c2", "Invariant mass using filltered events")
c2.cd()
invMass_cut.SetLineColor(ROOT.kBlue)
invMass_cut.SetLineWidth(2)
invMass_cut.Draw()
c2.Draw()
canvas.SaveAs("ZmumuinvMass_cut.png")
invMass_cut.Write()
usr_input = input ("Press any key to continue ")

