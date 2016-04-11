"""
Main screens and classes for the game
"""
from player import Player
from human import generate_dwellers
from room import Room
from shelter import Shelter

class GameScreen(object):
    """
    Base class for screens that hold gamestate
    """

    def __init__(self, gamestate):
        self.gs = gamestate

    def __call__(self, shell, stack):
        raise NotImplementedError()

from actions import ActionLoop

class GameState(object):
    """
    Represents the state of a game. This is the class to serialize/deserialize
    to save/load
    """
    pass

class StartDay(GameScreen):
    """
    Starts a new day
    """

    def __call__(self, shell, stack):
        gs = self.gs
        gs.day += 1

        #add 50 new action points, capped at 50 total, deals with overspend
        #from the previous day simply by allowing negative action points
        gs.action_points = min(gs.action_points + 50, 50)

        for room in gs.shelter.rooms:
            room.update(shell, gs)

        for person in gs.shelter.people:
            person.update(shell, gs)

        #TODO: Trader logic

        return ActionLoop(gs)

def new_game(shell, stack):
    """
    Screen for setting up a new game
    """

    gamestate = GameState()

    gamestate.day = 0
    gamestate.action_points = 0

    #create player
    gamestate.player = Player.create(shell)
    gamestate.player.inventory.update({
            'steel' : 5,
            'turret': 1,
            'chip'  : 1,
        })
    gamestate.player.caps = 100

    #create and populate shelter
    gamestate.shelter = Shelter()
    gamestate.shelter.people = generate_dwellers(5)

    #Add some starting rooms
    gamestate.shelter.rooms = [
            Room('living'),
            Room('generator'),
            Room('water'),
            Room('kitchen'),
        ]

    return StartDay(gamestate)
