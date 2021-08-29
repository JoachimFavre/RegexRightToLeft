# -*- coding: utf-8 -*-
r"""
Inverses a regex expression in order to have it working for a reversed string.

Use deep_reverse(regex) to reverse a regular expression and
find_last(regex, string) to have an example of a use for reversed expressions.
Do not hesitate to use r-strings (with a r before the ": such as r".\?") so
that \ is a character in itself and is not used for escaping characters (else
you would have to write "\\\\" instead of r"\\" to have a regex of \\ which
matches \ ).

Created on Sun Aug 29 22:01:21 2021
@author: Joachim Favre
"""
import re


REVERSE_GROUP_OPERATOR = {"": "",  # default case
                          "?:": "?:",  # anonym group
                          "?=": "?<=",  # positive lookafter
                          "?<=": "?=",  # positive lookbehind
                          "?!": "?<!",  # negative lookafter
                          "?<!": "?<"}  # negative lookbehind


class ParseException(Exception):
    """
    An exception that is triggered when there is a problem while parsing the
    given regex.
    """

    def __init__(self, message):
        super().__init__("Error while parsing the regular expression. Error: "
                         + message)


def is_unit(char):
    """
    Verifies whether the character given is a "unit" (meaning it is a regex
    command (by opposition to an operator)).
    """
    assert len(char) == 1
    return char.isalpha() or char.isnumeric() or char in ['.', ' ', '-']


def extract_operator(regex):
    """
    Extracts a potential multiplication operator (meaning '*', '+', '?'
    or {...}) from the very beginning of a regular expression.
    Returns {operator}, {rest of the regular expression}
    """
    if regex == "":
        return "", regex
    if regex[0] in ["*", "+", "?"]:
        return regex[0], regex[1:]
    if regex[0] == "{":
        end_point = get_closing_bracket_index(regex, "{", "}") + 1
        return regex[:end_point], regex[end_point:]
    return "", regex


def get_closing_bracket_index(regex, opening, closing):
    """
    Returns the index of the corresponding ending bracket. This function
    needs to have the first character being an opening bracket.
    """
    assert regex[0] == opening
    bracket_level = 0
    for index, char in enumerate(regex):
        if char == opening:
            bracket_level += 1
        elif char == closing:
            bracket_level -= 1
            if bracket_level == 0:
                return index
    raise ParseException("No closing bracket '" + closing + "' found.")


def split(regex):
    """
    Splits a regular expression to a head, an operator and the rest. The head
    is one "atom" (meaning a unit, an escaped character, an interval, or a
    group). See the function extract_operator(regex) for further information
    on the operators.
    """
    if regex == "":
        return "", "", ""
    end_point = None  # excluded
    if is_unit(regex[0]):
        end_point = 1
    elif regex[0] == "\\":
        end_point = 2
    elif regex[0] == "[":
        end_point = get_closing_bracket_index(regex, "[", "]") + 1
    elif regex[0] == "(":
        end_point = get_closing_bracket_index(regex, "(", ")") + 1
    else:
        raise ParseException("Unexpected token in '" + regex + "'. If it is "
                             "one character long, you can add it in the "
                             "is_unit(char) function.")

    operator, rest = extract_operator(regex[end_point:])
    return regex[:end_point], operator, rest


def split_group(group):
    """
    Converts a list of objects splitted by "|" into a list. The complication
    comes from the fact that we do not want to use other group's "|" to split
    this one. Meaning (a|(b|c)|e) should be splitted into ['a', '(b|c)', 'e'].
    Warning, this function supposes that there is no parenthesis around the
    given group (it must be under the form "a|(b|c)|e").
    """
    # suppose no parenthesis around group
    parenthesis_level = 0
    last_split_index = 0
    result = []
    for index, char in enumerate(group):
        if char == "(":
            parenthesis_level += 1
        elif char == ")":
            parenthesis_level -= 1
        elif char == "|" and parenthesis_level == 0:
            result.append(group[last_split_index:index])
            last_split_index = index + 1
    result.append(group[last_split_index:])
    return result


def extract_group(group):
    """
    Takes a group (which must begin with a '(' and end with a ')') and splits
    it into an operator (meaning anonym group, positive/negative lookahead,
    positive/negative lookbehind) and a list of the contained atoms (the
    atoms splitted by '|'); see split_group(group) for further information.
    """
    assert group[0] == "(" and group[-1] == ")"

    operator_end = 1
    if group[1] == "?":
        if len(group) >= 3 and group[1:3] in ["?:", "?=", "?!"]:
            operator_end = 3
        if len(group) >= 4 and group[1:4] in ["?<=", "?<!"]:
            operator_end = 4
    return group[1:operator_end], split_group(group[operator_end:-1])


def reverse(atom):
    """
    Takes an atom and reverses it. The complications come from the fact that
    we need to reverse every signle element of a group.
    """
    if len(atom) == 1:
        return atom
    if atom[0] == "\\" and len(atom) == 2:
        return atom
    if atom[0] == "[" and atom[-1] == "]":
        return atom
    if atom[0] == "(" and atom[-1] == ")":
        group_operator, terms = extract_group(atom)
        result = "(" + REVERSE_GROUP_OPERATOR[group_operator]
        for index, term in enumerate(terms):
            if index != 0:
                result += "|"
            result += deep_reverse(term)
        return result + ")"

    raise ParseException("'" + atom + "' is not an atom, this should not "
                         "happen.")


def deep_reverse(regex):
    """
    Reverses completely a regex expression. This is the function you need to
    call as a user.
    """
    if regex == "":
        return ""
    head, operator, rest = split(regex)
    return deep_reverse(rest) + reverse(head) + operator


def find_last(regex, string):
    """
    Finds the last (and biggest) occurence of the regular expression in the
    string. This is an example of how to use reversed_regex. If you need to
    use it into your code, you can just compute once reversed_regex using
    this program and only use this function in your code.
    """
    reversed_regex = deep_reverse(regex)
    reversed_string = string[::-1]
    match = re.search(reversed_regex, reversed_string)
    print(reversed_string)
    reversed_result = match.group(0)
    result = reversed_result[::-1]
    return result
