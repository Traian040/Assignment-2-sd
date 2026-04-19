from core import Workflow, Orchestrator, Event
from services import (
    IngestService,
    AnalysisService,
    VisualsService,
    AudioTextService,
    ComplianceService,
    PackagingService
)

def main():
    #init
    workflow = Workflow()
    orchestrator = Orchestrator(workflow)
    #register services
    orchestrator.register_processor(Event.INGEST_DONE, IngestService(orchestrator))
    orchestrator.register_processor(Event.ANALYSIS_DONE, AnalysisService(orchestrator))
    orchestrator.register_processor(Event.VISUALS_DONE, VisualsService(orchestrator))
    orchestrator.register_processor(Event.AUDIO_TEXT_DONE, AudioTextService(orchestrator))
    orchestrator.register_processor(Event.COMPLIANCE_DONE, ComplianceService(orchestrator))
    orchestrator.register_processor(Event.PACKAGING_DONE, PackagingService(orchestrator))

    #setup folders
    orchestrator.context["input_file"] = "vid2.mp4" #input file
    #in checksums.json there are 2 vid3.mp4 filenames
    #shorter md5 is wrong to showcase the error handling
    #switch the order around in the json file to see the error
    #vid 1 - drinking game 34.7 Mb
    #vid 2 - i could do that 3.99 Mb
    #vid 3 - she gave me three 27.57 Mb
    orchestrator.context["base_path"] = orchestrator.context["input_file"].split(".",1)[0]

    orchestrator.start_pipeline()

if __name__ == "__main__":
    main()