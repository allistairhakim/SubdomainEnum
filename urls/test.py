import sys

import treq
from twisted.internet.defer import CancelledError, inlineCallbacks
from twisted.internet.task import react
import time

# request to the URL below takes about 5 seconds to complete:
TEST_URL = 'http://httpbin.org/drip?duration=0'
TIMEOUT = float(sys.argv[-1])


@inlineCallbacks
def main(_):
    try:
        start = time.time()

        for i in range(100):
            response = yield treq.get(TEST_URL, timeout=TIMEOUT)
            print(response.code)

        end = time.time()

        print(str(100/(end-start)) + "it/s")
    except CancelledError:
        print('timeout')

react(main)
