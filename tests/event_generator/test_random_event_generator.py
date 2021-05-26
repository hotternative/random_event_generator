# Created on 21/11/2020
import logging
import pytest

from src.event_generator.random_event_generator import RandomEventGenerator


"""Good quality code should have appropriate logging level and message for support and troubleshooting. 
Here I demonstrate the idea with a minimal logger """
logger = logging.getLogger(__name__)


class TestRandomEventGenerator:

    # create a stub Listener class for testing purpose
    class Listener:
        @staticmethod
        def onEvent(dt):
            logger.debug(f'Listener is called at {dt}')

    def test_random_event_generator_initialising_with_unequal_length(self):
        """
        Test the function raises appropriate error if the length of the two input lists are unequal
        """
        with pytest.raises(ValueError):
            randomEventGenerator = RandomEventGenerator([60, 30], [0.1])


    def test_random_event_generator_initialising_with_negative_rate(self):
        """
        Test the function raises appropriate error if any rate is negative
        """
        with pytest.raises(ValueError):
            randomEventGenerator = RandomEventGenerator([60, -30], [0.1, 0.2])


    def test_random_event_generator_initialising_with_negative_duration(self):
        """
        Test the function raises appropriate error if any duration is negative
        """
        with pytest.raises(ValueError):
            randomEventGenerator = RandomEventGenerator([60, 30], [0.1, -0.2])

    def test_random_event_generator_single_duration(self):
        """
        Test the function can handle a single rate and duration
        It should log, *on average*, every second for 6 seconds (0.1 minutes = 6 seconds)

        """
        randomEventGenerator = RandomEventGenerator([60], [0.1])
        randomEventGenerator.run(listener=TestRandomEventGenerator.Listener())


    def test_random_event_generator_multiple_durations(self):
        """
        test the function can handle multiple rates and durations
        It should log, *on average*, every second for 6 seconds (0.1 minutes = 6 seconds),
        then every 2 seconds for 12 seconds
        """
        randomEventGenerator = RandomEventGenerator([60, 30], [0.1, 0.2])
        randomEventGenerator.run(listener=TestRandomEventGenerator.Listener())

    def test_random_event_generator_zero_rate(self):
        """
        test the function can handle zero rate
        It should sleep for 6 seconds (0.1 minutes = 6 seconds),
        """
        randomEventGenerator = RandomEventGenerator([0], [0.1])
        randomEventGenerator.run(listener=TestRandomEventGenerator.Listener())