#!/usr/bin/env python3

import sys
import json

from argparse import ArgumentParser

from datasets import load_dataset


def argparser():
    ap = ArgumentParser()
    ap.add_argument('dataset')
    ap.add_argument('subset')
    return ap


def main(argv):
    args = argparser().parse_args(argv[1:])

    dataset = load_dataset(args.dataset)
    for e in dataset[args.subset]:
        print(json.dumps(e, ensure_ascii=False))


if __name__ == '__main__':
    sys.exit(main(sys.argv))
