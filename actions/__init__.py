class Action(object):
    """
    Base class for actions
    """
    def __init__(self, game):
        self.game = game

class ActionLoop(object):
    """
    Main action loop
    """

    actions = []

    def __init__(self, game):
        self.game = game

    @classmethod
    def add_action(cls, action):
        """Adds an action to the list of possible actions"""
        cls.actions.append(action)

    def __call__(self, shell, stack):
        line = shell.readline(">")
        cmd, *args = line.split()

        for action in self.actions:
            if cmd == action.name or cmd in action.aliases:
                return action(self.game)

        shell.print_line("Unrecognised command: {}".format(cmd))
        return self
