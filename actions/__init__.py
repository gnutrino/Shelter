from game import GameScreen

class Action(GameScreen):
    """
    Base class for actions
    """
    #TODO: Implement
    pass

class ActionLoop(GameScreen):
    """
    Main action loop
    """

    def __call__(self, shell, stack):
        raise NotImplementedError()
