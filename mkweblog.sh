#!/usr/bin/env bash
set -euo pipefail

usage() {
    cat <<EOF
Usage: $0 SLUG "Post Title" ["tag1, tag2"]

Create a new Markdown post at weblog/SLUG.md.

Arguments:
    SLUG        Lowercase kebab-case filename without .md
    Post Title  Title used for the top-level Markdown heading
    tags        Optional comma-separated tag list
EOF
}

if [[ "${1:-}" == "-h" || "${1:-}" == "--help" ]]; then
    usage
    exit 0
fi

if [[ $# -lt 2 || $# -gt 3 ]]; then
    usage >&2
    exit 2
fi

filename=$1
title=$2
tags="${3:-}"
path="weblog/$filename.md"

if [[ -z "$filename" ]]; then
    echo "Error: SLUG cannot be empty." >&2
    usage >&2
    exit 2
fi

if [[ ! "$filename" =~ ^[a-z0-9]+(-[a-z0-9]+)*$ ]]; then
    echo "Error: SLUG must be lowercase kebab-case without .md." >&2
    usage >&2
    exit 2
fi

if [[ -z "$title" ]]; then
    echo "Error: Post Title cannot be empty." >&2
    usage >&2
    exit 2
fi

if [[ -e "$path" ]]; then
    echo "Error: $path already exists." >&2
    exit 1
fi

if [[ "$tags" != "" ]]; then
    tags_header="\nTags: $tags"
else
    tags_header=""
fi

tee "$path" <<EOF
---
Date: $(date +"%Y-%m-%d %H:%M")$(printf "%b" "$tags_header")
---

# $title

This is a new blog post. You can author it in _Markdown_, which is **awesome**.
EOF
