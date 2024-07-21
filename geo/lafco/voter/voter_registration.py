#! /usr/bin/env python
# Copyright 2024 John Hanley. MIT licensed.

from pathlib import Path

import pandas as pd

lafco_dir = Path("~/Desktop/lafco").expanduser()

_cols = [
    "LastName",
    # "MiddleName",
    "FirstName",
    # "NameSuffix",
    # "Gender",
    # "Ethnicity",
    "ResidenceAddress",
    "ResidenceCity",
    "ResidenceState",
    "ResidenceZipCode",
    # "PreDirection",
    # "StreetName",
    # "StreetSuffix",
    # "UnitAbbr",
    # "UnitNumber",
    # "MailAddress1",
    "MailAddress2",
    # "MailAddress3",
    # "MailAddress4",
    # "MailCity",
    # "MailState",
    # "MailZip",
    "PhoneNumber",
    "EmailAddress",
    # "BirthDate",
    # "RegistrationDate",
    "OriginalRegistrationDate",
    "LastUpdateDate",
    # "StatusCode",
    # "StatusReason",
    # "StateVoterStatus",
    # "PartyName",
    # "PartyAbbr",
    # "OtherParty",
    # "VBMProgramStatus",
    # "PrecinctID",
    "PrecinctName",
]


def get_menlo_registrations_df() -> pd.DataFrame:
    tsv = Path(lafco_dir / "2024Nov_EPASan_20240621_121126_KellyFergusson.txt")
    df = pd.read_csv(tsv, sep="\t", low_memory=False)

    # discard 19 useless columns
    df = df.dropna(axis=1, how="all")

    assert len(df) == len(df[df.DistrictName_1 == "East Palo Alto Sanitary District"])
    assert 9679 == len(df)
    df = df[df.MailAddress2 == "Menlo Park CA  94025"]
    assert 583 == len(df)

    return df[_cols]


def main() -> None:
    df = get_menlo_registrations_df()
    df = df[
        [
            "LastName",
            "FirstName",
            "ResidenceAddress",
            # "MailAddress2",
            "EmailAddress",
        ]
    ]
    with pd.option_context("display.max_rows", None):
        print(df)


if __name__ == "__main__":
    main()
