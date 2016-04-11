import random
from human import NPC

class Shelter(object):
    """class to hold shelter state"""

    def __init__(self):
        self.defense = 0
        self.rooms = []
        self.people = []

# list of possible names
name_list = [
        "Thompson",
        "Elenor",
        "Codsworth",
        "Sharmak",
        "Luthor",
        "Marshall",
        "Cole",
        "Diven",
        "Davenport",
        "John",
        "Max",
        "Lex",
        "Leth",
        "Exavor"
        ]

def generate_dwellers(num, gamestate=None, name_list=name_list):
    """
    Generates and returns 'num' random shelter dwellers

    Arguments:
    num -- Number of NPCs to generate
    gamestate -- (optional) current game state to use for getting the day and
                 checking whether generated dwellers already exist
    name_list -- list of names to use generate npcs. Default is game.name_list

    Returns:
    people -- List of generated NPCs
    """

    people = []

    if gamestate is not None:
        day = gamestate.day
        shelter = gamestate.shelter
    else:
        day = 0
        shelter = None

    while len(people) < num:
        first_name = random.choice(name_list)
        surname = random.choice(name_list)
        if first_name == surname:
            continue
        name = "{} {}".format(first_name, surname)
        #detects if someone of this name already exists
        if shelter is not None and name in map(str, shelter.people):
            continue

        people.append(NPC(
            first_name,
            surname,
            random.choice(['M', 'F']),
        ))

    return people
