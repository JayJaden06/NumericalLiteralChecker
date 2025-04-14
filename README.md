# Python Numeric Literal Checker

This program evaluates whether a string input conforms to the grammar of Python's (2025) numeric literals.
This program will work for decimal integers, octal, hexadecimal, and floating point literals. Underscore seperators in valid positions are supported.

## Installation

This program is a self-contained python file (.py). It requires no installation, but for the system to have python 3 installed.

## Usage

After the program is run, enter the path and file name (i.e. input.txt) into the console for a file that consists of strings to check.

The program expects for each line in the input file to consist of: (input string, expected result), with the string and expected result on the same line, separated by at least one space. The expected result should be either the word "accept" or "reject". The case of the expected result does not matter.

For example:
{{file begin}}
100_00e+10 accept
0xFOOB4RB@Z Reject

After the input file is entered, the program will check the input strings and write the results to "out.txt" in the same directory as the program.

## Group Information

Group: POLY Owns Logical Yeeting
Group Members: Jaden Fong and Mario Mariotta IV

Contributions:

Mario:
- NFA
- Numeric Literal Checker

Jaden:
- Numeric Literal Checker Interface

