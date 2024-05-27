#! /usr/bin/env python
# Copyright 2023 John Hanley. MIT licensed.
# from https://codereview.stackexchange.com/questions/284448/matching-from-a-big-list-of-keywords
from pprint import pp
import re

from typing_extensions import Any
import regex
import unidecode


class Drug:
    def __init__(self, name: str, atc: str, position: tuple[int, int] | None):
        # normalize name make it capitalize
        self.name = re.escape(name.upper())
        self.atc = atc
        self.start = position[0] if position is not None else None
        self.stop = position[1] if position is not None else None

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Drug):
            return False
        return self.name == other.name and self.atc == other.atc

    def __hash__(self) -> int:
        return hash((self.name, self.atc))

    def __repr__(self) -> str:
        return f"Drug({self.name}, {self.atc}, {self.start, self.stop}))"


NUM_DRUGS = 150_000
US_DRUGS = [Drug(f"MED{i:05d}", f"{i}", None) for i in range(NUM_DRUGS)]


def _extract_drugs_from_prescription_text(prescription_text: str) -> list[Drug]:
    # normalize prescription text (remove accents)
    normalized_prescription_text = unidecode.unidecode(prescription_text)

    # remove non word character
    normalized_prescription_text = re.sub(r"\W+", " ", normalized_prescription_text)

    # For every occurrence of a drug's name in the prescription text
    # it will append a Drug() object with match's details in a list
    matched_drugs = []
    for drug in US_DRUGS:
        for match in regex.finditer(
            re.escape(drug.name), re.escape(normalized_prescription_text), re.IGNORECASE
        ):
            matched_drugs.append(Drug(drug.name, drug.atc, match.span()))

    # Will clean up the matches list from duplicates substring
    # ex: 'DOLIPRANE' and 'DOLIPRANE CODEINE'
    # if they start at the same point, first one is removed
    matched_drugs_without_substring = []
    for match in matched_drugs:
        if [
            m
            for m in matched_drugs
            if m.start <= match.start <= m.stop and len(match.name) < len(m.name)
        ]:
            pass
        else:
            matched_drugs_without_substring.append(match)

    # remove duplicates
    return list(set(matched_drugs_without_substring))


def main() -> None:
    # an ATC, https://en.wikipedia.org/wiki/Anatomical_Therapeutic_Chemical_Classification_System
    # vitamin_c = "A11GA01"

    prescription_text = (
        "- TEST -  medication names like"
        " MED1, MED2, MED3, MED00004, MED00005."
        " End of the test #$%^"
    )
    normalized_prescription_text = re.escape(
        unidecode.unidecode(prescription_text.upper())
    )
    _extract_drugs_from_prescription_text(prescription_text)

    matched_drugs = []
    for DRUG in US_DRUGS:
        for match in regex.finditer(DRUG.name, normalized_prescription_text):
            matched_drugs.append(Drug(DRUG.name, DRUG.atc, match.span()))
    pp(matched_drugs)


if __name__ == "__main__":
    main()
