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
#   process.source.fileNames = [          ##
#    '/store/relval/CMSSW_3_5_0_pre1/RelValTTbar/GEN-SIM-RECO/STARTUP3X_V14-v1/0006/14920B0A-0DE8-DE11-B138-002618943926.root'
#   ]                                     ##  (e.g. 'file:AOD.root')
#                                         ##
#                                         ##
# process.out.outputCommands = [ 'keep *' ]  ##  (e.g. taken from PhysicsTools/PatAlgos/python/patEventContent_cff.py)
#                                         ##
#   process.out.fileName = ...            ##  (e.g. 'myTuple.root')
#                                         ##
#   process.options.wantSummary = True    ##  (to suppress the long output at the end of the job)    

process.options.wantSummary = False 
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(50) )
process.MessageLogger.cerr.FwkReport.reportEvery = 10

