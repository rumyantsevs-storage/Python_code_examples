# -*- coding: utf-8 -*-

from random import randint

computer_number = 0


def guess_a_number():
    global computer_number
    computer_number = str(randint(1000, 9999))


def check_number(player_number):
    global computer_number
    scores, new_number1, new_number2 = {'bulls': 0, 'cows': 0}, '', ''

    # print(computer_number)
    # print(player_number)

    i = 0
    while i < len(computer_number):
        if player_number[i] == computer_number[i]:
            scores['bulls'] += 1
        else:
            new_number1 += computer_number[i]
            new_number2 += player_number[i]
        i += 1

    if scores['bulls'] == 4:
        return scores

    i = 0
    while i < len(new_number1):
        j = 0
        while j < len(new_number1):
            if new_number1[i] == new_number2[j]:
                scores['cows'] += 1
                break
            j += 1
        i += 1

    # print(new_number1)
    # print(new_number2)

    return scores
