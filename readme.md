###  `event_generator` package
##### random_event_generator module
- `RandomEventGenerator` class:
Initialised with two variables: `(rate_per_min, duration_mins)`. Validate the length and non-negetivity of the variables.

- A `run(Listener)` method implemented in the `RandomEventGenerator` class. Once the class runs for the
total time given, and during that time, notify a supplied listener each time an event is generated.

### Test cases
In `test_random_event_generator` module, there are:
- A stub Listener class implemented for testing purpose
- Tests covering all codes in the `random_event_generator` module

### Installation
I recommend creating a virtual environment and install the package into the environment, for example:
```bash
$ python3 -m venv venv
$ source venv/bin/activate  
$ pip3 install . -r requirements.txt
```

### Tests
To run the tests to see the listener called, simply:
```bash
$ python3 -m pytest
```
