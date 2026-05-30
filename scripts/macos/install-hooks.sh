#!/usr/bin/env bash
set -euo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source_root="$(cd "$script_dir/../.." && pwd)"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --source-root)
      source_root="$(cd "$2" && pwd)"
      shift 2
      ;;
    *)
      echo "Unknown argument: $1" >&2
      exit 2
      ;;
  esac
done

git -C "$source_root" config core.hooksPath .githooks
echo "Configured Git hooks path: .githooks"
