import base64
import math
import os
from datetime import datetime
from urllib.parse import quote_plus

import sqlalchemy
from dotenv import load_dotenv

load_dotenv("/home/wcn/virtualenvs/.env")


def roundup(x, nearest_value):
    return int(math.ceil(x / nearest_value)) * nearest_value


def rounddown(x, nearest_value):
    return int(math.floor(x / nearest_value)) * nearest_value


def date_diff_in_seconds(dt2, dt1):
    timedelta = dt2 - dt1
    return timedelta.days * 24 * 3600 + timedelta.seconds


def dhms_from_seconds(seconds):
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    return (days, hours, minutes, seconds)


def connect_database(dbname: str = "home"):
    user = os.getenv("USER_DB")
    password = os.getenv("PASSWORD_DB")
    host = os.getenv("HOST_DB")
    port = "3306"

    connstr = f"mariadb+mariadbconnector://{user}:{quote_plus(password)}@{host}:{port}/{dbname}"

    engine = sqlalchemy.create_engine(connstr, echo=False)
    return engine, engine.connect()


def connect_database_psql():
    user = os.getenv("USER_DB_PSQL")
    password = os.getenv("PASSWORD_DB")
    host = os.getenv("HOST_DB_PSQL")
    port = 5432
    dbname = "home"

    connstr = f"postgresql://{user}:{quote_plus(password)}@{host}:{port}/{dbname}"

    engine = sqlalchemy.create_engine(connstr, echo=False)
    return engine, engine.connect()


def popup_html(df):
    project_name = df["name"]
    company = df["company"]
    project_number = str(df["project_number"]).replace("nan", "")
    year = df["years"]
    location = f"{df['city']}, {df['country']}"
    vessels = str(df["vessels"]).replace("nan", "")
    description = df["description"]
    logo = df["company_logo"]
    tools = df["tools_all"]
    days = "" if df["days_total"] == 0 else int(df["days_total"])
    type_support = df["type"]

    encoded = base64.b64encode(open(os.path.join(os.getcwd(), "img", logo), "rb").read())

    left_col_color = "#19a7bd"
    right_col_color = "#f2f0d3"

    #     <td style="width: 150px;background-color: """
    #     + left_col_color
    #     + """;"><span style="color: #ffffff;">project number</span></td>
    # <td style="width: 350px;background-color: """
    #     + right_col_color
    #     + """;">{}</td>""".format(project_number)
    #     + """
    # </tr>
    # <tr>

    html = (
        """<!DOCTYPE html>
    <html>
    <head>
    <img src="data:image/png;base64,{}" style="width:250px;">
    <h4 style="margin-bottom:10"; width="200px"><b>{}</b></h4>""".format(
            encoded.decode("UTF-8"), project_name
        )
        + """
    </head>
        <table style="height: 126px; width: 500px;">
    <tbody>
    <tr>
    <td style="width: 150px;background-color: """
        + left_col_color
        + """;"><span style="color: #ffffff;">company</span></td>
    <td style="width: 350px;background-color: """
        + right_col_color
        + """;">{}</td>""".format(company)
        + """
    </tr>
    <tr>
    <td style="width: 150px;background-color: """
        + left_col_color
        + """;"><span style="color: #ffffff;">year</span></td>
    <td style="width: 350px;background-color: """
        + right_col_color
        + """;">{}</td>""".format(year)
        + """
    </tr>
        <tr>
    <td style="width: 150px;background-color: """
        + left_col_color
        + """;"><span style="color: #ffffff;">days</span></td>
    <td style="width: 350px;background-color: """
        + right_col_color
        + """;">{}</td>""".format(days)
        + """
    </tr>
    <tr>
    <td style="width: 150px;background-color: """
        + left_col_color
        + """;"><span style="color: #ffffff;">location</span></td>
    <td style="width: 350px;background-color: """
        + right_col_color
        + """;">{}</td>""".format(location)
        + """
    </tr>
        <tr>
    <td style="width: 150px;background-color: """
        + left_col_color
        + """;"><span style="color: #ffffff;">type</span></td>
    <td style="width: 350px;background-color: """
        + right_col_color
        + """;">{}</td>""".format(type_support)
        + """
    </tr>
        <tr>
    <td style="width: 150px;background-color: """
        + left_col_color
        + """;"><span style="color: #ffffff;">tools</span></td>
    <td style="width: 350px;background-color: """
        + right_col_color
        + """;">{}</td>""".format(tools)
        + """
    </tr>
    <tr>
    <td style="width: 150px;background-color: """
        + left_col_color
        + """;"><span style="color: #ffffff;">equipment</span></td>
    <td style="width: 350px;background-color: """
        + right_col_color
        + """;">{}</td>""".format(vessels)
        + """
    </tr>
    <tr>
    <td style="width: 150px;background-color: """
        + left_col_color
        + """;"><span style="color: #ffffff;">description</span></td>
    <td style="width: 350px;background-color: """
        + right_col_color
        + """;">{}</td>""".format(description)
        + """
    </tr>
    </tbody>
    </table>
    </html>
    """
    )
    return html
