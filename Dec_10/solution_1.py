'''
Advent of Code - Dec 10
Author: Kevin Peter

--- Day 10: Factory ---
Just across the hall, you find a large factory. Fortunately, the Elves here have plenty of time to decorate. Unfortunately, it's because the factory machines are all offline, and none of the Elves can figure out the initialization procedure.

The Elves do have the manual for the machines, but the section detailing the initialization procedure was eaten by a Shiba Inu. All that remains of the manual are some indicator light diagrams, button wiring schematics, and joltage requirements for each machine.

For example:

[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}
[...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}
[.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}
The manual describes one machine per line. Each line contains a single indicator light diagram in [square brackets], one or more button wiring schematics in (parentheses), and joltage requirements in {curly braces}.

To start a machine, its indicator lights must match those shown in the diagram, where . means off and # means on. The machine has the number of indicator lights shown, but its indicator lights are all initially off.

So, an indicator light diagram like [.##.] means that the machine has four indicator lights which are initially off and that the goal is to simultaneously configure the first light to be off, the second light to be on, the third to be on, and the fourth to be off.

You can toggle the state of indicator lights by pushing any of the listed buttons. Each button lists which indicator lights it toggles, where 0 means the first light, 1 means the second light, and so on. When you push a button, each listed indicator light either turns on (if it was off) or turns off (if it was on). You have to push each button an integer number of times; there's no such thing as "0.5 presses" (nor can you push a button a negative number of times).

So, a button wiring schematic like (0,3,4) means that each time you push that button, the first, fourth, and fifth indicator lights would all toggle between on and off. If the indicator lights were [#.....], pushing the button would change them to be [...##.] instead.

Because none of the machines are running, the joltage requirements are irrelevant and can be safely ignored.

You can push each button as many times as you like. However, to save on time, you will need to determine the fewest total presses required to correctly configure all indicator lights for all machines in your list.

There are a few ways to correctly configure the first machine:

[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}
You could press the first three buttons once each, a total of 3 button presses.
You could press (1,3) once, (2,3) once, and (0,1) twice, a total of 4 button presses.
You could press all of the buttons except (1,3) once each, a total of 5 button presses.
However, the fewest button presses required is 2. One way to do this is by pressing the last two buttons ((0,2) and (0,1)) once each.

The second machine can be configured with as few as 3 button presses:

[...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}
One way to achieve this is by pressing the last three buttons ((0,4), (0,1,2), and (1,2,3,4)) once each.

The third machine has a total of six indicator lights that need to be configured correctly:

[.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}
The fewest presses required to correctly configure it is 2; one way to do this is by pressing buttons (0,3,4) and (0,1,2,4,5) once each.

So, the fewest button presses required to correctly configure the indicator lights on all of the machines is 2 + 3 + 2 = 7.

Analyze each machine's indicator light diagram and button wiring schematics. What is the fewest button presses required to correctly configure the indicator lights on all of the machines?
'''
from itertools import combinations
from os import path
import re

sample_input_file = path.join(path.dirname(__file__), 'sample_input.txt')
input_file = path.join(path.dirname(__file__), 'input.txt')

with open(input_file, 'r') as file:
    data = file.read().splitlines()

indicator_lights_list, buttons_list = [], []

for line in data:
    indicator_lights = line[1: line.index(']')]
    indicator_lights_list.append(indicator_lights)
    buttons_str = line[line.index(']') + 1: line.index('{')].strip()
    buttons = re.findall(r'\((.*?)\)', buttons_str)
    buttons_list.append(buttons)

'''
Expected output format for indicator lights: ['.##.', '...#.', '.###.#']
Expected output format for buttons: [['3', '1,3', '2', '2,3', '0,2', '0,1'], ['0,2,3,4', '2,3', '0,4', '0,1,2', '1,2,3,4'], ['0,1,2,3,4', '0,3,4', '0,1,2,4,5', '1,2']]
'''

reqd_button_presses = 0


def get_button_values(indicator_light, buttons):
    button_values = []
    for btn in buttons:
        btn_binary = ['0'] * len(indicator_light)
        for pos in btn.split(','):
            btn_binary[int(pos)] = '1'
        btn_binary_str = ''.join(btn_binary)
        btn_value = int(btn_binary_str, 2)
        button_values.append(btn_value)
    return button_values


def get_indicator_light_value(indicator_light):
    indicator_light_binary = ''.join(['1' if ch == '#' else '0' for ch in indicator_light])
    return int(indicator_light_binary, 2)


# def values_needed_to_xor_to_target(button_values, target):
#     n = len(button_values)
#     for r in range(1, n + 1):
#         for combo in combinations(button_values, r):
#             if eval('^'.join(map(str, combo))) == target:
#                 return combo
#     return None

# def values_needed_to_xor_to_target(button_values, target):
#     # dp[xor_value] = (count, last_button_used)
#     # We track which buttons lead to each XOR value
#     dp = {0: (0, [])}  # Start with 0 XOR (no buttons pressed)

#     for button in button_values:
#         new_states = {}
#         for current_xor, (count, buttons_used) in dp.items():
#             new_xor = current_xor ^ button
#             new_count = count + 1
#             new_buttons = buttons_used + [button]

#             # Only update if we found a shorter path to this XOR value
#             if new_xor not in dp or new_count < dp[new_xor][0]:
#                 new_states[new_xor] = (new_count, new_buttons)

#         dp.update(new_states)

#         # Early exit if we found the target
#         if target in dp:
#             return tuple(dp[target][1])

#     return None if target not in dp else tuple(dp[target][1])

def values_needed_to_xor_to_target(button_values, target):
    from collections import deque

    visited = {0}
    queue = deque([(0, [])])  # (current_xor, buttons_used)

    while queue:
        current_xor, buttons_used = queue.popleft()

        if current_xor == target:
            return tuple(buttons_used)

        for button in button_values:
            new_xor = current_xor ^ button
            if new_xor not in visited:
                visited.add(new_xor)
                queue.append((new_xor, buttons_used + [button]))

    return None


for i in range(len(data)):
    indicator_light_value = get_indicator_light_value(indicator_lights_list[i])
    button_values = get_button_values(indicator_lights_list[i], buttons_list[i])

    reqd_button_presses += len(values_needed_to_xor_to_target(button_values, indicator_light_value))

print(f"Required button presses: {reqd_button_presses}")
