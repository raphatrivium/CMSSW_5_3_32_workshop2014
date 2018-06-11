import FWCore.ParameterSet.Config as cms

process = cms.Process("MuonPlots")

# Messages
process.load("FWCore.MessageService.MessageLogger_cfi")
process.MessageLogger.cerr.FwkReport.reportEvery = 1000

#process.MessageLogger.cerr.FwkReport.reportEvery = 1
#process.MessageLogger.destinations += ['AnalyzerMessages']
#process.MessageLogger.categories   += ['IMPGP']
#process.MessageLogger.debugModules += ['globalMuons']
#process.MessageLogger.AnalyzerMessages = cms.untracked.PSet(
#    threshold  = cms.untracked.string('DEBUG'),
#    default    = cms.untracked.PSet(limit = cms.untracked.int32(0)),
#    IMPGP = cms.untracked.PSet(limit = cms.untracked.int32(-1))
#    )

process.load("Configuration.StandardSequences.Geometry_cff")
process.load("Configuration.StandardSequences.MagneticField_38T_cff")
process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
process.load("Configuration.StandardSequences.Reconstruction_cff")
process.GlobalTag.globaltag = 'START44_V7::All'

process.source = cms.Source(
    "PoolSource",
    fileNames = cms.untracked.vstring(
    #'file:patTuple.root'
    'file:tupleMC.root'
    )
    )

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(5000) )
process.options   = cms.untracked.PSet( wantSummary = cms.untracked.bool(True) )

process.TFileService = cms.Service('TFileService', fileName=cms.string('plots_simple.root') )

from HLTrigger.HLTfilters.hltHighLevel_cfi import hltHighLevel
reskim  = hltHighLevel.clone(TriggerResultsTag = cms.InputTag('TriggerResults','',''))
process.recoMu     = reskim.clone(HLTPaths = ['skim_RecoMu'],)
process.bscMinBias = hltHighLevel.clone(HLTPaths = ['HLT_L1_BscMinBiasOR_BptxPlusORMinus'], )

## Common plots
loose_cut = 'isGlobalMuon  ' 

## trigger_match = '(' \
##                 ' triggerMatchesByPath("HLT_Mu9").at(0).pt() > 15) || ' \
##                 '!triggerObjectMatchesByPath("HLT_Mu15_v1").empty()' \
##                 ')'

trigger_match = ' '

my_cut = ' && isTrackerMuon ' \
         ' &&  innerTrack.pt > 20. '

tight_cut = loose_cut + my_cut + trigger_match

from MuonAnalysis.Examples.inclusiveMuonPlots_cfi import makeInclusiveMuonPlots;
process.globalMuons = cms.EDAnalyzer(
    "InclusiveMuonPlots",
    makeInclusiveMuonPlots(0.4,20.),
    # muons     = cms.InputTag('selectedPatMuons',''),
    muons     = cms.InputTag('patMuonsWithTrigger',''),
    selection = cms.string("isGlobalMuon"),
    onlyLeadingMuon = cms.bool(False),
    primaryVertices = cms.InputTag("offlinePrimaryVertices"),
    )

## Now we make the sub-plots with classification by hits
process.globalMuonsGhost = process.globalMuons.clone(selection = "isGlobalMuon && (-5 <= userInt('classByHitsGlb') <= -1)")
process.globalMuonsPunch = process.globalMuons.clone(selection = "isGlobalMuon && ( 0 <= userInt('classByHitsGlb') <=  1)")
process.globalMuonsLight = process.globalMuons.clone(selection = "isGlobalMuon && (userInt('classByHitsGlb') == 2)")
process.globalMuonsHeavy = process.globalMuons.clone(selection = "isGlobalMuon && (userInt('classByHitsGlb') >= 3)")
process.globalMuonsPrompt = process.globalMuons.clone(selection = "isGlobalMuon && (userInt('classByHitsGlb') >= 4)")

process.globalMuonsVBTF = process.globalMuons.clone(selection = tight_cut)
process.globalMuonsVBTFGhost = process.globalMuons.clone(selection = tight_cut + " && isGlobalMuon && (-5 <= userInt('classByHitsGlb') <= -1)")
process.globalMuonsVBTFPunch = process.globalMuons.clone(selection = tight_cut + " && isGlobalMuon && ( 0 <= userInt('classByHitsGlb') <=  1)")
process.globalMuonsVBTFLight = process.globalMuons.clone(selection = tight_cut + " && isGlobalMuon && (userInt('classByHitsGlb') == 2)")
process.globalMuonsVBTFHeavy = process.globalMuons.clone(selection = tight_cut + " && isGlobalMuon && (userInt('classByHitsGlb') >= 3)")
process.globalMuonsVBTFPrompt = process.globalMuons.clone(selection = tight_cut + " && isGlobalMuon && (userInt('classByHitsGlb') >= 4)")

from UserCode.Examples.inclusiveMuonPlotsMRTU_cfi import makeInclusiveMuonPlotsMRTU;
process.globalMuonsMRTU = cms.EDAnalyzer(
    "InclusiveMuonPlotsMRTU",
    makeInclusiveMuonPlotsMRTU(),
    #muons     = cms.InputTag('selectedPatMuons',''),
    muons     = cms.InputTag('patMuonsWithTrigger',''),
    selection = cms.string("isGlobalMuon"),
    primaryVertices = cms.InputTag("offlinePrimaryVertices"),
    )

process.globalMuonsMRTUVBTF = process.globalMuonsMRTU.clone(selection = tight_cut)

process.p = cms.Path(
#    process.recoMu +
#    process.bscMinBias +
    process.globalMuons +
    process.globalMuonsGhost +    
    process.globalMuonsPunch +    
    process.globalMuonsLight +
    process.globalMuonsHeavy +
    process.globalMuonsVBTF +
    process.globalMuonsVBTFGhost +    
    process.globalMuonsVBTFPunch +    
    process.globalMuonsVBTFLight +    
    process.globalMuonsVBTFHeavy +
    process.globalMuonsMRTU +
    process.globalMuonsMRTUVBTF    
)

