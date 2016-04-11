"""
Player class and utility functions
"""
from human import Human
from item import Inventory

class Player(Human):
    """Player class, inherits Human attributes."""

    def __init__(
            self, first_name=None, day_of_birth=0,
            parent_1=None, parent_2=None, age=21, gender='M'):
        """Player class constructor.

        Arguments:
        first_name -- first name of Player
        day_of_birth -- day Player was born
        parent_1 -- name of Player's father
        parent_2 -- name of Player's mother
        age -- age of player
        gender -- gender of player
        """
        print("in Player.__init__, gender = {}".format(gender))
        super().__init__(
            first_name, day_of_birth,
            parent_1, parent_2, age, gender)
        player_stats = ["medic", "crafting", "tactician", "cooking",
                        "barter", "inspiration", "scrapper",
                        "electrician"]
        for stat in player_stats: #Adds player specific stats to stat 
            # dict
            self.stats[str(stat)] = 0

        self.inventory = Inventory()

    @classmethod
    def create(cls, shell):
        """
        creates and returns a player from user input
        """
        shell.print_line()

        first_name = shell.get_name("What is your first name?")
        surname    = shell.get_name("What is your surname?")
        father = Human(surname=surname)

        maiden_name = shell.get_name("What is your mother's maiden name?")
        mother = Human(surname=maiden_name)

        gender = shell.choose_from("What is your gender?", [('Female', 'F'), ('Male', 'M')])

        return cls(first_name, 0, father, mother, 21, gender)
        
    def level_up(self):
        super().level_up()
        print_line("\n")
        print_line("You can level up any of these attributes: ")
        for stat in choice_dict.keys():
            print_line(" {}".format(stat), end = " ")
        choice = input("Please choose an attribute to level up: ")
        choice.lower()
        perks = ["medic", "crafting", "tactitian", "cooking",
                 "inspiration", "scrapper", "barter", "electrician"]
        #Perks specific to the player are added to the dictionary of
        #available choices
        for perk in perks:
            choice_dict[perk] = self.stats[perk]
        if choice in choice_dict.keys():
            choice_dict[choice] += 1
        else:
            print_line("Invalid choice")
            self.level -= 1
            self.level_up()
