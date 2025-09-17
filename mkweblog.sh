#!/usr/bin/env bash
set -euo pipefail

filename=$1
title=$2
tags="${3:-}"

if [[ "$tags" != "" ]]; then
    tags_header="\nTags: $tags"
else
    tags_header=""
fi

tee weblog/"$filename".md <<EOF
---
Date: $(date +"%Y-%m-%d %H:%M")$(printf "$tags_header")
---

# $title

This is a new blog post. You can author it in _Markdown_, which is **awesome**.
EOF
