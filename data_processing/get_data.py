from datetime import datetime

import pandas as pd

from app import cache
from wordcloud import WordCloud, STOPWORDS
import re


@cache.memoize(timeout=3600)
def get_month_list():
    month_list = ["January", "February", "March", "April", "May", "June"]
    month_list = [{"label": month, "value": month} for month in month_list]
    return month_list


@cache.memoize(timeout=3600)
def get_category_list():
    df = load_csv("files/911_data.csv")
    category_list = []
    dispo_list = df["FINAL_DISPO"].unique().tolist()
    dispo_list.sort()
    category_list = [{"label": item, "value": item} for item in dispo_list]
    return category_list


@cache.memoize(timeout=3600)
def load_csv(file_name):
    df = pd.read_csv(file_name)
    return df


@cache.memoize(timeout=3600)
def load_data(file_name):
    df = load_csv(file_name)
    #df["Month"] = pd.to_datetime(df["OFFENSE_DATE"]).dt.strftime("%B")
    #df["Month_Number"] = pd.to_datetime(df["OFFENSE_DATE"]).dt.strftime("%m")
    #df["OFFENSE_TIME"] = df["OFFENSE_TIME"].replace({"PT": ""})
    #df["Offence Time"] = df.apply(lambda row: format_date(row), axis=1)
    #df["Month"] = pd.to_datetime(df["OFFENSE_DATE"]).dt.strftime("%B")
    #df["Weekday"] = pd.to_datetime(df["OFFENSE_DATE"]).dt.strftime("%A")
    return df


def format_date(row):
    pattern = "\d+"
    date = row["OFFENSE_TIME"]
    match_list = re.findall(pattern, date)
    while len(match_list) <= 2:
        match_list.insert(0, "00")
    new_match_list = ["{:02d}".format(int(i)) for i in match_list]
    new_time = ":".join(new_match_list)
    new_time = datetime.strptime(new_time, "%H:%M:%S").hour
    return new_time


@cache.memoize(timeout=3600)
def get_call_data(month, category):
    df = load_csv("files/911_data.csv")
    if month:
        selected_months = []
        if isinstance(month, list):
            selected_months = month
        else:
            selected_months.append(month)
        df = df[df["Month"].isin(selected_months)]
    if category:
        selected_categories = []
        if isinstance(category, list):
            selected_categories = category
        else:
            selected_categories.append(category)
        df = df[df["FINAL_DISPO"].isin(selected_categories)]
    #df["Month"] = pd.to_datetime(df["OFFENSE_DATE"]).dt.strftime("%B")
    #df["Weekday"] = pd.to_datetime(df["OFFENSE_DATE"]).dt.strftime("%A")
    return df


def get_word_cloud(call_type_list):
    custom_stop_words = {"W", "HI", "18YRS", "LIC", "1091AB", " Combined", "447A", "Violation", "Vehicle", "Stop",
                         "Parking", "Female", "check", "unk", "calls", "svrn", "type", "amb", "run", "call", "person"}
    stop_words = STOPWORDS
    stop_words.update(custom_stop_words)
    call_type_list = list(set(call_type_list))
    new_call_type_list = [i for i in call_type_list if isinstance(i, str)]
    words = " ".join(new_call_type_list)
    words = words.upper()
    word_cloud = WordCloud(width=800,
                           height=400,
                           random_state=21,
                           max_font_size=300,
                           background_color="#c4e2ff",
                           stopwords=stop_words)
    if words:
        word_cloud.generate(words)
    else:
        word_cloud.generate("No data")

    return word_cloud
