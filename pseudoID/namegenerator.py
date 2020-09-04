# https://de.wiktionary.org/wiki/Verzeichnis:Deutsch/Namen
# https://www.datendieter.de/item/Liste_von_deutschen_Staedtenamen_.csv
import random
from datetime import datetime, timedelta


def generate_n_personal_info(n_items=10000):
    # Names
    with open('../../data_test/names_female', 'r') as female, \
            open('../../data_test/names_male', 'r') as male, \
            open('../../data_test/names_family', 'r') as name:
        names_female = female.read().split("   ")[1::2]
        names_male = male.read().split("   ")[1::2]
        names_family = name.read().split("   ")[1::2]

    # Date of Birth
    age_mean = datetime(1990, 1, 1)
    age_std_days = 10 * 365

    rand_date = age_mean + timedelta(days=random.gauss(0, age_std_days))

    # Place of Birth
    with open('../../data_test/staedte_osm.txt', 'r', encoding="utf8") as file:
        cities = file.read().split("\"")[1::2]

    data = []
    for i in range(n_items):
        dob_random = age_mean + timedelta(days=random.gauss(0, age_std_days))

        data.append([random.choice(names_male + names_female).strip(),
                           random.choice(names_family).strip(),
                           random.choice(cities).strip(),
                           dob_random.strftime("%d-%m-%Y"),
                           random.choice(names_family).strip()])

    return data
