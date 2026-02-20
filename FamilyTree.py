# Class to generate a family tree and taking in user queries to access the data
# Author: Aidan Fernandez

from Person import Person
from PersonFactory import PersonFactory


class FamilyTree:
    def __init__(self):
        self.person_factory = PersonFactory()
        self.family_tree = []
        self.root_last_names = []
        self.start_year = 1950
        self.end_year = 2120
        self.stop = False

    def generate_family_tree(self):
        """
        Generate a family tree starting with two people born in start_year
        then stops when end_year is reached or no children created.
        """
        print("Generating family tree...")
        # BFS approach to generating tree
        create_root_people = self._create_root_people()
        queue = create_root_people
        while queue:
            current = queue.pop(0)
            self.family_tree.append(current)
            self._add_spouse(current)
            self._add_children(current)
            # Stop if we reach the end year
            if current.get_year_born() > self.end_year:
                break

    def _create_root_people(self):
        """
        Create the initial two people born in self.start_year.
        By spec they are a couple and their last names are preserved for direct descendants.
        """
        # use fixed example last names to know start name
        Adam = self.person_factory.create_person(self.start_year)
        Eve = self.person_factory.create_person(self.start_year)
        Adam.set_spouse(Eve)
        Eve.set_spouse(Adam)
        

        self.root_last_names = [Adam.last_name, Eve.last_name]
        self.family_tree.append(Adam)
        self.family_tree.append(Eve)
        return [Adam, Eve]

    def _add_children(self, parent: Person):
        """
        Add children to the given parent person.
        """
        self.person_factory.try_create_children(parent, self.root_last_names)
        if parent.had_children:
            for child in parent.children:
                self.family_tree.append(child)

    def _add_spouse(self, person: Person):
        """
        Add a spouse to the given person.
        """
        if person.get_spouse():
            return
        self.person_factory.try_create_spouse(person)
        if person.get_spouse():
            self.family_tree.append(person.get_spouse())

    

    def _handle_input(self):
        while True:
            user_input = input("(1) Total number of people in Family Tree\n" +
                               "(2) Total number of people in the tree by decade\n" +
                               "(3) Duplicate Names\n" +
                               "(4) Exit\n"
            )
            if user_input.lower() == "exit":
                break
            # Process the user input and query the family tree
            self._process_query(user_input)

    def _process_query(self, query: str):
        if query == "1":
            print(f"Total number of people in Family Tree: {len(self.family_tree)}")
        elif query == "2":
            for decade in range(1950, 2120, 10):
                count = sum(1 for p in self.family_tree if p.get_year_born() // 10 == decade // 10)
                print(f"Total number of people in the tree born in the {decade}s: {count}")
        elif query == "3":
            duplicates = self._find_duplicate_names()
            if duplicates:
                print("Duplicate names found:")
                for name, count in duplicates.items():
                    print(f" - {name}: {count}")
        elif query == "4":
            print("Exiting...")
            self.stop = True
        else:
            print("Invalid input. Please enter a valid option.")

    def _find_duplicate_names(self):
        name_counts = {}
        for person in self.family_tree:
            full_name = f"{person.first_name} {person.last_name}"
            if full_name in name_counts:
                name_counts[full_name] += 1
            else:
                name_counts[full_name] = 1
        duplicates = []
        for name, count in name_counts.items():
            if count > 1:
                duplicates.append((name, count))
        return duplicates

def main():
    family_tree = FamilyTree()
    family_tree.generate_family_tree()
    while not family_tree.stop:
        family_tree._handle_input()
    # You can add more functionality here, like querying the family tree

if __name__ == "__main__":
    main()