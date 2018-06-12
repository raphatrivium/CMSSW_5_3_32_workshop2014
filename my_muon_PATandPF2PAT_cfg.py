## import skeleton process
from PhysicsTools.PatAlgos.patTemplate_cfg import *

# the source is already defined in patTemplate_cfg.
# We can override source and various other things
#process.load("CommonTools.ParticleFlow.Sources.source_ZtoEles_DBS_312_cfi")
#process.source = cms.Source("PoolSource", 
#     fileNames = cms.untracked.vstring('file:myAOD.root')
#)

#process.source.fileNames = cms.untracked.vstring(
#    pickRelValInputFiles(
#    cmsswVersion  = 'CMSSW_4_4_2'
#    #, relVal        = 'RelValTTbar'
#    #, relVal        = 'RelValSingleMuPt100'
#    , relVal        = 'RelValZMM'
#    , globalTag     = 'START44_V7'
#    , numberOfFiles = 1
#    )
#    )

## let it run
process.p = cms.Path(
    process.patDefaultSequence
    )


## ------------------------------------------------------
#  In addition you usually want to change the following
#  parameters:
## ------------------------------------------------------
#
#   process.GlobalTag.globaltag =  ...    ##  (according to https://twiki.cern.ch/twiki/bin/view/CMS/SWGuideFrontierConditions)
#                                         ##
process.source.fileNames = [          
    'file:/afs/cern.ch/cms/Tutorials/TWIKI_DATA/CMSDataAnaSch_RelValZMM525.root'
]                                     ##  (e.g. 'file:AOD.root')
#                                         ##
#                                         ##
# process.out.outputCommands = [ 'keep *' ]  ##  (e.g. taken from PhysicsTools/PatAlgos/python/patEventContent_cff.py)
#                                         ##
process.out.fileName =  ('myTuple.root')
#                                         ##
#   process.options.wantSummary = True    ##  (to suppress the long output at the end of the job)    

#-----------------------------------------
# use Particle Flow Muons
runOnMC = True

# Configure PAT to use PF2PAT instead of AOD sources
# this function will modify the PAT sequences.
from PhysicsTools.PatAlgos.tools.pfTools import *

# An empty postfix means that only PF2PAT is run,
# otherwise both standard PAT and PF2PAT are run. In the latter case PF2PAT
# collections have standard names + postfix (e.g. patElectronPFlow)  
postfix = "PFlow"
jetAlgo="AK5"
# usePF2PAT is PAT tool to switch the input of the all pat::Candidate collections from normal reco objects to particle flow objects. 
#If 'runPF2PAT' is true, PF2PAT will be added in front of the patDefaultSequence. 
usePF2PAT(process,runPF2PAT=True, jetAlgo=jetAlgo, runOnMC=runOnMC, postfix=postfix) 
# to run second PF2PAT+PAT with different postfix uncomment the following lines
# and add the corresponding sequence to path
#postfix2 = "PFlow2"
#jetAlgo2="AK7"
#usePF2PAT(process,runPF2PAT=True, jetAlgo=jetAlgo2, runOnMC=True, postfix=postfix2)

# to use tau-cleaned jet collection uncomment the following:
#getattr(process,"pfNoTau"+postfix).enable = True 

# to switch default tau to HPS tau uncomment the following:
#adaptPFTaus(process,"hpsPFTau",postfix=postfix)


if runOnMC == False:
    # removing MC matching for standard PAT sequence
    # for the PF2PAT+PAT sequence, it is done in the usePF2PAT function
    removeMCMatchingPF2PAT( process, '' ) 

## let it run
process.p = cms.Path(
    getattr(process,"patPF2PATSequence"+postfix)
#    second PF2PAT
#    + getattr(process,"patPF2PATSequence"+postfix2)
)

if not postfix=="":
    process.p += process.patDefaultSequence

# Add PF2PAT output to the created file
from PhysicsTools.PatAlgos.patEventContent_cff import patEventContentNoCleaning
process.out.outputCommands = cms.untracked.vstring('drop *',
                                                   'keep recoPFCandidates_particleFlow_*_*',
                                                   *patEventContentNoCleaning ) 


# top projections in PF2PAT:
getattr(process,"pfNoPileUp"+postfix).enable = True 
getattr(process,"pfNoMuon"+postfix).enable = True 
getattr(process,"pfNoElectron"+postfix).enable = True 
getattr(process,"pfNoTau"+postfix).enable = False 
getattr(process,"pfNoJet"+postfix).enable = True 

# verbose flags for the PF2PAT modules
getattr(process,"pfNoMuon"+postfix).verbose = False
#--------------------------------------------
#End Particle Flow

#MC particle match
#-------------------------------------------
#from SUSYBSMAnalysis.Zprime2muAnalysis.PATTools import pruneMCLeptons, addMuonMCClassification
#pruneMCLeptons(process, use_sim=True)
                 
## process.genSimLeptons.filter = cms.vstring('(abs(pdgId) == 13 || abs(pdgId) == 11)')
#----------------------------------

#using GEN ang SIM.
#---------------------------------------
process.load("SimGeneral.HepPDTESSource.pythiapdt_cfi")
process.inFlightMuons = cms.EDProducer("PATGenCandsFromSimTracksProducer",
        src           = cms.InputTag("g4SimHits"),   ## use "famosSimHits" for FAMOS, "g4SimHits" for FULLSIM
        setStatus     = cms.int32(9),
        particleTypes = cms.vstring("mu+"),          ## picks also mu-, of course
        filter        = cms.vstring(""), ##("pt > 0.5"),  ## just for testing
        makeMotherLink = cms.bool(True),
        writeAncestors = cms.bool(True),            ## save also the intermediate GEANT ancestors of the muons
        genParticles   = cms.InputTag("genParticles"),
)

process.patDefaultSequence.replace(process.muonMatch,process.inFlightMuons + process.muonMatch)

process.muMatch1 = process.muonMatch.clone(mcStatus = [1,3,8])
process.muMatch9 = process.muonMatch.clone(mcStatus = [9], matched = cms.InputTag("inFlightMuons"), maxDeltaR = 1.0)

process.patDefaultSequence.replace(
    process.muonMatch,
    process.muMatch1 +
    process.muMatch9
    )

## particles source to be used for the matching
## add input(s) with MC match information
process.patMuons.genParticleMatch = cms.VInputTag(
    cms.InputTag("muMatch1"),
    cms.InputTag("muMatch9"),
)
#----------------------------------------------------------


process.options.wantSummary = False 
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(50) )
process.MessageLogger.cerr.FwkReport.reportEvery = 10
