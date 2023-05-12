# oasst-fi

Open Assistant dataset translated to Finnish

## Processing

Get original data

```
mkdir original-data
python3 scripts/get_data.py OpenAssistant/oasst1 train > original-data/train.jsonl
python3 scripts/get_data.py OpenAssistant/oasst1 validation > original-data/validation.jsonl
```

(Full data not committed due to size)

Filter to English subset

```
python3 scripts/filter_by_lang.py en original-data/train.jsonl > original-data/en-train.jsonl
python3 scripts/filter_by_lang.py en original-data/validation.jsonl > original-data/en-validation.jsonl
```

Convert text from JSONL files to DOCX

```
python3 scripts/jsonl2doc.py original-data/en-train.jsonl doc-in
python3 scripts/jsonl2doc.py original-data/en-validation.jsonl doc-in
```

Translate DOCX files from `doc-in/` using [DeepL](<https://www.deepl.com/>) and save outputs in `doc-out/`.

Convert back to JSONL

```
python3 scripts/doc2jsonl.py \
    --include-original \
    original-data/en-validation.jsonl \
    doc-out/en-validation-*.docx \
    > oasst1-fi-validation.jsonl

python3 scripts/doc2jsonl.py \
    --include-original \
    original-data/en-train.jsonl \
    doc-out/en-train-*.docx \
    > oasst1-fi-train.jsonl
```

## License

This dataset is licensed under the [Apache License, Version 2.0](https://www.apache.org/licenses/LICENSE-2.0).

Note that under the [DeepL terms and conditions](https://www.deepl.com/en/pro-license), this data may not be used to develop, market or train a machine
translation algorithm.
