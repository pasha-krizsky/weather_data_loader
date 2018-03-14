import requests
import os


def update_headers(session_to_update):
    session_to_update.headers.update({
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0) Gecko/20100101 Firefox/45.0'
    })


def load_weather_page(city_id, year, month):
    url = "https://www.gismeteo.ru/diary/{0}/{1}/{2}/".format(int(city_id), int(year), int(month))
    return session.get(url).text


def load_weather_pages_to_files(year_from, month_from, year_to, month_to, city_id, city_name):
    prefix = "./weather_story/"
    subdir = "/raw"
    current_year = year_from
    current_month = month_from

    while current_year - year_to != -1 and current_month - month_to != -1:
        data = load_weather_page(city_id, current_year, current_month)

        final_path = prefix + city_name + subdir
        if not os.path.exists(final_path):
            os.makedirs(final_path)

        with open(final_path + "/{0}_{1}.html".format(int(current_year), int(current_month)),
                  'wb') as output_file:
            output_file.write(data.encode('utf8'))
        current_month -= 1

        if current_month == 0:
            current_month = 12
            current_year -= 1


session = requests.Session()
update_headers(session)

# fill in these params!
city_id_param = 14771
# folder name actually
city_name_param = "kronshtadt"

year_from_param = 2018
month_from_param = 3
year_to_param = 2015
month_to_param = 1

load_weather_pages_to_files(
    year_from_param,
    month_from_param,
    year_to_param,
    month_to_param,
    city_id_param,
    city_name_param)


