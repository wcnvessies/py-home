import math
from urllib.parse import quote_plus
import sqlalchemy
import os
from dotenv import load_dotenv

load_dotenv('/home/wcn/virtualenvs/.env')

def roundup(x, nearest_value):
    return int(math.ceil(x / nearest_value)) * nearest_value


def rounddown(x, nearest_value):
    return int(math.floor(x / nearest_value)) * nearest_value

def connect_database():
    user = os.getenv('USER_DB')
    password = os.getenv("PASSWORD_DB")
    host = os.getenv("HOST_DB")
    port = "3306"
    dbname = "home"

    connstr = f'mariadb+mariadbconnector://{user}:{quote_plus(password)}@{host}:{port}/{dbname}'

    engine = sqlalchemy.create_engine(connstr, echo=True)
    return engine, engine.connect()

def popup_html(df):
    project_name=df['name']
    company=df['company']
    project_number=str(df['project_number']).replace("nan","")
    year=df['year']
    location=f"{df['city']}, {df['country']}"
    vessels=str(df['vessels']).replace("nan","")
    description=df['description']

    left_col_color = "#19a7bd"
    right_col_color = "#f2f0d3"
    
    html = """<!DOCTYPE html>
    <html>
    <head>
    <h4 style="margin-bottom:10"; width="200px"><b>{}</b></h4>""".format(project_name) + """
    </head>
        <table style="height: 126px; width: 500px;">
    <tbody>
    <tr>
    <td style="width: 150px;background-color: """+ left_col_color +""";"><span style="color: #ffffff;">project number</span></td>
    <td style="width: 350px;background-color: """+ right_col_color +""";">{}</td>""".format(project_number) + """
    </tr>
    <tr>
    <td style="width: 150px;background-color: """+ left_col_color +""";"><span style="color: #ffffff;">company</span></td>
    <td style="width: 350px;background-color: """+ right_col_color +""";">{}</td>""".format(company) + """
    </tr>
    <tr>
    <td style="width: 150px;background-color: """+ left_col_color +""";"><span style="color: #ffffff;">year</span></td>
    <td style="width: 350px;background-color: """+ right_col_color +""";">{}</td>""".format(year) + """
    </tr>
    <tr>
    <td style="width: 150px;background-color: """+ left_col_color +""";"><span style="color: #ffffff;">location</span></td>
    <td style="width: 350px;background-color: """+ right_col_color +""";">{}</td>""".format(location) + """
    </tr>
    <tr>
    <td style="width: 150px;background-color: """+ left_col_color +""";"><span style="color: #ffffff;">equipment</span></td>
    <td style="width: 350px;background-color: """+ right_col_color +""";">{}</td>""".format(vessels) + """
    </tr>
    <tr>
    <td style="width: 150px;background-color: """+ left_col_color +""";"><span style="color: #ffffff;">description</span></td>
    <td style="width: 350px;background-color: """+ right_col_color +""";">{}</td>""".format(description) + """
    </tr>
    </tbody>
    </table>
    </html>
    """
    return html