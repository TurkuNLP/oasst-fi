#!/usr/bin/env python3

import sys
import json

from argparse import ArgumentParser


def argparser():
    ap = ArgumentParser()
    ap.add_argument('lang')
    ap.add_argument('jsonl')
    return ap


def main(argv):
    args = argparser().parse_args(argv[1:])

    with open(args.jsonl) as f:
        for l in f:
            d = json.loads(l)
            if d['lang'] == args.lang:
                print(l, end='')


if __name__ == '__main__':
    sys.exit(main(sys.argv))
