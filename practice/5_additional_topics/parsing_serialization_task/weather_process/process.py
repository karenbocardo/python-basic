import os
import json
from statistics import mean
from datetime import datetime

global cities
global summary
cities = dict()
summary = dict()

def process_city(city, data):
    temp = list()
    wind_speed = list()
    for hour in data["hourly"]:
        temp.append(hour["temp"])
        wind_speed.append(hour["wind_speed"])
    
    stats = dict()

    # temperature statistics for the city
    stats['min_temp'] = min(temp)
    stats['max_temp'] = max(temp)
    stats['mean_temp'] = mean(temp)

    # wind speed statistics for the city
    stats['min_wind_speed'] = min(temp)
    stats['max_wind_speed'] = max(temp)
    stats['mean_wind_speed'] = mean(temp)

    cities[city] = stats

def process_country():
    summary['mean_temp'] = mean([city['mean_temp'] for city in cities.values()])
    summary['mean_wind_speed'] = mean([city['mean_wind_speed'] for city in cities.values()])
    summary['coldest_place'] = min(cities, key=lambda index: cities[index]['mean_temp'])
    summary['warmest_place'] = max(cities, key=lambda index: cities[index]['mean_temp'])
    summary['windiest_place'] = max(city['mean_wind_speed'] for city in cities.values())

def save_result():
    from xml.dom import minidom

    def write_attribs(dicc, elem):
        for stat, value in dicc.items():
            if type(value) is not str:
                value = f'{value:.2f}'
            elem.setAttribute(stat, value)

    root = minidom.Document()
    
    # weather
    weather = root.createElement('weather') 
    weather.setAttribute('country', 'Spain')
    weather.setAttribute('date', str(datetime.today().date()))
    root.appendChild(weather)
    
    # summary
    summary_elem = root.createElement('summary')
    write_attribs(summary, summary_elem)
    weather.appendChild(summary_elem)

    # cities
    cities_elem = root.createElement('cities')
    for city, stats in cities.items():
        city_elem = root.createElement(city)
        write_attribs(stats, city_elem)
        cities_elem.appendChild(city_elem)
    weather.appendChild(cities_elem)

    # save
    xml_str = root.toprettyxml(indent ="\t") 
    
    save_path_file = "result.xml"
    
    with open(save_path_file, "w") as f:
        f.write(xml_str) 

def process(source_data="source_data"):
    # read source data
    src_data = f"{os.getcwd()}/{source_data}"
    for city_name in os.listdir(src_data):
        city_folder = os.path.join(src_data, city_name)
        for file in os.listdir(city_folder):
            # read city json
            with open(os.path.join(city_folder, file)) as f:
                data = json.load(f)
                process_city(city_name, data)
    process_country()
    save_result()
