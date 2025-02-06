import { readdirSync } from 'fs';
import { join } from 'path'
const __dirname = import.meta.dirname;

function getCoreList() {
    let output = []
    const files = readdirSync(join(__dirname, 'retroarch'));
    for (let file of files) {
        if (file.includes('_libretro.js')) {
            output.push(file.replace('_libretro.js', ''));
        }
    }
    return output;
}

export { getCoreList };
