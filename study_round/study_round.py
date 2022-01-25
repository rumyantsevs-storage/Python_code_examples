# -*- coding: utf-8 -*-

number = '3.999999999'
fraction_digits = 3
# keep_point = True
# nzeros = 1
# ======= тело функции =========
has_minus = False
if number[0] == '-':
    number = number[1:]
    has_minus = True

point_index = False
if number.find('.') != -1:
    point_index = number.find('.')

length_of_number = len(number)
symbols = []

if point_index:
    for i in range(point_index+1, length_of_number):
        symbols.append(int(number[i]))

# print(symbols)

length_of_symbols = len(symbols)

increment = 0
i = length_of_symbols - 1
while i >= fraction_digits - 1:
    digit = symbols[i] + increment
    if digit >= 9:
        symbols[i] = 0
        increment = 1
        if i == fraction_digits:
            fraction_digits -= 1
    elif digit >= 5:
        symbols[i] = digit
        increment = 1
    else:
        symbols[i] = digit
        increment = 0
    if i < length_of_symbols - 1:
        symbols[i+1] = 0
    i -= 1

# print(symbols)
print(fraction_digits)

symbols2 = []

if point_index:
    for i in range(0, point_index):
        symbols2.append(int(number[i]))

# print(symbols2)

length_of_symbols2 = len(symbols2)

if fraction_digits < 0:
    increment = 1
    fraction_digits = 1
else:
    increment = 0

i = length_of_symbols2 - 1
while i >= fraction_digits - 1:
    digit = symbols2[i] + increment
    if digit >= 9:
        symbols2[i] = 0
        increment = 1
        if i == fraction_digits:
            fraction_digits -= 1
    elif digit >= 5:
        symbols2[i] = digit
        increment = 1
    else:
        symbols2[i] = digit
        increment = 0
    if i < length_of_symbols2 - 1:
        symbols2[i+1] = 0
    i -= 1

if fraction_digits < 0:
    symbols2.insert(0, 1)

# print(symbols2)
print(fraction_digits)

symbols = ''.join(map(str, symbols))
symbols2 = ''.join(map(str, symbols2))

if point_index:
    string = symbols2 + '.' + symbols
else:
    string = symbols

if has_minus:
    string = '-' + string

print(number)
print(string)
