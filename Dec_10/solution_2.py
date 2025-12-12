'''
Advent of Code - Dec 10
Author: Kevin Peter

--- Part Two ---
All of the machines are starting to come online! Now, it's time to worry about the joltage requirements.

Each machine needs to be configured to exactly the specified joltage levels to function properly. Below the buttons on each machine is a big lever that you can use to switch the buttons from configuring the indicator lights to increasing the joltage levels. (Ignore the indicator light diagrams.)

The machines each have a set of numeric counters tracking its joltage levels, one counter per joltage requirement. The counters are all initially set to zero.

So, joltage requirements like {3,5,4,7} mean that the machine has four counters which are initially 0 and that the goal is to simultaneously configure the first counter to be 3, the second counter to be 5, the third to be 4, and the fourth to be 7.

The button wiring schematics are still relevant: in this new joltage configuration mode, each button now indicates which counters it affects, where 0 means the first counter, 1 means the second counter, and so on. When you push a button, each listed counter is increased by 1.

So, a button wiring schematic like (1,3) means that each time you push that button, the second and fourth counters would each increase by 1. If the current joltage levels were {0,1,2,3}, pushing the button would change them to be {0,2,2,4}.

You can push each button as many times as you like. However, your finger is getting sore from all the button pushing, and so you will need to determine the fewest total presses required to correctly configure each machine's joltage level counters to match the specified joltage requirements.

Consider again the example from before:

[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}
[...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}
[.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}
Configuring the first machine's counters requires a minimum of 10 button presses. One way to do this is by pressing (3) once, (1,3) three times, (2,3) three times, (0,2) once, and (0,1) twice.

Configuring the second machine's counters requires a minimum of 12 button presses. One way to do this is by pressing (0,2,3,4) twice, (2,3) five times, and (0,1,2) five times.

Configuring the third machine's counters requires a minimum of 11 button presses. One way to do this is by pressing (0,1,2,3,4) five times, (0,1,2,4,5) five times, and (1,2) once.

So, the fewest button presses required to correctly configure the joltage level counters on all of the machines is 10 + 12 + 11 = 33.

Analyze each machine's joltage requirements and button wiring schematics. What is the fewest button presses required to correctly configure the joltage level counters on all of the machines?
'''
from os import path
import re
from z3 import Int, Optimize, Sum, sat

sample_input_file = path.join(path.dirname(__file__), 'sample_input.txt')
input_file = path.join(path.dirname(__file__), 'input.txt')

# Choose which file to run
file_to_use = input_file  # change to input_file for real input

with open(file_to_use, 'r') as file:
    data = file.read().splitlines()

buttons_list, joltage_list = [], []

for line in data:
    buttons_str = line[line.index(']') + 1: line.index('{')].strip()
    buttons = re.findall(r'\((.*?)\)', buttons_str)
    buttons_list.append(buttons)
    joltage = line[line.index('{') + 1: line.index('}')]
    joltage_list.append(joltage)

'''
Expected output format for buttons:
[['3', '1,3', '2', '2,3', '0,2', '0,1'],
 ['0,2,3,4', '2,3', '0,4', '0,1,2', '1,2,3,4'],
 ['0,1,2,3,4', '0,3,4', '0,1,2,4,5', '1,2']]

Expected output format for joltage:
['3,5,4,7', '7,5,12,7,2', '10,11,11,5,10,5']
'''


def min_presses_with_z3(buttons_strs, joltage_str):
    """
    Solve one machine using Z3:
        minimize sum x_j
        subject to A * x = target, x_j >= 0, integer
    buttons_strs: list like ['3', '1,3', ...]
    joltage_str: string like '3,5,4,7'
    """
    target = list(map(int, joltage_str.split(',')))
    k = len(target)          # number of counters
    m = len(buttons_strs)    # number of buttons

    # Build matrix A of size k x m
    # A[i][j] = 1 if button j increments counter i
    A = [[0] * m for _ in range(k)]
    for j, b_str in enumerate(buttons_strs):
        if b_str.strip() == '':
            continue
        indices = list(map(int, b_str.split(',')))
        for idx in indices:
            A[idx][j] += 1

    opt = Optimize()
    x = [Int(f"x_{j}") for j in range(m)]

    # Non negativity constraints
    for v in x:
        opt.add(v >= 0)

    # Counter equations: for each counter i
    for i in range(k):
        opt.add(Sum(A[i][j] * x[j] for j in range(m)) == target[i])

    total_presses = Sum(x)
    opt.minimize(total_presses)

    if opt.check() != sat:
        # No solution (should not happen for valid puzzle input)
        return None

    model = opt.model()
    return model.eval(total_presses).as_long()


reqd_button_presses = 0
for buttons, joltage in zip(buttons_list, joltage_list):
    presses = min_presses_with_z3(buttons, joltage)
    if presses is None:
        raise RuntimeError("No valid configuration for a machine")
    reqd_button_presses += presses

print(reqd_button_presses)
