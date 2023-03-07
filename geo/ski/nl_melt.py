# Copyright 2023 John Hanley. MIT licensed.

# https://stackoverflow.com/questions/75654727/merge-two-dataframes-on-variables-of-the-same-data-type
import pandas as pd


def woz_melt():
    df1, df2 = _get_dataframes()

    assert set(df1.stadsdeel) == set(df2.stadsdeel)  # Yup, the spellings match!

    print(common_years := set(df1.year) & set(df2.year))
    df1 = df1[df1.year.isin(common_years)]
    df2 = df2[df2.year.isin(common_years)]

    print(df1.merge(df2, how="left", on=["stadsdeel", "year"]).dropna())


def _get_dataframes():
    woz_waarde = "https://raw.githubusercontent.com/uvacw/teaching-bdaca/main/12ec-course/week03/exercises/wozwaarde-clean.csv"
    df1 = pd.read_csv(woz_waarde)
    df1 = df1.melt(
        id_vars=["wijk", "code", "stadsdeel"],
        var_name="year",
        value_name="wozwaarde",
    )

    jaarboek = "https://cms.onderzoek-en-statistiek.nl/uploads/2021_jaarboek_2112_28485510ff.xlsx"
    df2 = pd.read_excel(jaarboek, skiprows=2, skipfooter=2)
    df2 = df2.drop([0, 9])
    df2["stadsdeel"] = df2["stadsdeel"].apply(lambda s: s.split()[-1])
    df2 = df2.melt(id_vars="stadsdeel", var_name="year", value_name="population")

    df1["year"] = df1["year"].map(int)
    df2["year"] = df2["year"].map(int)
    df1["stadsdeel"] = df1["stadsdeel"].map(str)
    df2["stadsdeel"] = df2["stadsdeel"].map(str)

    return df1, df2


if __name__ == "__main__":
    woz_melt()
