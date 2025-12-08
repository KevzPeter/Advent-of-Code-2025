const fs = require('fs');
const path = require('path');

const inputFilePath = path.join(__dirname, 'sample-input.txt');

const input = fs.readFileSync(inputFilePath, 'utf-8').trim().split('\n');

const getPassword = (input) => {
    let currPos = 50;
    let password = 0;
    for (const line of input) {
        if (line.charAt(0) === 'L') {
            currPos = (currPos - parseInt(line.slice(1), 10)) % 100;
        }
        else {
            currPos = (currPos + parseInt(line.slice(1), 10)) % 100;
        }
        if (currPos == 0) {
            password++;
        }
        console.log(`After ${line}: currPos=${currPos}, password=${password}`);
    }
    return password;
}

console.log(getPassword(input));


