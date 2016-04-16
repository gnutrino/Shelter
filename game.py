"""
Main screens and classes for the game
"""
from player import Player
from room import Room
from shelter import Shelter, generate_dwellers
from engine import Sequence
from actions import ActionLoop

class Game(object):
    """
    Represents the state of a game. This is the class to serialize/deserialize
    to save/load
    """

    def __init__(self):
        """instantiates Game in the most basic state that won't throw errors if
        used, actual logic for startign a new game from a gameplay point of
        view goes in NewGame"""
        self.day = 0
        self.action_points = 0

        self.player = None
        self.shelter = Shelter()

    ### Screens:

    @classmethod
    def NewGame(cls, shell, stack):
        """
        Screen for setting up a new game
        """

        game = cls()

        game.day = 0
        game.action_points = 0

        #create player
        game.player = Player.create(shell)
        game.player.inventory.update({
                'steel' : 5,
                'turret': 1,
                'chip'  : 1,
            })
        game.player.caps = 100

        #create and populate shelter
        game.shelter = Shelter()
        game.shelter.people = generate_dwellers(5, game)

        #Add some starting rooms
        game.shelter.rooms = [
                Room('living'),
                Room('generator'),
                Room('water'),
                Room('kitchen'),
            ]

        return game.StartDay

    def StartDay(self, shell, stack):
        """
        Starts a new day
        """
        self.day += 1
        shell.print_line("A new day dawns. It is now day {} in the vault".format(self.day))

        #add 50 new action points, capped at 50 total, deals with overspend
        #from the previous day simply by allowing negative action points
        self.action_points = min(self.action_points + 50, 50)

        for room in self.shelter.rooms:
            room.update(shell, self)

        for person in self.shelter.people[:]:
            person.update(shell, self)

        #TODO: Trader logic

        return Sequence(self.LevelUps, ActionLoop(self))

    def LevelUps(self, shell, stack):
        """
        apply any pending level ups
        """
        return Sequence(*(person.level_up for person in self.shelter.people))

    ### End of Screens
