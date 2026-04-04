#!/usr/bin/env python3
# Reconstructed approximation of an early "just make it work" helper.
# This is not claimed to be the exact original file.

import json
import sys
from pathlib import Path


ATLAS_PREFIX = "https://www.openanatomy.org/atlases/macbioidi/mauritania/thorax-2020-11-15/"


def main():
    har = json.loads(Path(sys.argv[1]).read_text())
    assets = {}
    for entry in har["log"]["entries"]:
        req = entry["request"]
        res = entry["response"]
        if req["method"] != "GET":
            continue
        if not req["url"].startswith(ATLAS_PREFIX):
            continue
        if "/viewer/" in req["url"]:
            continue
        if res["status"] != 200:
            print("bad response", req["url"], res["status"])
            sys.exit(1)
        body = res["content"]["text"]
        assets[req["url"]] = body
    print("found", len(assets), "files")


if __name__ == "__main__":
    main()
