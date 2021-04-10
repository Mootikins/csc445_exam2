# Discrete Pushdown Automata

This program is a YAML-defined pushdown automata that can be used to validate
words in defined automata.

## Dependencies

Dependencies for this program are minimal but listed in `requirements.txt`
nonetheless. They can be installed by running `pip install -r requirements`.
Naturally, this will also work in a virtual environment, but YAML parsing is
useful enough that it's not a bad idea to install it system-wide.

## The YAML File

A sample YAML definition file is provided in `sample.yaml`, which has comments
to explain the format and layout. While efforts have been taken to verify that
provided YAML files are in the correct format, there is no guarantee they will
work perfectly, so be careful.

The YAML file contains the following main sections:

- `alphabet`: a single string that is used to define the alphabet of the
  automata.
- `states`: An array of strings that serve as the states. While the sample uses
  `q0` through `q3`, any strings can be provided that are supported by the YAML
  spec.
- `initial`: A string that specifies which state in the `states` array is the
  initial state for the automata.
- `end`: An array of strings that should be present in the `states` array. Any
  states given here should *not* be defined in the `transitions` key.
- `final`: An array of strings that specifies which states from the `states`
  array should be considered a valid final state.
- `transitions`: A nested dictionary where each first level key is the starting
  state for any defined transitions from that state.

  Inside this top level key, there can be one of two types of dictionaries:

  - Any number of *key*: *value* pairs where *key* is the current character in
    the alphabet, and *value* is the destination state.

  - Any number of *key*: *value* pairs where the *key* is a stack value or
    `else`. The value is another dictionary that will be evaluated as follows if
    the current value on the stack matches the *key*:

    - `pop`: An integer saying how many values to pop off the stack.
    - `push`: An array of strings to push onto the stack *after* popping off of
      the stack.
    - `to`: A string specifying which state from the `states` array should be
      moved to after any stack manipulation.

    The `else` key is used to specify which state to transition to if none of
    the stack values defined in the character's match the current value on the
    stack. Note that the value of this `else` key is equivalent to the *value*
    that does not use the stack definitions.
- `stack`: The initial state of the stack when the automata starts.

## Running

The program takes a minimum of two input parameters, which are described in the
help text below:

```
usage: main.py [-h] -f,--yaml-file INPUT word [word ...]

A basic YAML-defined pushdown automata

positional arguments:
  word                  Word(s) to try running through the defined
                        automata

optional arguments:
  -h, --help            show this help message and exit
  -f,--yaml-file INPUT  The YAML file to use as the automaton definition
```
