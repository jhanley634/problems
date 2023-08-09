#! /usr/bin/env python
# Copyright 2023 John Hanley. MIT licensed.

from pathlib import Path

from datasets import load_dataset
from huggingface_hub import hf_hub_download
from transformers import (
    AutoTokenizer,
    DataCollatorForSeq2Seq,
    T5ForConditionalGeneration,
    T5Tokenizer,
)
import evaluate
import numpy as np
import requests
import rouge_score


class Summarizer:
    CACHE_DIR = Path("/tmp/cache")

    @classmethod
    def _get_cache_filespec(cls, url: str) -> Path:
        cls.CACHE_DIR.mkdir(exist_ok=True)

        basename = Path(url).name
        if "." not in basename:
            basename += ".html"
        return cls.CACHE_DIR / basename

    def add_doc_url(self, url: str) -> None:
        fspec = self._get_cache_filespec(url)
        if not fspec.exists():
            ua = "Wget/1.21.4"
            resp = requests.get(url, headers={"User-Agent": ua})
            resp.raise_for_status()
            ct = resp.headers["Content-Type"]
            assert "text/html; charset=UTF-8" == ct, ct
            assert "UTF-8" == resp.encoding, resp.encoding
            # pp(dict(resp.headers))
            fspec.write_bytes(resp.content)

        self.add_doc(fspec.read_text(encoding="UTF-8"))

    def add_doc_file(self, in_file: Path) -> None:
        self.add_doc(in_file.read_text(encoding="UTF-8"))

    def add_doc(self, text: str) -> None:
        hf_hub_download(repo_id="google/pegasus-xsum", filename="config.json")
        billsum = load_dataset("billsum", split="ca_test")
        billsum = billsum.train_test_split(test_size=0.2)

        from pprint import pp

        # pp(billsum["train"][0])
        pp(list(billsum["test"][0].keys()))
        x = self.preprocess(billsum["train"][0])
        print(len(x), type(x))

        tokenized_billsum = billsum.map(self.preprocess, batched=True)
        print(tokenized_billsum, type(tokenized_billsum))
        rouge = evaluate.load("rouge")
        print(rouge, type(rouge))

    def preprocess(self, examples):
        checkpoint = "t5-small"
        tokenizer = AutoTokenizer.from_pretrained(checkpoint)
        prefix = "summarize: "

        inputs = [prefix + doc for doc in examples["text"]]
        model_inputs = tokenizer(inputs, max_length=1024, truncation=True)

        labels = tokenizer(
            text_target=examples["summary"], max_length=128, truncation=True
        )

        model_inputs["labels"] = labels["input_ids"]

        data_collator = DataCollatorForSeq2Seq(tokenizer=tokenizer, model=checkpoint)
        print(data_collator)

        return model_inputs

    # model = T5ForConditionalGeneration.from_pretrained("google/t5-small")
    # model = T5ForConditionalGeneration.from_pretrained("google/t5-v1_1-base")

    def compute_metrics(self, eval_pred):
        predictions, labels = eval_pred
        checkpoint = "t5-small"
        tokenizer = AutoTokenizer.from_pretrained(checkpoint)
        decoded_preds = tokenizer.batch_decode(predictions, skip_special_tokens=True)
        labels = np.where(labels != -100, labels, tokenizer.pad_token_id)
        decoded_labels = tokenizer.batch_decode(labels, skip_special_tokens=True)

        result = rouge_score.compute(
            predictions=decoded_preds, references=decoded_labels, use_stemmer=True
        )

        prediction_lens = [
            np.count_nonzero(pred != tokenizer.pad_token_id) for pred in predictions
        ]
        result["gen_len"] = np.mean(prediction_lens)

        return {k: round(v, 4) for k, v in result.items()}


def t5():
    gen_model_name = "t5-small"
    tokenizer = T5Tokenizer.from_pretrained(gen_model_name, legacy=False)
    model = T5ForConditionalGeneration.from_pretrained(gen_model_name)

    input_ids = tokenizer(
        "The <extra_id_0> walks in <extra_id_1> park", return_tensors="pt"
    ).input_ids
    labels = tokenizer(
        "<extra_id_0> cute dog <extra_id_1> the <extra_id_2>", return_tensors="pt"
    ).input_ids

    # the forward function automatically creates the correct decoder_input_ids
    loss = model(input_ids=input_ids, labels=labels).loss
    print(loss.item())


def translate():
    tokenizer = T5Tokenizer.from_pretrained("t5-small", legacy=False)
    model = T5ForConditionalGeneration.from_pretrained("t5-small")

    text = "translate English to German: The house is wonderful."
    input_ids = tokenizer(text, return_tensors="pt").input_ids
    outputs = model.generate(input_ids, max_new_tokens=20)
    print(tokenizer.decode(outputs[0], skip_special_tokens=True))


if __name__ == "__main__":
    translate()
