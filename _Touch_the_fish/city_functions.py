def get_city_formatted(city, country, population=''):
    if population:
        full_city = city + " " + country + " Population=" + population
    else:
        full_city = city + " " + country

    return full_city.title()


