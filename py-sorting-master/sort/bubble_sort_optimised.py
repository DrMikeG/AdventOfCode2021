# py-sorting <http://github.com/gwtw/py-sorting>
# Copyright 2015 Daniel Imms <http://www.growingwiththeweb.com>
# Released under the MIT license <http://github.com/gwtw/py-sorting/blob/master/LICENSE>

def default_compare(a, b):
  if a < b:
    return -1
  elif a > b:
    return 1
  return 0

def sort(array, compare=default_compare):
  unsorted_below = len(array)
  while unsorted_below != 0:
    last_swap = 0
    for i in range(1, unsorted_below):
      if compare(array[i - 1], array[i]) > 0:
        array[i], array[i - 1] = array[i - 1], array[i]
        last_swap = i
    unsorted_below = last_swap
  return array
