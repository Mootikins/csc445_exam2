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

  A general transition definition has three parts:

  - `pop`: The number of values to pop off the stack -- defaults to one (1)
  - `push`: An array of strings or values to push onto the stack after popping
  - `to`: The destination state to transition to after stack operations

  The top level (state) key contains any number of nested *key*: *value* pairs,
  where the key is the character that the transition information (in value) is
  used.

  The value mentioned in the previous paragraph can contain up to four keys:

    - `stack`: Any number of *key*: *value* pairs, where the key is a stack
      value to transition on, and value is the general transition definition
      described above (that contains `pop`, `push`, and `to`).
    - The keys from the general transition definition above. This is used only
      if none of the transitions in the `stack` key (if present) match the
      current top of the stack.

- `stack`: The initial state of the stack when the automata starts.

## Running

The program takes a minimum of two input parameters, which are described in the
help text below:

```
usage: main.py [-h] -f, --yaml INPUT [-d, --debug] word [word ...]

A basic YAML-defined pushdown automata

positional arguments:
  word              Word(s) to try running through the defined automata

optional arguments:
  -h, --help        show this help message and exit
  -f, --yaml INPUT  The YAML file to use as the automaton definition
  -d, --debug       Print debug messages, which includes transitions (default:
                    False)
```
