# Class for representing a person in Family Tree
# Author: Aidan Fernandez

class Person:
    def __init__(self, year_born, first_name, last_name, is_descendant):
        self.year_born = year_born
        # first name based on year born 
        self.first_name = first_name

        # last name
        self.last_name = last_name

        # flag: is person related to first two
        self.is_descendant = is_descendant

        # if they get married then create a new person +- 10 years of spouse
        self.spouse = None
        
        # based on birth rate per year
        # children born between 25-45 years after parent birth
        self.children = []
        
        self.year_died = None

        self.had_children = False
        

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.year_born})"

    def set_year_born(self, year_born):
        self.year_born = year_born

    def set_spouse(self, spouse):
        self.spouse = spouse

    def add_child(self, child):
        self.children.append(child)

    def set_year_died(self, year_died):
        self.year_died = year_died

    def get_year_born(self):
        return self.year_born

    def get_spouse(self):
        return self.spouse

    def get_children(self):
        return self.children

    def get_year_died(self):
        return self.year_died

    def had_children(self):
        self.had_children = True

    def is_descendant(self, bool: bool):
        self.is_descendant = bool