#! /usr/bin/env _TYPER_STANDARD_TRACEBACK=1 python
# Copyright 2024 John Hanley. MIT licensed.
# from https://codereview.stackexchange.com/questions/289102/tokenize-a-file
from collections import Counter
from collections.abc import Generator
from pathlib import Path
from typing import TextIO

from spacy.language import Language
from spacy.tokens.token import Token
import spacy
import spacy.tokens
import typer

punctuation = str.maketrans(
    '.,;:!?"()[]{}-',
    "              ",
)


def get_simple_words(line: str) -> Generator[str]:
    for wrd in line.translate(punctuation).split():
        word = wrd
        # strip possessives
        word = word.removesuffix("'")
        word = word.removesuffix("'s")

        if word.isalpha():
            yield word


def _get_spacy_tokens(nlp: Language, line: str) -> Generator[Token]:
    yield from (word for word in nlp(line.strip()) if word.is_alpha)


def spacy_wordlist(
    fin: TextIO,
    simp_out: TextIO,
    spcy_out: TextIO,
) -> None:
    english_model = "en_core_web_sm"
    try:
        nlp = spacy.load(english_model)
    except OSError:  # pragma: no cover
        # $ python -m spacy download en_core_web_sm
        spacy.cli.download(english_model)
        nlp = spacy.load(english_model)
    simp_seen = {"cannot"}
    spcy_seen = set()
    cnt: Counter[str] = Counter()
    dups = 0

    for line_num, orig_line in enumerate(fin):
        line = orig_line.lower()
        simp_out.write(f"\n{1 + line_num}\n\n")
        spcy_out.write(f"\n{1 + line_num}\n\n")

        for word in get_simple_words(line):
            if word not in simp_seen:
                simp_seen.add(word)
                simp_out.write(f"{word}\n")

        for token in _get_spacy_tokens(nlp, line):
            cnt[token.text] += 1
            if token.text in spcy_seen:
                dups += 1
            else:
                spcy_seen.add(token.text)
                spcy_out.write(f"{token}\n")

    cnt = Counter({k: v for k, v in cnt.items() if v >= 3})
    assert len(cnt) > 0
    # pp(sorted(cnt.items(), key=itemgetter(1)))
    # print(len(spcy_seen), dups)


def main(in_file: Path) -> None:
    with open(in_file) as fin:
        temp = Path("/tmp")
        simp_txt = temp / "bible_simple.txt"
        spcy_txt = temp / "bible_spacy.txt"
        with open(simp_txt, "w") as simp_out, open(spcy_txt, "w") as spcy_out:
            spacy_wordlist(fin, simp_out, spcy_out)


if __name__ == "__main__":
    typer.run(main)
