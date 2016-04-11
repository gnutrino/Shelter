"""
Player class and utility functions
"""

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
        Human.__init__(
            self, first_name, day_of_birth,
            parent_1, parent_2, age, gender)
        player_stats = ["medic", "crafting", "tactician", "cooking",
                        "barter", "inspiration", "scrapper",
                        "electrician"]
        for stat in player_stats: #Adds player specific stats to stat 
            # dict
            self.stats[str(stat)] = 0
        """
        self.medic = 0  # Improves healing capabilities of stimpacks
        self.crafting = 0  # Chance to not use components when crafting.
        self.tactician = 0  # Boosts defense.
        self.cooking = 0  # Boosts production level of kitchen.
        self.barter = 0  # Increases selling prices, decreases buying prices.
        self.inspiration = 0  # Boosts production and defense.
        self.scrapper = 0  # Boosts chance of bonus components when scrapping.
        self.electrician = 0  # Boosts power production
        """
        
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
        """ #Old choice_dict dictionary
        choice_dict = {
        'strength':self.stats["strength"], 'perception':self.stats["perception"],
        'endurance':self.stats["endurance"], 'charisma':self.stats["charisma"],
        'intelligence':self.stats["intelligence"], 'luck':self.stats["luck"],
        'medic':self.stats["medic"], 'crafting':self.stats["crafting"],
        'tactician':self.stats["tactician"], 'cooking':self.stats["cooking"],
        'inspiration':self.stats["inspiration"], 'scrapper':self.stats["scrapper"],
        'barter':self.stats["barter"], 'electrician':self.stats["electician"]
        }
        """
        if choice in choice_dict.keys():
            choice_dict[choice] += 1
        else:
            print_line("Invalid choice")
            self.level -= 1
            self.level_up()

def character_creation(shell):
    first_name = shell.get_word("What is your first name?")

    surname    = shell.get_word("What is your surname?")
    father = Human(surname=surname)

    maiden_name = shell.get_word("What is your mother's maiden name?")
    mother = Human(surname=maiden_name)

    gender = shell.choose_from("What is your gender?", [('Female', 'F'), ('Male', 'M')])

    return Player(first_name, 0, father, mother, 21, sex)
