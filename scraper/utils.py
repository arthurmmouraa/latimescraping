import datetime
import re


def convert_abbreviated_date(date_text):
    month_dict = {
        "Jan.": "January",
        "Feb.": "February",
        "Dec.": "December",
        "Nov.": "November",
        "Oct.": "October",
        "Sept.": "September",
        "Aug.": "August",
    }
    date_text = date_text.split()
    if date_text[0] in month_dict:
        date_text[0] = month_dict[date_text[0]]
    date_text = " ".join(date_text)
    return date_text


def calculate_date_limit(months):
    today = datetime.date.today()
    first_day_of_month = today.replace(day=1)
    date_limit = first_day_of_month - datetime.timedelta(days=30 * months)
    return date_limit


def contains_money_amount(text):
    money_pattern = r"\$[\d,]+(\.\d+)?|\d+\s?(dollars?|USD)"
    return bool(re.search(money_pattern, text))


def count_search_phrase(text, search_phrase):
    return text.lower().count(search_phrase.lower())
