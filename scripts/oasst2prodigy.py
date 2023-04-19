#!/usr/bin/env python3

# Format translated oasst1 corpus JSONL for Prodigy (https://prodi.gy/)

import sys
import json

from html import escape
from argparse import ArgumentParser


def argparser():
    ap = ArgumentParser()
    ap.add_argument('--initial-only', action='store_true')
    ap.add_argument('jsonl')
    return ap


def main(argv):
    args = argparser().parse_args(argv[1:])

    output_count, deleted_count, nolabels_count, skipped_count = 0, 0, 0, 0
    
    with open(args.jsonl) as f:
        for l in f:
            d = json.loads(l)

            # skip?
            if d['deleted']:
                deleted_count += 1
                continue
            elif d['labels'] is None:
                nolabels_count += 1
                continue
            elif args.initial_only and d['parent_id'] is not None:
                skipped_count += 1
                continue
            
            # id and texts
            id_ = d['message_id']
            text = d['text']
            orig_text = d['orig_text']
            
            # labels
            keys = list(sorted(d['labels'].keys()))
            assert keys == ['count', 'name', 'value'], f'unexpected keys {keys}'

            lengths = [len(d['labels'][k]) for k in d['labels']]
            assert len(set(lengths)) == 1, 'label len mismatch'
            length = lengths[0]

            label_strs = []
            for i in range(length):
                name = d['labels']['name'][i]
                value = d['labels']['value'][i]
                count = d['labels']['count'][i]
                label_strs.append(f'{name}: {value:.0%} ({count})')
            labels = '<b>Labels</b>: ' + '\n'.join(label_strs)

            # role
            text_role = d['role']
            if d['parent_id'] is None:
                text_role += ' (initial message)'
            else:
                text_role += ' (response)'
            
            # make html
            html = ''.join([
                '<div class="text-role">', escape(text_role), '</div>'
                '<div class="original-text">', escape(orig_text), '</div>'
                '<div class="translated-text">', escape(text), '</div>'
                '<div class="labels">', labels, '</div>'
            ])

            # output
            o = {
                "id": id_,
                "html": html,
                "meta": { "id": id_ },
            }
            print(json.dumps(o, ensure_ascii=False))

            output_count += 1
            
    print(f'output {output_count}', file=sys.stderr)
    print(f'excluded {deleted_count} marked "deleted"', file=sys.stderr)
    print(f'excluded {nolabels_count} missing "labels"', file=sys.stderr)
    print(f'skipped {skipped_count} due to command-line args"', file=sys.stderr)


if __name__ == '__main__':
    sys.exit(main(sys.argv))
