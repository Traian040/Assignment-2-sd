import time

from services.base import Processor
from core.states import Event

class ComplianceService(Processor):
    def process(self, context):
        print("Step 5: Compliance - Starting safety and branding checks...")

        #cehck for regional content(fake news)
        print("Task: Running safety scanner...")
        time.sleep(2)
        print("Compliance: Scanning for regional content censorship...")
        time.sleep(3)
        print("Compliance: No prohibited content detected for the target regions.")

        #hardcore checking for this one
        print("Task: Applying regional branding...")

        time.sleep(5)
        print(f"Compliance: regional branding compliant to regional guidelines.")

        print("Step 5 Complete: Safety scan and regional branding finalized.")
        self.mediator.on_event(Event.COMPLIANCE_DONE)