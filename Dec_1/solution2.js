const fs = require('fs');
const path = require('path');

const inputFilePath = path.join(__dirname, 'input.txt');

const input = fs.readFileSync(inputFilePath, 'utf-8').trim().split('\n');

// Positive modulo helper
const mod = (n, m) => ((n % m) + m) % m;

const getPassword = (input) => {
    let currPos = 50;  // dial starts at 50
    let password = 0;  // number of times a click lands on 0

    for (const line of input) {
        const dir = line[0];
        const steps = parseInt(line.slice(1), 10);

        if (dir === 'R') {
            // Moving right: positions are currPos + 1, ..., currPos + steps (mod 100)
            // Distance from currPos to next 0 going right:
            // if currPos = 0, the next 0 is after 100 steps; else after (100 - currPos) steps
            let d = (100 - currPos) % 100;
            if (d === 0) d = 100;

            if (steps >= d) {
                // First hit at step d, then every 100 steps after that
                password += 1 + Math.floor((steps - d) / 100);
            }

            currPos = mod(currPos + steps, 100);
        } else if (dir === 'L') {
            // Moving left: positions are currPos - 1, ..., currPos - steps (mod 100)
            // Distance from currPos to previous 0 going left:
            // if currPos = 0, first 0 again after 100 steps (we ignore starting position)
            // else after currPos steps
            let d = (currPos === 0) ? 100 : currPos;

            if (steps >= d) {
                // First hit at step d, then every 100 steps after that
                password += 1 + Math.floor((steps - d) / 100);
            }

            currPos = mod(currPos - steps, 100);
        } else {
            throw new Error(`Invalid direction in line: ${line}`);
        }
    }

    return password;
};


console.log(getPassword(input));


