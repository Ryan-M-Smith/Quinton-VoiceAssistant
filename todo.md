# To-Do List for Quinton's development

* Finish programming responses **(90%)** - **TESTING** (updating/bug fixing after each test)

* Set up data collection (has been working without problems in testing so far)
  * History **(100%)**
  * Cache **(100%)**

* Set up wake word detection/"always listening" **(90%)** - TESTING
  * Live listening works
  * Need a better way to do wake word detection without wasting credits

* Skim through and clean code **(70%)** - This will probably be an ongoing thing across releases and will never truly be completed

* Set up Quinton's behavior at runtime **(90%)**
  * Quinton can run a full `detect -> listen -> reply` sequence, but the behavior is most likely going to be changing little bits with every update

* Get custom exceptions and warnings working **(98%)** - Everything works, but warnings currently act as exceptions

* _Possible removal:_ Add system information in a `__init__.py` file **(0%)**

* Write `setup.py`/installation files **(0%)**

* Setup wizard **(0%)**

* Write documentation **(70%)**

## Like-to have's that aren't needed for the initial release (in order of usefulness)

* ALSA PCM detection for playback/capture devices (instead of hard-coding in certain cards that must be used) **(0%)**

* Write a method that implements Houndify's formula to calculate credit usage **(50%)**
  * The functions are written, but getting the length of an audio command going into the houndify API is complicated

* Output logs (would log after every request-reply sequence and after an error/warning) **(50%)**
  * Logs are created if an exception/warning is raised, but not after replies

* Simplify the signal handler to be in one function **(0%)**
  * The function to be called in the `try` block would be passed in as a parameter
  * Function arguments/scope issues make this harder than I originally thought
  * The plus side to this is that it will reduce clutter and simplify the code in `main.py`

* Add `silent` decorator for custom exceptions that don't give output to the user **(0%)**
  * Not really useful (hence being ranked least useful)
