""" ADVENT OF CODE 2020 - DAY 21 - RAYMOND LI """

from __future__ import annotations

import logging
from typing import Dict, List, Set, Tuple


def read_input(filepath: str) -> Tuple[Dict[str, Set[str]], List[str]]:
    """Return processed version of the puzzle input.

    Returned tuple is in the format: (allergens, ingredients)
    """
    with open(filepath) as input_file:
        foods = input_file.read().strip().split('\n')

    allergens = {}  # Dict[str, Set[str]]
    ingredients = []  # List[str]
    for food in foods:
        item_ingredients, item_allergens = food.rstrip(')').split(' (contains ')
        item_ingredients = item_ingredients.split()
        ingredients.append(item_ingredients)
        for allergen in item_allergens.split(', '):
            if allergen not in allergens:
                allergens[allergen] = set(item_ingredients)
            else:
                allergens[allergen] &= set(item_ingredients)

    return (allergens, ingredients)


def solve_part1(filepath: str) -> int:
    """Returns solution to Day 21 Part 1 problem.

    >>> solve_part1('test1.txt')
    5
    """
    logging.debug(f'EXECUTING SOLVE - 1')
    allergens, ingredients = read_input(filepath)

    all_allergens = set(aller for allergen in allergens.values() for aller in allergen)
    return sum(ingredient not in all_allergens for food_item in ingredients for ingredient in food_item)


def process_ingredient(item_allergens: Set[str], ingredient: str,
                       ingredients: Dict[str, Set[str]], allergens: Dict[str, str]) -> None:
    """Process ingredient and its possible allergens.
    """
    for aller in item_allergens:
        if aller in ingredients[ingredient]:
            allergens[aller] = ingredient
            ingredients.pop(ingredient)
            remove_allergen(ingredients, aller)
            return
        else:
            ingredients[ingredient].add(aller)


def remove_allergen(ingredients: Dict[str, Set[str]], allergen: str) -> None:
    """Remove given allergen from any ingredients in ingredients.
    """
    for ingredient in ingredients:
        if allergen in ingredients[ingredient]:
            ingredients[ingredient].remove(allergen)


def solve_part2(filepath: str) -> str:
    """Returns solution to Day 21 Part 2 problem.
    """
    logging.debug(f'EXECUTING SOLVE - 2')
    allergens, _ = read_input(filepath)

    allergen_pairs = []
    for _ in range(len(allergens)):
        allergen_pairs.append(find_solo_allergen(allergens))

    allergen_pairs.sort(key=lambda pair: pair[0])
    return ','.join(pair[1] for pair in allergen_pairs)


def find_solo_allergen(allergens: Dict[str, Set[str]]) -> Tuple[str, str]:
    """Return the allergen and the ingredient that only has one ingredient.

    Returned tuple is in the form: (allergen, ingredient)
    """
    for allergen in allergens:
        if len(allergens[allergen]) == 1:
            solo = (allergen, allergens[allergen].pop())
            remove_ingredient(allergens, solo[1])
            return solo


def remove_ingredient(allergens: Dict[str, Set[str]], ingredient: str) -> None:
    """Remove the given ingredient from the allergens.
    """
    for allergen in allergens:
        if ingredient in allergens[allergen]:
            allergens[allergen].remove(ingredient)


if __name__ == '__main__':
    # logging.basicConfig(level=logging.DEBUG)
    logging.basicConfig(level=logging.WARNING)

    import doctest
    doctest.testmod()

    print(f'D21P1: {solve_part1("input.txt")}')
    print(f'D21P2: {solve_part2("input.txt")}')
