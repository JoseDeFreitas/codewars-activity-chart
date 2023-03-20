import requests
import calendar
from datetime import datetime, timedelta
import json
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/{username}", response_class=HTMLResponse)
async def get_user(
    request: Request, username: str, year: str = str(datetime.now().year), aspect: str = "light"
    ):

    r_url = f"https://www.codewars.com/api/v1/users/{username}/code-challenges/completed"
    r_params = {
        "page": 0
    }

    response = None
    try:
        response = requests.get(url=r_url, params=r_params).json()
    except:
        print("There was a problem while connecting to the API.")
        return

    if response["totalItems"] == 0:
        return templates.TemplateResponse(
            "nodata.html",
            {
                "request": request,
                "data": "<p id=\"not-found\">No data was found for this user.</p>",
            }
        )
    
    n_pages = response["totalPages"]

    month_names = get_external_data()
    edit_days, edit_count = get_edit_days(response, r_url, r_params, n_pages)
    streak_edits = calculate_streak(year, edit_days)
    day_levels = get_day_levels(edit_days)

    colour_mode = f"/{aspect}.css"

    edit_data = format_data_html(year, month_names, edit_days, day_levels)

    return templates.TemplateResponse(
        "userchart.html",
        {
            "request": request,
            "username": username,
            "year": year,
            "total": edit_count,
            "streak": streak_edits,
            "aspect": colour_mode,
            "data": edit_data
        }
    )


def get_external_data() -> tuple:
    """Reads the "external.json" file and retrieves their objects

    Returns
    -------
    tuple[dict]
        map between numbers and month names
    """

    with open("external.json", "r") as json_read:
        json_data = json.load(json_read)

    return json_data["month-names"]


def get_edit_days(response: dict, r_url: str, r_params: str, n_pages: int) -> tuple:
    """Retrieves the days of edits and the number of edits

    Parameters
    ----------
    response : dict
        The first response taken from the Mediawiki Action API
    r_url : str
        The URL of the response
    r_params : str
        The parameters to attach to the response

    Returns
    -------
    tuple[dict, int]
        a dict with the dates the user made at least one edit and the
        quantity of the edits and a number with the total count of
        edits made
    """

    edit_days = {}

    for i in range(n_pages):
        for completion in response["data"]:
            date = completion["completedAt"][:10]

            if date not in edit_days.keys():
                edit_days[date] = 1
            else:
                edit_days[date] = edit_days[date] + 1

        r_params["page"] = i + 1
        response = requests.get(url=r_url, params=r_params).json()

    edit_count = sum(edit_days.values())

    return edit_days, edit_count


def calculate_streak(year: str, edit_days: dict) -> str:
    """Calculates de current or the longest streak made

    Parameters
    ----------
    year : str
        The year the user chose
    edit_days : dict
        The dict with the days and count of edits the user made
        for each of them

    Returns
    -------
    str
        the text with the number of the current or the longest
        streak
    """

    streak_number = 0
    streak_edits = ""

    if year == str(datetime.now().year):
        last = datetime.now()
        while 1:
            if str(last)[:10] in edit_days:
                streak_number += 1
                last = last - timedelta(days=1)
            else:
                break

        streak_edits = f"Current streak: {streak_number}"
    else:
        streak_count = 0
        last = datetime.strptime(list(edit_days.keys())[0], "%Y-%m-%d")
        for day in range(len(list(edit_days.keys()))):
            if str(last)[:10] in edit_days:
                streak_count += 1
                last = last - timedelta(days=1)

                if (streak_number < streak_count):
                    streak_number = streak_count
            else:
                last = datetime.strptime(list(edit_days.keys())[day], "%Y-%m-%d") - timedelta(days=1)
                streak_count = 1

        streak_edits = f"Longest streak: {streak_number}"

    return streak_edits


def get_day_levels(edit_days: dict) -> list:
    """Calculates the numbers to use as breakpoints for the colours

    Parameters
    ----------
    edit_days : dict
        The dict with the days and count of edits the user made
        for each of them

    Returns
    -------
    list
        the numbers that the HTML classes should use to decide
        which tone of colour to apply to the square
    """

    day_levels = []
    max_edit = max(edit_days.values())
    last_number = max_edit

    for _ in range(5):
        last_number = last_number - (max_edit / 6)
        day_levels.append(int(last_number))

    return day_levels


def format_data_html(year: str, month_names: dict, edit_days: dict, day_levels: list) -> str:
    """Formats the data using HTML tags and attributes

    Parameters
    ----------
    year : str
        The year the user chose
    month_names : dict
        A dict with the map between numbers and month names
    edit_days : dict
        The dict with the days and count of edits the user made
        for each of them
    day_levels : list
        List of numbers to serve as breakpoints for the colours
        of the squares

    Returns
    -------
    str
        the HTML string with all the information
    """

    edit_data = ""
    year_days = calendar.Calendar().yeardayscalendar(int(year), width=12)

    month_count = 1
    for month in year_days[0]:
        lower_month = month_names[str(month_count)].lower()

        edit_data += f"<div id=\"{lower_month}\" class=\"month\">"
        edit_data += f"<h2 class=\"month-title\">{month_names[str(month_count)]}</h2>"
        edit_data += "<div class=\"month-container\">"

        week_count = 1
        for week in month:
            edit_data += f"<div id=\"{lower_month}-week-{week_count}\" class=\"week\">"

            for day in week:
                number_day = f"{year}-{str(month_count).zfill(2)}-{str(day).zfill(2)}"
                char_day = f"{month_names[str(month_count)][:3]} {day}, {year}"

                day_transparency = "no-transparent"
                edit_level = "day-level-0"
                tooltip = f"No contributions on {char_day}"

                if day == 0:
                    day_transparency = "yes-transparent"
                    edit_level = ""
                    tooltip = ""

                if number_day in edit_days:
                    tooltip = f"{edit_days[number_day]} contributions on {char_day}"

                    if edit_days[number_day] >= day_levels[0]:
                        edit_level = "day-level-6"
                    elif edit_days[number_day] >= day_levels[1]:
                        edit_level = "day-level-5"
                    elif edit_days[number_day] >= day_levels[2]:
                        edit_level = "day-level-4"
                    elif edit_days[number_day] >= day_levels[3]:
                        edit_level = "day-level-3"
                    elif edit_days[number_day] >= day_levels[4]:
                        edit_level = "day-level-2"
                    elif edit_days[number_day] < day_levels[4] and edit_days[number_day] > 1:
                        edit_level = "day-level-1"
                    elif edit_days[number_day] == 1:
                        edit_level = "day-level-1"
                        tooltip = f"{edit_days[number_day]} contribution on {char_day}"

                edit_data += f"""
                <div class=\"day {edit_level} {day_transparency}\">
                    <span class=\"tooltip-text\">{tooltip}</span>
                </div>
                """

            edit_data += "</div>"
            week_count += 1

        edit_data += "</div>"
        edit_data += "</div>"
        month_count += 1

    return edit_data
