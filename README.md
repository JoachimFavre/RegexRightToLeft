# Regex Right To Left
## Description
Turns a regular expression into one that would work the same on a reversed string. In other words, the regex is turned to a right-to-left version of itself. This can be used to find the last (and biggest) occurrence of a regex in a string.

## Features
- Regex atoms
  - Single characters (called units in the program)
  - Escaped characters
  - Intervals
  - Groups (including group operators (see after))
- Repetition operators
  - Single characters: *, +, ?
  - Braces-repetition, such as {2,3}
- Group operators
  - Anonymous group: ?:
  - Positive/negative lookafter: ?= / ?!
  - Positive/negative lookbehind: ?<= / ?<!

## How to use
To only reverse a regular expression, you can call the ```deep_reverse(regex)``` function. If you need an example on how to use a reversed regular expression, you can take a look at the ```find_last(regex, string)``` function.
