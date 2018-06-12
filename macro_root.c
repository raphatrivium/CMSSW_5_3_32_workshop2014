void mais(){

gSystem->Load("libFWCoreFWLite.so");
AutoLibraryLoader::enable();
TFile f("myTuple.root");

Events->SetAlias("muons","patMuons_selectedPatMuons__PAT.obj");
Events->SetAlias("muonsPFcuts","patMuons_selectedPatMuonsPFlow__PAT.obj");
TH1F * histoPFcuts=new TH1F("histoPFcuts","histoPFcuts",50,0.,80.);
TH1F * histo=new TH1F("histo","histo",50,0.,80.);
Events->Draw("muonsPFcuts.pt()>>histoPFcuts");
Events->Draw("muons.pt()>>histo");
histo->SetLineColor(1);
histoPFcuts->SetLineColor(2);
histoPFcuts->SetLineStyle(2);
histo->Draw();
histoPFcuts->Draw("same");

}
