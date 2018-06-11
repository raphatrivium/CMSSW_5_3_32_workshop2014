int main () {

gSystem->Load("libFWCoreFWLite.so");
AutoLibraryLoader::enable();

TFile f("myTuple.root");
//new TBrowser();

Events->SetAlias("muons","patMuons_cleanPatMuons__PAT.obj");

Events->Draw("muons.pt()");
Events->Draw("muons.eta()");


}
