# -*- coding: utf-8 -*-

from random import randint
from termcolor import cprint

NUMBER_OF_CATS = 8
DAYS_FOR_LIVING = 365 * 3


class House:

    def __init__(self):
        self.food = 30
        self.money = 50
        self.cat_food_bowl = 0
        self.dirt = 0

    def __str__(self):
        return 'В доме\t' + ' | ' + \
               'еда\t\t%4d' % self.food + ' | ' + \
               'денег %4d' % self.money + ' | ' + \
               'кошачьей еды %4d' % self.cat_food_bowl + ' | ' + \
               'грязи %4d' % self.dirt


class Human:
    near_dead = 0
    eating = 0
    worked = 0
    rested = 0
    bought_food = 0
    bought_cat_food = 0
    cleaned_house = 0

    def __init__(self, name='Человек'):
        self.name = name
        self.fullness = 30
        self.home = house
        self.pet = None
        self.deaded = False

    def __str__(self):
        return self.name + '\t' + ' | ' + \
               'сытость\t%4d\t' % self.fullness

    def act(self):
        if self.fullness < 0:
            self.die()
        elif self.fullness <= 10:
            self.eat()
        elif self.home.food <= 20:
            self.buy_food()
        elif self.home.money <= 50:
            self.work()
        elif (self.home.cat_food_bowl <= 90) and (self.pet is not None):
            self.buy_cat_food()
        elif self.home.dirt >= 90:
            self.clean_the_house()
        else:
            self.play_vieogames()

    def pick_up_a_cat(self, cat):
        print(self.name, 'подобрал кота', cat.name, 'и поселил его в доме.')
        self.pet = cat
        cat.home = self.home

    def eat(self):
        if self.home.food >= 30:
            print(self.name, 'ест.')
            self.fullness += 30
            self.home.food -= 30
            Human.eating += 1
        else:
            cprint(self.name + ' еды нет(', color='red')
            self.fullness -= 10
            Human.near_dead += 1

    def work(self):
        print(self.name, 'работает.')
        self.home.money += 150
        self.fullness -= 10
        Human.worked += 1

    def play_vieogames(self):
        print(self.name, 'играет в видеоигры.')
        self.fullness -= 10
        Human.rested += 1

    def buy_food(self):
        print(self.name, 'покупает еды.')
        self.home.money -= 50
        self.home.food += 50
        Human.bought_food += 1

    def buy_cat_food(self):
        print(self.name, 'покупает кошачьей еды.')
        self.home.cat_food_bowl += 50
        self.home.money -= 50
        Human.bought_cat_food += 1

    def clean_the_house(self):
        print(self.name, 'убирается в доме.')
        self.home.dirt -= 100
        if self.home.dirt < 0:
            self.home.dirt = 0
        self.fullness -= 20
        Human.cleaned_house += 1

    def die(self):
        cprint(self.name + ' мертв.', color='red')
        self.deaded = True


class Cat:
    near_dead = 0

    def __init__(self, name='Кот'):
        self.name = name
        self.fullness = 30
        self.home = None
        self.deaded = False

    def __str__(self):
        return self.name + '\t' + ' | ' + \
               'сытость\t%4d' % self.fullness

    def act(self):
        if self.fullness < 0:
            self.die()
        elif self.fullness <= 10:
            self.eat()
        else:
            dice = randint(0, 1)
            self.sleep() if dice == 0 else self.tear_wallpapers()

    def eat(self):
        if self.home.cat_food_bowl >= 20:
            print(self.name, 'ест.')
            self.fullness += 20
            self.home.cat_food_bowl -= 10
        else:
            cprint(self.name + ' нет еды(', color='red')
            self.fullness -= 10
            Cat.near_dead += 1

    def sleep(self):
        print(self.name, 'спит.')
        self.fullness -= 10

    def tear_wallpapers(self):
        print(self.name, 'дерет обои.')
        self.fullness -= 10
        self.home.dirt += 5

    def die(self):
        cprint(self.name + ' мертв.', color='red')
        self.deaded = True


house = House()
petrov = Human(name='Петров')

cats = []

for number in range(1, NUMBER_OF_CATS + 1):
    cat = Cat(name='Кот ' + str(number))
    cats.append(cat)

for cat in cats:
    petrov.pick_up_a_cat(cat)

for day in range(1, DAYS_FOR_LIVING + 1):
    cprint('================================= день %3d =================================' % day, color='red')
    petrov.act()
    for cat in cats:
        cat.act()
    cprint('----------------------------------------------------------------------------', color='cyan')
    cprint(petrov.__str__())
    for cat in cats:
        cprint(cat.__str__())
    cprint(house.__str__())
cprint('=================================== итог ===================================', color='red')
print('Человек в течение', DAYS_FOR_LIVING, 'дней за все время:')
human_eating = Human.eating / DAYS_FOR_LIVING * 100
human_worked = Human.worked / DAYS_FOR_LIVING * 100
human_rested = Human.rested / DAYS_FOR_LIVING * 100
human_bought_food = Human.bought_food / DAYS_FOR_LIVING * 100
human_bought_cat_food = Human.bought_cat_food / DAYS_FOR_LIVING * 100
human_cleaned_house = Human.cleaned_house / DAYS_FOR_LIVING * 100
cprint('- ел:............' + str(round(human_eating, 2)) + ' %', color='green')
cprint('- работал:.......' + str(round(human_worked, 2)) + ' %', color='yellow')
cprint('- отдыхал:.......' + str(round(human_rested, 2)) + ' %', color='magenta')
cprint('- пок.еду:.......' + str(round(human_bought_food, 2)) + ' %', color='cyan')
cprint('- пок.кош.еду:...' + str(round(human_bought_cat_food, 2)) + ' %', color='white')
cprint('- убирался:......' + str(round(human_cleaned_house, 2)) + ' %', color='red')
if human_eating > 0:
    cprint(' ' * int(round(human_eating * 0.76, 0)), on_color='on_green', end='')
if human_worked > 0:
    cprint(' ' * int(round(human_worked * 0.76, 0)), on_color='on_yellow', end='')
if human_rested > 0:
    cprint(' ' * int(round(human_rested * 0.76, 0)), on_color='on_magenta', end='')
if human_bought_food > 0:
    cprint(' ' * int(round(human_bought_food * 0.76, 0)), on_color='on_cyan', end='')
if human_bought_cat_food > 0:
    cprint(' ' * int(round(human_bought_cat_food * 0.76, 0)), on_color='on_white', end='')
if human_cleaned_house > 0:
    cprint(' ' * int(round(human_cleaned_house * 0.76, 0)), on_color='on_red', end='')
cprint(' ', on_color=None)
print('Коты голодали', Cat.near_dead, 'раз, человек голодал', Human.near_dead, 'раз')
deaded_cats = 0
for cat in cats:
    deaded_cats += 1 if cat.deaded else deaded_cats
print('Котов умерло', deaded_cats)
print('Человек умер:', 'да' if petrov.deaded else 'нет')
input()
