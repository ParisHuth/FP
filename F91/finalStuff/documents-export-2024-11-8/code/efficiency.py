import ROOT
from array import array

max_count = 1000000000000000
current_count =0
# Open the input file and get the tree
input_file = ROOT.TFile.Open("/local/fp9192/data/MC/mc_147770.Zee.root")
tree = input_file.Get("mini")

# Define histograms for the numerator and denominator
binning = [0, 10, 20, 30, 40, 50, 60, 80, 100, 200]  # Example binning in GeV for pT
denominator_hist = ROOT.TH1D("denominator", "Probe Electrons (All); p_{T} [GeV]; Counts", len(binning) - 1, array('d', binning))
numerator_hist = ROOT.TH1D("numerator", "Probe Electrons (Tight); p_{T} [GeV]; Counts", len(binning) - 1, array('d', binning))
tight_pt = ROOT.TH1D("tight_pt", "Tight Electrons over p_{T}; p_{T} [GeV]; Counts", 8, 30, 115)

# Loop over events in the tree
for event in tree:
    if current_count >= max_count:
        break
    current_count+=1
    tag_found = False
    tag_index = -1

    # First, try to find a "tag" electron that meets strict criteria
    for i in range(event.lep_n):
        if (event.lep_flag[i] & 512) != 0:        
        #if (event.lep_flag[i] & 512) != 0 and event.lep_type[i] == 11 and event.trigE==True and event.lep_pt[i] / 1000.0 <= 25 :  # Check if the electron type is valid (assuming '11' is electron)
            pT_tight = event.lep_pt[i] / 1000.0  # Convert MeV to GeV
            #tight_pt.Fill(pT_tight)
            tag_found = True
            tag_index = i
            break  # Stop searching once a tag is found

    # Skip event if no tag electron is found
    if not tag_found:
        continue

    # Look for a "probe" electron, disregarding other event selection cuts
    for j in range(event.lep_n):
        if j == tag_index:  # Skip the tag electron itself
            continue
        if event.lep_type[j] != 11:  # Only consider electrons
            continue

        # Fill denominator histogram with the probe electron's pT
        pT_probe = event.lep_pt[j] / 1000.0  # Convert MeV to GeV
        denominator_hist.Fill(pT_probe)

        # Check if the probe electron passes the tight ID criteria
        # (e.g., check if the "tight" flag is set in lep_flag)
    #if (event.lep_flag[i] & 512) != 0 and event.lep_type[i] == 11 and event.trigE==True and event.lep_pt[i] / 1000.0 <= 25 :        
        if (event.lep_flag[j] & 512) != 0:  # Assuming bit 9 (value 512) indicates "tight"
            numerator_hist.Fill(pT_probe)

# Calculate efficiency by dividing numerator by denominator
efficiency_hist = numerator_hist.Clone("efficiency")
efficiency_hist.Divide(denominator_hist, "B")

# Draw the efficiency histogram
canvas = ROOT.TCanvas("c1", "Efficiency", 800, 600)
efficiency_hist.SetTitle("Detection Efficiency for Tight Electrons; p_{T} [GeV]; Efficiency")
efficiency_hist.Draw("E")



# Save the output if needed
canvas.SaveAs("tight_Zee_efficiency.png")


# Clean up
input_file.Close()

usr_input = input ("Press any key to continue ")

