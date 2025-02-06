import assert from 'node:assert/strict';
import { getCoreList } from '../index.mjs';

const cores = getCoreList();

assert.ok(cores.includes('fceumm'));
assert.ok(cores.length > 10);
