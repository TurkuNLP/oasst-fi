#!/usr/bin/env python3

import docx
import sys
import json
import tqdm

from logging import warning
from argparse import ArgumentParser


def argparser():
    ap = ArgumentParser()
    ap.add_argument('jsonl')
    ap.add_argument('docxs', nargs="+")
    ap.add_argument('--include-original', action='store_true')
    return ap


def load_original_data(fn):
    data = []
    with open(fn) as f:
        for l in f:
            data.append(json.loads(l))
    return data


def yield_translations(fnames):
    expected_doc_idx = 0

    for fname in tqdm.tqdm(fnames):
        d = docx.Document(fname)

        for p in d.paragraphs:
            if p.runs[0].bold and p.text.startswith("Asiakirja "):
                doc_idx = int(p.text[len("Asiakirja "):])
                if expected_doc_idx != doc_idx:
                    warning(f'index mismatch: {expected_doc_idx} != {doc_idx}')
                expected_doc_idx += 1
            else:
                yield p.text


def main(argv):
    args = argparser().parse_args(argv[1:])

    original_data = load_original_data(args.jsonl)

    for i, t in enumerate(yield_translations(args.docxs)):
        d = original_data[i]

        if args.include_original:
            d['orig_text'] = d['text']

        d['text'] = t

        print(json.dumps(d, ensure_ascii=False))
    count = i + 1

    if count != len(original_data):
        print(f'''
##############################################################################
#
# WARNING: incomplete: got {count} documents, original is {len(original_data)}
#
##############################################################################
''', file=sys.stderr)


if __name__=="__main__":
    sys.exit(main(sys.argv))
