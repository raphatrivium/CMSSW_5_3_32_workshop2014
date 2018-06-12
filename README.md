# CMSSW_5_3_32_workshop2014

Usind CMSSW_5_3_32 for 2014 exercises

MUONS
Reference: https://twiki.cern.ch/twiki/bin/view/CMS/SWGuideCMSDataAnalysisSchool2013MuonExercise

Step 1 - Create a folder
$mkdir CMSDAS
$cd CMSDAS/

Step 2 - Crete the structure CMSSW
$cmsrel CMSSW_5_3_32
Some versions you must go to the folder "src/" as CMSSW_5_3_7 ("$cd CMSSW_5_3_7/src"). So you will notice an error when you compile the file (Step 4). But in this version you must go to folder:
$cd CMSSW_5_3_32/

Step 3 - Acess the cms environment
$ cmsenv

Step 4 - copy few packges and compile it.
$ cp -rf  /afs/cern.ch/user/h/hdyoo/public/CMSDAS2014/MuonExercise/
$ scram b -j 8

Step5 - Go this folder, keep the original file as a reference and work on a copy
$ cd UserCode/CMSDAS/test/PATTuple/
$ cp short_muon_PATandPF2PAT_cfg.py my_muon_PATandPF2PAT_cfg.py

Step 6 - Open file "my_muon_PATandPF2PAT_cfg.py" with your favorite text editor
$ vi my_muon_PATandPF2PAT_cfg.py

Step 7 - Uncomment this line (remove the first character "#" and becareful with identation)

#   process.source.fileNames = [          ##
#    '/store/relval/CMSSW_3_5_0_pre1/RelValTTbar/GEN-SIM-RECO/STARTUP3X_V14-v1/0006/14920B0A-0DE8-DE11-B138-002618943926.root'
#   ]

and that , but change "..." with "('myTuple.root')"

#   process.out.fileName = ...            ##  (e.g. 'myTuple.root')

Step 8 - run the configuration file and see what happens. 
$cmsRun my_muon_PATandPF2PAT_cfg.py



