# Class for reading csv files to create Person objects for Family tree
# Author: Aidan Fernandez

# csv & random learned from geeksforgeeks
import csv
import math
import random
from Person import Person


class PersonFactory:

    def __init__(self):
        self._read_files()

    def _read_files(self):
        print("Reading files...")
        # Initialize all dictionaries
        self.rankings_dict = {}
        self.birth_rates_dict = {}
        self.life_expectancy_dict = {}
        self.first_names_dict = {}
        self.last_names_dict = {}
        self.birth_rates_dict = {}
        self.marriage_rates_dict = {}

        # Fill dictionaries
        self._set_rank_probability()
        self._set_birth_rates()
        self._set_life_expectancy()
        self._set_first_names()
        self._set_last_names()
        self._set_marriage_rates()

    # Helper functions to input data

    def _set_rank_probability(self):
        """Set the rank probability for each rank in a rankings_dict."""
        ranking_file = "rank_to_probability.csv"

        with open(ranking_file, "r") as f:
            rankings = f.readline().strip().split(",")

            for i in range(len(rankings)):
                self.rankings_dict[i] = rankings[i]

    def _set_birth_rates(self):
        """Set the birth rates for each year in a birth_rates_dict."""
        birth_rate_file = "birth_and_marriage_rates.csv"

        with open(birth_rate_file, "r") as f:
            reader = csv.DictReader(f)

            for row in reader:
                decade = row.get("decade")
                rate = float(row.get("birth_rate", 0))
                self.birth_rates_dict[decade] = rate

    def _set_life_expectancy(self):
        """Set the life expectancy for each year in a life_expectancy_dict."""
        life_expectancy_file = "life_expectancy.csv"

        with open(life_expectancy_file, "r") as f:
            reader = csv.DictReader(f)

            for row in reader:
                year = int(row.get("Year"))
                expectancy = float(row.get("life_expectancy", 0))
                self.life_expectancy_dict[year] = expectancy

    def _set_first_names(self):
        """Set the dict of first names and their probabilities"""
        first_name_file = "first_names.csv"

        with open(first_name_file, "r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                decade = row.get("decade")
                name = row.get("name")
                frequency = float(row.get("frequency", 0))

                # add values into two lists sorted by decade
                bucket = self.first_names_dict.setdefault(
                    decade, {"names": [], "frequencies": []}
                )
                bucket["names"].append(name)
                bucket["frequencies"].append(frequency)

    def _set_last_names(self):
        last_name_file = "last_names.csv"

        with open(last_name_file, "r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                decade = row.get("Decade")
                name = row.get("LastName")
                frequency = float(row.get("Rank", 0))

                # add values into two lists sorted by decade
                bucket = self.last_names_dict.setdefault(
                    decade, {"LastNames": [], "Ranks": []}
                )
                bucket["LastNames"].append(name)
                bucket["Ranks"].append(frequency)

    def _set_birth_rate(self):
        """Set the birth rate for each year in a birth_rates_dict."""
        birth_rate_file = "birth_and_marriage_rates.csv"

        with open(birth_rate_file, "r") as f:
            reader = csv.DictReader(f)

            for row in reader:
                year = int(row.get("year"))
                rate = float(row.get("birth_rate", 0))
                self.birth_rates_dict[year] = rate

    def _set_marriage_rates(self):
        """Set the marriage rates for each year in a marriage_rates_dict."""
        marriage_rate_file = "birth_and_marriage_rates.csv"

        with open(marriage_rate_file, "r") as f:
            reader = csv.DictReader(f)

            for row in reader:
                decade = row.get("decade")
                rate = float(row.get("marriage_rate", 0))
                self.marriage_rates_dict[decade] = rate

    # Helper functions for rules for generating names and other attributes

    def _decade(self, year_born):
        decade = (year_born // 10) * 10
        return f"{decade}s", decade

    def _get_name(self, year_born):
        decade_key = self._decade(year_born)[0]
        bucket = self.first_names_dict.get(decade_key)
        if bucket and bucket.get("names"):
            return random.choices(bucket["names"], weights=bucket["frequencies"])[0]
        return None

    def _get_last_name(self, year_born):
        # convert year like 1953 -> "1950s"
        decade_key = self._decade(year_born)[0]
        bucket = self.last_names_dict.get(decade_key)
        weights = []
        for rank in bucket.get("Ranks", []):
            weight = 0.0
            weight = float(self.rankings_dict.get(rank, 0))
            weights.append(weight)
        if bucket and bucket.get("LastNames"):
            return random.choices(bucket["LastNames"], weights=weights)[0]

    def _get_birth_rate(self, year):
        decade_key = self._decade(year)[0]
        if decade_key in self.birth_rates_dict:
            return self.birth_rates_dict.get(decade_key)

    def _how_many_children(self, year):
        birth_rate = self._get_birth_rate(year)
        if birth_rate:
            # Simulate the number of children based on the birth rate
            low = max(0, int(math.floor(birth_rate - 1.5)))
            high = max(low, int(math.ceil(birth_rate + 1.5)))
            return random.randint(low, high)
        return 0

    def _get_marriage_rate(self, year):
        decade_key = self._decade(year)[0]
        if decade_key in self.marriage_rates_dict:
            return self.marriage_rates_dict.get(decade_key)

    def _married(self, year) -> Person:
        marriage_rate = self._get_marriage_rate(year)
        if random.random() < marriage_rate:
            # return wife/husband/spouse
            return
        return False

    def _get_year_died(self, year_born):
        lifetime = self._get_life_expectancy(year_born)
        if lifetime is None:
            return None
        try:
            lifetime = float(lifetime)
        except (ValueError, TypeError):
            return None
        min_age = max(0, int(lifetime - 10))
        max_age = max(min_age, int(lifetime + 10))
        death_age = random.randint(min_age, max_age)
        return death_age + year_born

    def _get_life_expectancy(self, year_born):
        decade_born = self._decade(year_born)[1]
        return self.life_expectancy_dict.get(decade_born)

    # public functions
    def create_person(self, year_born, last_name=None, is_descendant=False):
        name = self._get_name(year_born)
        if last_name is None:
            last_name = self._get_last_name(year_born)
        # if they are root descendant they
        person = Person(year_born, name, last_name, is_descendant)
        person.set_year_died(self._get_year_died(year_born))
        return person

    def try_create_spouse(self, person: Person):
        spouse = self.get_spouse(person)
        if not spouse:
            # Create a new spouse if not found
            spouse_year_born = person.get_year_born() + random.randint(-10, 10)
            spouse = self.create_person(spouse_year_born)
            person.set_spouse(spouse)
            spouse.set_spouse(person)

    def try_create_children(self, parent: Person, root_last_names: []):
        if parent.had_children:
            return
        spouse = parent.get_spouse()
        if spouse:
            # older parent is the parent for calculating children age
            if parent.get_year_born() < spouse.get_year_born():
                parent, spouse = spouse, parent

        num_children = self._how_many_children(parent.get_year_born())
        for _ in range(num_children):
            child_year_born = parent.get_year_born() + random.randint(25, 45)
            child = self.create_person(child_year_born, parent.last_name)
            parent.children.append(child)
            if spouse:
                spouse.children.append(child)
            if (
                child.last_name == root_last_names[0]
                or child.last_name == root_last_names[1]
            ):
                child.is_descendant = True
        parent.had_children = True
        spouse.had_children = True if spouse else False
