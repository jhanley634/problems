#! /usr/bin/env python
# Copyright 2023 John Hanley. MIT licensed.
from pathlib import Path
from pprint import pp
from typing import Any

from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    CodeGenTokenizerFast,
    PhiForCausalLM,
    T5ForConditionalGeneration,
    T5Tokenizer,
)
import requests

CACHE_DIR = Path("/tmp/cache")


def get_cache_filespec(url: str) -> Path:
    CACHE_DIR.mkdir(exist_ok=True)

    basename = Path(url).name
    if "." not in basename:
        basename += ".html"
    return CACHE_DIR / basename


class Summarizer:
    def add_doc_url(self, url: str, verbose: bool = True) -> str:
        fspec = get_cache_filespec(url)
        if not fspec.exists():
            ua = "Wget/1.21.4"
            resp = requests.get(url, headers={"User-Agent": ua})
            resp.raise_for_status()
            ct = resp.headers["Content-Type"]
            assert "text/html; charset=UTF-8" == ct, ct
            assert "UTF-8" == resp.encoding, resp.encoding
            if verbose:
                pp(dict(resp.headers))
            fspec.write_bytes(resp.content)

        return self.add_doc(fspec.read_text(encoding="UTF-8"))

    def add_doc_file(self, in_file: Path, **kwargs: Any) -> str:
        return self.add_doc(in_file.read_text(encoding="UTF-8"), **kwargs)

    @staticmethod
    def add_doc(
        text: str,
        limit: int = 24,
        verbose: bool = False,
    ) -> str:
        text = "summarize: " + text[:1800]
        if verbose:
            print(text, "\n\n\n")

        tokenizer, model = get_llm_model()
        input_ids = tokenizer(text, return_tensors="pt").input_ids
        outputs = model.generate(input_ids, max_new_tokens=limit)
        return str(tokenizer.decode(outputs[0], skip_special_tokens=True))

    # model = T5ForConditionalGeneration.from_pretrained("google/t5-v1_1-base")


def get_t5_model() -> tuple[T5Tokenizer, T5ForConditionalGeneration]:
    t5 = "t5-small"
    tokenizer = T5Tokenizer.from_pretrained(t5, legacy=False)
    assert isinstance(tokenizer, T5Tokenizer), type(tokenizer)

    model = T5ForConditionalGeneration.from_pretrained(t5)
    assert isinstance(model, T5ForConditionalGeneration), type(model)

    return tokenizer, model


def get_llm_model() -> tuple[CodeGenTokenizerFast, Any]:
    phi = "microsoft/phi-1.5"
    tokenizer = AutoTokenizer.from_pretrained(phi)
    assert isinstance(tokenizer, CodeGenTokenizerFast), type(tokenizer)

    model = AutoModelForCausalLM.from_pretrained(phi)
    assert isinstance(model, PhiForCausalLM), type(model)

    return tokenizer, model


def translate() -> None:
    tokenizer, model = get_llm_model()
    text = "translate English to German: The house is wonderful."
    input_ids = tokenizer(text, return_tensors="pt").input_ids
    outputs = model.generate(input_ids, max_new_tokens=20)
    print(tokenizer.decode(outputs[0], skip_special_tokens=True))


if __name__ == "__main__":
    translate()
