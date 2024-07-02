import datetime
import re


def convert_abbreviated_date(date_text):
    """
    Converts a date with abbreviated month to full month name.

    Args:
        date_text (str): Date in abbreviated format, e.g., "Jan. 5, 2024".

    Returns:
        str: Converted date in full month name format, e.g., "January 5, 2024".
    """
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
    """
    Calculates the date limit based on the number of months ago from the first day of the current month.

    Args:
        months (int): Number of months to go back.

    Returns:
        datetime.date: A date object representing the calculated date limit.
    """
    today = datetime.date.today()
    first_day_of_month = today.replace(day=1)
    date_limit = first_day_of_month - datetime.timedelta(days=30 * months)
    return date_limit


def contains_money_amount(text):
    """
    Checks if a text contains a money amount.

    Args:
        text (str): Text to search for money amount.

    Returns:
        bool: True if the text contains a money amount, False otherwise.
    """
    money_pattern = r"\$[\d,]+(\.\d+)?|\d+\s?(dollars?|USD)"
    return bool(re.search(money_pattern, text))


def count_search_phrase(text, search_phrase):
    """
    Counts the number of occurrences of a search phrase in a text, ignoring case sensitivity.

    Args:
        text (str): Text to search for occurrences.
        search_phrase (str): Phrase to be counted in the text.

    Returns:
        int: Number of times the search phrase occurs in the text.
    """
    return text.lower().count(search_phrase.lower())
