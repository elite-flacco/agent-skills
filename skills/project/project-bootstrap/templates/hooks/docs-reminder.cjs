#!/usr/bin/env node
// Advisory hook: warns when a subagent modified code but left docs untouched.
// Exits 0 always — non-blocking. Flip to exit(2) at bottom to make it blocking.

const { execSync } = require('child_process');

function clean(args) {
  try {
    execSync(`git diff --quiet HEAD ${args}`, { stdio: 'pipe' });
    return true;
  } catch {
    return false;
  }
}

const codeUnchanged = clean('');
if (codeUnchanged) process.exit(0);

const docPaths = ['README.md', 'CLAUDE.md', 'AGENTS.md']
  .filter((p) => {
    try {
      execSync(`git ls-files --error-unmatch ${p}`, { stdio: 'pipe' });
      return true;
    } catch {
      return false;
    }
  })
  .join(' ');

if (!docPaths) process.exit(0);

const docsUnchanged = clean(`-- ${docPaths}`);
if (docsUnchanged) {
  console.error(
    `[docs-reminder] Code changed but ${docPaths} untouched. ` +
      `If this task affected user-facing behavior, setup, architecture, or conventions, ` +
      `update docs before reporting done. Reply with "no doc impact" if none applies.`,
  );
  // To make blocking: process.exit(2);
}

process.exit(0);
