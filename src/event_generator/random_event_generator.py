# Created on 20/11/2020
import logging
import multiprocessing
import random
import time

from datetime import datetime


logger = logging.getLogger(__name__)

class RandomEventGenerator:
    ####################################################################################################################
    #  generates random events.
    ####################################################################################################################
    def __init__(self, rate_per_min, duration_mins):
        logger.info('Random Event Generator initialising...')
        if len(rate_per_min) != len(duration_mins):

            error_msg = 'rate_per_min and duration_mins must have the same length'
            logger.error(error_msg)
            raise ValueError(error_msg)


        # check that all the rates are greater or equal to zero, since a negative rate doesn't make sense
        # also convert the rate into rate per second
        self.rates = []
        for rate in rate_per_min:
            if rate < 0:
                error_msg = 'All elements in rate_per_minute shall be greater or equal to zero'
                logger.error(error_msg)
                raise ValueError(error_msg)
            else:
                self.rates.append(rate/60)


        # check that all the durations are greater or equal to zero, since a negative duration doesn't make sense
        # also convert the unit of duration into seconds
        self.durations = []
        for duration in duration_mins:
            if duration < 0:
                error_msg = 'All elements in duration_minutes shall be greater or equal to zero'
                logger.error(error_msg)
                raise ValueError(error_msg)
            else:
                self.durations.append(duration * 60)

    @staticmethod
    def _run(rate, listener):
        """
         Generate a random duration to sleep between two consecutive events and call the listener after sleep

         Since the rate is constant within each interval,
         if we assume the incidence of future events is independent of the past --> this is a Poisson process -->
         the time interval between two events in a Poisson process follows exponential distribution -->

         """
        logger.info(f'Starting event generator at rate {rate} per second')
        while True:
            # create a random sleep duration with exponential distribution:
            sleep_duration = random.expovariate(rate)

            # sleep for this long
            time.sleep(sleep_duration)

            # call the listener object on waking up
            listener.onEvent(datetime.now())

    def run(self, listener):
        for rate, duration in zip(self.rates, self.durations):
            logger.info(f'Random_event_generator starts at {datetime.now()}')
            if rate == 0:
                # rate equals zero means that in the given duration, no event needs to be issued.
                # The program can sleep through the given duration.
                time.sleep(duration)
                continue

            # Start _run as a process, here I choose multiprocessing to make use of its terminate API
            event_generator_process = multiprocessing.Process(target=self._run, args=(rate, listener))
            event_generator_process.start()

            # main process sleeps for the duration to block
            time.sleep(duration)

            # terminate the event_generator process after sleep
            event_generator_process.terminate()

            # make sure the event generator process is cleaned up
            event_generator_process.join()
