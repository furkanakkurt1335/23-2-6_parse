"""Adds telephone no number to the CSV muhtarlik data fetched from icisleri.gov.tr"""

import os
import json
import glob

import pandas as pd
from fuzzywuzzy import fuzz

villages = pd.read_csv(os.path.join("data/icisleri.csv"))
villages["Tel"] = ""
villages["Tel Kaynak"] = ""
villages["Eski Muhtar"] = ""
villages["Eski Muhtar Tel"] = ""

phone_folder = "data/tel/"  # folder containing csv files
files = [y for x in os.walk("data/tel") for y in glob.glob(os.path.join(x[0], "*.csv"))]

for file in files:  # for each csv file
    df = pd.read_csv(file)  # read csv file
    i = 1

    stats = {
        "city_mismatch": [],
        "district_mismatch": [],
        "village_mismatch": [],
    }

    for line in df.values:  # for each line in csv file
        max_ratio, max_city = 0, ""
        for city_t in villages["Il"].unique():  # for each city in entire data
            ratio_t = fuzz.token_set_ratio(
                line[0], city_t
            )  # get similarity of city (from csv with phone data) and city_t (from our current data)
            if ratio_t > max_ratio:  # if similarity is greater than max similarity
                max_ratio, max_city = (
                    ratio_t,
                    city_t,
                )  # update max similarity and max city

        if max_ratio > 80:  # if max similarity is greater than 80
            sel_city = max_city  # select city
        else:
            stats["city_mismatch"].append(line)
            continue
        rem_villages = villages[villages["Il"] == sel_city]

        max_ratio, max_district = 0, ""  # reset max similarity
        for district_t in villages[
            "Ilce"
        ].unique():  # for each district in selected city
            ratio_t = fuzz.token_set_ratio(
                line[1], district_t
            )  # get similarity of district (from csv with phone data) and district_t (from our current data)
            if ratio_t > max_ratio:  # if similarity is greater than max similarity
                max_ratio, max_district = (
                    ratio_t,
                    district_t,
                )  # update max similarity and max district

        if max_ratio > 80:  # if max similarity is greater than 80
            sel_district = max_district
        else:
            stats["district_mismatch"].append(line)
            continue
        rem_villages = rem_villages[rem_villages["Ilce"] == sel_district]

        max_ratio, max_village = 0, ""
        for village_t in rem_villages[
            "Muhtarlik"
        ].unique():  # for each village in selected district in selected city in entire data
            village_str = (
                village_t.replace("KÖYÜ", "").replace("MAH.", "").strip()
            )  # remove unnecessary words (but we learnt today that the fuzzy search seem not to be affected by these words)
            ratio_t = fuzz.token_set_ratio(
                line[2], village_str
            )  # get similarity of village (from csv with phone data) and village_t (from our current data)
            if ratio_t > max_ratio:  # if similarity is greater than max similarity
                max_ratio, max_village = (
                    ratio_t,
                    village_t,
                )  # update max similarity and max village

        if max_ratio > 80:  # if max similarity is greater than 80
            sel_village = max_village  # select village
        else:
            stats["village_mismatch"].append(line)
            continue

        match_t = rem_villages[rem_villages["Muhtarlik"] == sel_village]
        index = match_t.index.tolist()[0]
        if line[3] != "":  # if authority is not empty
            ratio_t = fuzz.token_set_ratio(
                line[3], match_t.iloc[0]["Muhtar"]
            )  # get similarity of village (from csv with phone data) and village_t (from our current data)

            if ratio_t > 80:
                villages.at[index, "Tel"] = line[4]
                villages.at[index, "Tel Kaynak"] = line[5]
            else:
                villages.at[index, "Eski Muhtar"] = line[3]
                villages.at[index, "Eski Muhtar Tel"] = line[4]
                villages.at[index, "Tel Kaynak"] = line[5]
        i += 1

    print(
        file,
        "City",
        len(stats["city_mismatch"]),
        "/",
        len(df),
        "District",
        len(stats["district_mismatch"]),
        "/",
        len(df),
        "Village",
        len(stats["village_mismatch"]),
        "/",
        len(df),
    )

villages.to_csv(os.path.join("data/icisleri_tel.csv"))
