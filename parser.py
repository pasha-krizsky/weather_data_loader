from bs4 import BeautifulSoup
import os


def parse_table(rows):
    res = []
    i = 0
    for tr in rows:
        position = tr.findAll('td')[0].text
        temp = tr.findAll('td')[1].text
        pressure = tr.findAll('td')[2].text

        cloud_element = tr.findAll('td')[3]

        cloud = ''
        if len(cloud_element.findAll('img')) > 0:
            cloud = cloud_element.findAll('img')[0]['src']

        if 'dull' in cloud:
            cloud = 1
        elif 'suncl' in cloud:
            cloud = 0.5
        elif 'sunc' in cloud:
            cloud = 0.25
        elif 'sun' in cloud:
            cloud = 0
        else:
            cloud = 'NAN'

        wind_element = tr.findAll('td')[5]
        wind_value = 'NAN'
        if len(wind_element.findAll('span')) > 0:
            wind_value = wind_element.findAll('span')[0].text

        res.append([])
        res[i].append(position)
        res[i].append(temp)
        res[i].append(pressure)
        res[i].append(cloud)
        res[i].append(wind_value)
        i = i + 1

    return res


def parse(year_from, month_from, year_to, month_to, city_name):

    prefix = "./weather_story/"
    subdir = "/res"

    current_year = year_from
    current_month = month_from

    while current_year - year_to != -1 and current_year - month_to != -1:

        with open(prefix + city_name + '/raw/{0}_{1}.html'.format(current_year, current_month), 'r',
                  encoding='utf-8') as file:
            data = file.read().replace('\n', '')

        final_path = prefix + city_name + subdir
        if not os.path.exists(final_path):
            os.makedirs(final_path)

        file_to_write = open(final_path + '/{0}_{1}.txt'.format(current_year, current_month), 'w',
                             encoding='utf-8')

        soup = BeautifulSoup(data, "lxml")
        table = soup.find('table', {'align': "center"})
        rows = table.findAll('tr', {'align': "center"})
        result = parse_table(rows)
        for row in result:
            for element in row:
                file_to_write.write(str(element))
                file_to_write.write(" ")
            file_to_write.write("\n")

        current_month -= 1

        if current_month == 0:
            current_month = 12
            current_year -= 1


# fill in these params!
city_name_param = "kronshtadt"
year_from_param = 2018
month_from_param = 3
year_to_param = 2015
month_to_param = 1

parse(
    year_from_param,
    month_from_param,
    year_to_param,
    month_to_param,
    city_name_param)
