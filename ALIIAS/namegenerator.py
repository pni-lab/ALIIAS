# https://de.wiktionary.org/wiki/Verzeichnis:Deutsch/Namen
# https://www.datendieter.de/item/Liste_von_deutschen_Staedtenamen_.csv
import random
from datetime import datetime, timedelta


def generate_n_personal_info(n_items=10000, weight_city=True):
    # Names
    with open('../data_test/names_female', 'r') as female, \
            open('../data_test/names_male', 'r') as male, \
            open('../data_test/names_family', 'r') as name:
        names_female = female.read().split("   ")[1::2]
        names_male = male.read().split("   ")[1::2]
        names_family = name.read().split("   ")[1::2]

    # Date of Birth
    age_mean = datetime(1990, 1, 1)
    age_std_days = 10 * 365

    rand_date = age_mean + timedelta(days=random.gauss(0, age_std_days))

    # Place of Birth
    #with open('../data_test/staedte_osm.txt', 'r', encoding="utf8") as file:
    #    cities = file.read().split("\"")[1::2]

    with open('../data_test/list_big_cities.txt', 'r', encoding="utf8") as file:
        big_cities = file.read().split("\n")

    if weight_city:
        for i in range(20):
            big_cities.append(big_cities[0])
    data = []
    data_joined = []

    for i in range(n_items):
        dob_random = age_mean + timedelta(days=random.gauss(0, age_std_days))
        family_name = random.choice(names_family).strip()

        maiden_name = random.choice(names_family).strip()

        new_entry = [random.choice(names_male + names_female).strip(),
                           family_name,
                           random.choice(big_cities).strip(),
                           dob_random.strftime("%d-%m-%Y"),
                           maiden_name]
        data.append(new_entry)
        data_joined.append('_'.join(new_entry))
    return data, data_joined
