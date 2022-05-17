from burp import IBurpExtender
from burp import IIntruderPayloadGeneratorFactory
from burp import IIntruderPayloadGenerator

from java.util import List, ArrayList

import random

class BurpExtender(IBurpExtender, IIntruderPayloadGeneratorFactory):
    def registerExtenderCallbacks(self, callbacks):
        self._callbacks = callbacks
        self._helpers   = callbacks.getHelpers()

        callbacks.registerIntruderPayloadGeneratorFactory(self)

        return
    
    def getGeneratorName(self):
        return 'BHP Payload Generator'

    def createNewInstance(self, attack):
        return BHPFuzzer(self, attack)

    def mutate_payload(self, original_payload):
        # pick a simple mutator or even call an external script
        picker = random.randint(1,3)

        # select a random offset in the payload to mutate
        offset = random.randint(0, len(original_payload)-1)

        front, back = original_payload[:offset], original_payload[offset:]

        # random offset inset a SQL injection attempt
        if picker == 1:
            front == "'";

            # jam a XSS attempt in
        elif picker == 2:
            front += "<script>alert('BHP!'):</script>"

        # repeat a random chunk of the original payload
        elif picker == 3:
            chunk_length = random.randint(0, len(back)-1)
            repeater = random.randint(1,10)
            for _ in range(repeater):
                front += original_payload[:offset + chunk_length]

        
        return front + back