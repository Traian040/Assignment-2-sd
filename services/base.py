from abc import ABC, abstractmethod
import os

class Processor(ABC):
    def __init__(self, mediator):
        self.mediator = mediator

    @abstractmethod
    def process(self, context: dict):
        pass
    #perform task

    def ensure_dir(self, path):
        os.makedirs(path, exist_ok=True)
        #create the directory if it doesn't exist'