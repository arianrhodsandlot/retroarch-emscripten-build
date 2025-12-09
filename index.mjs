import { readdirSync } from 'fs';
import { join } from 'path'
const __dirname = import.meta.dirname;

function getCoreList() {
    let output = []
    const files = readdirSync(join(__dirname, 'retroarch'));
    for (let file of files) {
        if (file.includes('_libretro.zip')) {
            output.push(file.replace('_libretro.zip', ''));
        }
    }
    return output;
}

export { getCoreList };
