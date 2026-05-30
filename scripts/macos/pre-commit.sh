#!/usr/bin/env bash
set -euo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source_root="$(cd "$script_dir/../.." && pwd)"
manifest_path="$source_root/manifest.json"

echo "Staging skill file changes..."
git -C "$source_root" add -- skills

echo "Syncing skill manifest..."
"$script_dir/sync-manifest.sh" --source-root "$source_root"

echo "Refreshing skill discovery links..."
"$script_dir/link.sh" --source-root "$source_root"

echo "Validating managed skills..."
"$script_dir/validate.sh" --source-root "$source_root"

git -C "$source_root" add -- "$manifest_path"
echo "Pre-commit skill checks passed."
