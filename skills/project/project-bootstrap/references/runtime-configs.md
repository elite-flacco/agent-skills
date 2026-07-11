# Runtime hook configs (Claude Code / ZCode / Codex)

The verify-gate hook is the same command in every runtime:

```bash
git diff --quiet HEAD || npm run verify || exit 2
```

Only the **config wrapper**, the **available hook events**, the **timeout unit**,
and the **enablement flag** differ. Detect which runtime(s) are installed and
copy the matching template(s) from `templates/`.

## At a glance

| | Claude Code | ZCode | Codex |
|---|---|---|---|
| Config path | `.claude/settings.json` | `.zcode/config.json` | `.codex/hooks.json` |
| Wrapper | `{ "hooks": { <Event>: [...] } }` | `{ "hooks": { "enabled": true, "events": { <Event>: [...] } } }` | `{ "hooks": { <Event>: [...] } }` |
| `SubagentStop` | ✅ | ❌ (not a supported event) | ✅ |
| `Stop` | ✅ | ✅ | ✅ |
| `timeout` unit | **milliseconds** | **seconds** | **seconds** |
| Enablement | on by default | needs `"enabled": true` | on by default; needs `/hooks` trust review |
| Memory file | `CLAUDE.md` (reads `AGENTS.md` too) | `AGENTS.md` | `AGENTS.md` |

`Stop` is the **only** event all three support, so it's the portable baseline.
`SubagentStop` adds per-subagent gating (verify re-runs after each subagent
finishes — valuable for `superpowers:subagent-driven-development`); include it
on Claude Code and Codex where available. ZCode has no equivalent, so its gate
fires at turn end — CI remains the per-commit backstop there.

## The three config blocks

### Claude Code → `.claude/settings.json`

Timeouts in **milliseconds**. `SubagentStop` + `Stop` both wired.

```json
{
  "hooks": {
    "SubagentStop": [
      {
        "matcher": "*",
        "hooks": [
          {
            "type": "command",
            "command": "git diff --quiet HEAD || npm run verify || exit 2",
            "timeout": 180000
          }
        ]
      }
    ],
    "Stop": [
      {
        "matcher": "*",
        "hooks": [
          {
            "type": "command",
            "command": "git diff --quiet HEAD || npm run verify || exit 2",
            "timeout": 180000
          }
        ]
      }
    ]
  }
}
```

### ZCode → `.zcode/config.json`

Timeouts in **seconds**. `Stop` only (no `SubagentStop` event). Requires
`"enabled": true`. Omit the matcher to match all tools.

```json
{
  "hooks": {
    "enabled": true,
    "events": {
      "Stop": [
        {
          "hooks": [
            {
              "type": "command",
              "command": "git diff --quiet HEAD || npm run verify || exit 2",
              "timeout": 180
            }
          ]
        }
      ]
    }
  }
}
```

### Codex → `.codex/hooks.json`

Timeouts in **seconds** (default 600 if omitted). `SubagentStop` + `Stop` both
wired. **Codex skips hooks until reviewed** — after copying, the user must run
`/hooks` and trust the new hook before it fires.

```json
{
  "hooks": {
    "SubagentStop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "git diff --quiet HEAD || npm run verify || exit 2",
            "timeout": 180
          }
        ]
      }
    ],
    "Stop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "git diff --quiet HEAD || npm run verify || exit 2",
            "timeout": 180
          }
        ]
      }
    ]
  }
}
```

## Why `|| exit 2`

All three runtimes treat exit code `2` from a `Stop`/`SubagentStop` hook as
"surface this to the agent and continue" (block-and-continue with the failure
output as context). A plain non-zero exit is treated as an error and may be
silently swallowed. The `exit 2` ensures a failing `verify` is actually fed
back to the agent rather than lost.

## Merging into an existing config

If the target config already has hooks, **merge the event arrays** — don't
overwrite the file. Append the verify-gate entry to the existing
`Stop` / `SubagentStop` array(s). For ZCode, preserve the existing `enabled`
flag (it must stay `true`).
