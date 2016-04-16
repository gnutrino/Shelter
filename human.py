"""Module containing all Human classes."""
from general_funcs import print_line, SLOW, FAST, NORMAL
from collections import OrderedDict

class Human(object):
    """Basic class for all humans in game."""

    def __init__(self, first_name, surname, gender, age=21, day_of_birth=0, 
                 father=None, mother=None):
        """Constructor for Human class.

        Arguments:
        first_name -- first name of Human
        surname    -- surname of Human, if None and father is given, inherits
                      from father
        gender -- gender of Human
        age -- age of Human
        day_of_birth -- day Human was born
        father -- Human's father
        mother -- Human's mother
        """
        self.alive = True

        self.first_name = first_name
        if surname is None and father is not None:
            surname = father.surname
        self.surname = surname

        self.gender = gender.upper()
        self.day_of_birth = day_of_birth
        self.age = age

        self.father = father
        self.mother = mother

        self.hunger = 0
        self.thirst = 0

        self.partner = None

        # The stats of the person. Affects the production of
        # room the person has been assigned to.
        # TODO: randomise starting stats for NPCs
        self.stats = OrderedDict((
                    ("strength",     1),
                    ("perception",   1),
                    ("endurance",    1),
                    ("charisma",     1),
                    ("intelligence", 1),
                    ("agility",      1),
                    ("luck",         1),
                ))

        self.work_room = None
        self.children = []

        self.level = 1  # Determines production efficiency
        self.XP = 0

    def __str__(self):
        """String representation of object, first name and last name.

        Returns:
        str -- "Firstname Lastname"
        """
        return "{} {}".format(self.first_name, self.surname)

    def details(self):
        """returns a list of lines to output showing details of this person"""
        result = [
                str(self),
                "Age: {0.age} | Gender: {0.gender} | Hunger: {0.hunger} | Thirst: {0.thirst} | Room: {0.work_room}".format(self),
                ]

        for stat, value in self.stats.items():
            result.append("    {} : {}".format(stat, value))

        return result

    def stat(self, stat):
        """
        Returns the value of stat for this character

        Arguments:
        stat -- name of the stat to fetch

        Returns:
        int -- value of the requested stat
        """
        return self.stats[stat]


    def update(self, shell, gamestate):
        """stub function to contain daily code for people"""
        shell.print_line("{}.update is not implemented.".format(type(self).__name__))
        
    def see_stats(self):
        """Check stats of inhabitant."""
        for stat in self.stats:
            print_line("{}: {}".format(stat, self.stats[stat]))
  
    def feed(self, amount):
        """Reduce hunger level of inhabitant.

        Arguments:
        amount -- how much to feed inhabitant
        """
        self.hunger -= amount
        if self.hunger < 0:
            self.hunger = 0

    def drink(self, amount):
        """Reduce thirst level of inhabitant.

        Arguments:
        amount -- how much to feed inhabitant
        """
        self.thirst -= amount
        if self.thirst < 0:
            self.thirst = 0
    
    def level_up(self, shell, stack):
        """Generic level up screen"""
        if not self.has_levelup():
            return None

        shell.print_line("{} has gained enough experience to level up!!!".format(self))
        shell.print_line(*self.details(), sep='\n')
        self.level += 1

        choices = [("{} (current: {})".format(stat, value), stat) for stat, value in self.stats.items()]
        choice = shell.choose_from("Choose an attribute to increase:", choices)
        self.stats[choice] += 1

        #continue levelling up if we have the xp for it
        return self.level_up
    
    def has_levelup(self):
        """Check experience of inhabitant is enough to level up.

        Returns:
        bool -- whether or not Human can level up"""
        # Xp needed to level up increases exponentially
        xp_needed = 10 + (3**self.level)
        return self.XP >= xp_needed
            
    def gain_xp(self, amount):
        """Increase experience of person. If they have enough to level 
        up, they do
        
        Arguments:
        amount -- amount to level up by
        """
        self.XP += amount
    
    def heal(self, amount):
        """Heal Human.

        Arguments:
        amount -- amount of health to give
        """
        self = people[0]
        if self.medic > 0:  # Medic Boost.
            amount = amount * (1 + (0.05 * self.medic))
        self.HP += amount
        if self.HP > 99:  # Truncates health
            self.HP = 100

    def mature(self, person):
        """Increment Human's age.

        Arguments:
        person -- Human who's aging
        """
        person.age += 1
        print_line("{} has matured and is now {} years old!" \
        .format(self, self.age))

    def take_damage(self, amount):
        """Take health from Human.

        Arguments:
        amount -- amount of health to take
        """
        self.defense = self.stats["strength"] * 10
        damage_taken = amount - self.defense
        if damage_taken < 1:
            damage_taken = 0
        else:
            self.HP -= damage_taken
            if self.HP < 1:
                self.die()
    
    def increase_hunger(self, amount):
        """Increase hunger level of Human by certain amount
        
        Arguments:
        amount -- amount of hunger to increase by
        """
        self.hunger += amount
    
    def increase_thirst(self, amount):
        """Increase thirst level of Human by certain amount
        
        Arguments:
        amount -- amount of thirst to increase by
        """
        self.thirst += amount
    
    def scavenge(self, days=10):
        """Send inhabitant on scavenging mission.

        Arguments:
        days -- ask user for number of days if this is 'days'.
        """
        self.current_activity = "scavenging"
        if not (isinstance(days, int)) or days <= 0:
            person.days_to_scavenge_for = 10
        else:
            person.days_to_scavenge_for = days

    def can_mate(self):
        """Check if Human meets requirements to have children.

        Returns:
            bool -- whether or not human can mate
        """
        if self.age < 18:
            return False
        if len(self.children) > 5:  # Upper limit of children is 5
            return False
        # Have to wait for a year before parent can have child again.
        for child in self.children:
            if people(child).age < 1:
                return False
        return True

    def die(self, game, cause):
        """Kill self, and unassign from a assigned room.
            #Should make this a method of the main game.
        Arguments:
        game -- main game object
        cause -- cause of death
        """
        print_line("{} has died of {}!".format(self, cause))
        if self.assigned_room:
            game.rooms[self.assigned_room].remove(str(self))
        if not isinstance(self, Player):
            pass
        else:
            self.alive = False


class NPC(Human):
    """NPC class, inherits Human attributes."""

    def __init__(self, first_name, surname, gender, age=21, day_of_birth=0, 
                 father=None, mother=None):
        """NPC class constructor.

        Arguments:
        first_name   -- first name of NPC
        surname      -- surname of NPC
        gender       -- gender of NPC
        age          -- age of NPC
        day_of_birth -- day NPC was born on
        father       -- father of NPC
        father       -- mother of NPC
        """
        super().__init__(first_name, surname, gender, age, day_of_birth,
                         father, mother)

        self.current_activity = ""
        self.days_active = 0
        self.activity_limit = 0
        self.scavenging = False
        self.days_scavenging = 0
        self.days_to_scavenge_for = 0

