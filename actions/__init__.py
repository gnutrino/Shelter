class Action(object):
    """
    Base class for actions
    """
    def __init__(self, game):
        self.game = game

    def parse_args(self, args):
        """
        Parse the arg string and set up the action as appropriate

        Arguments:
        args -- the argument string, unsplit
        """
        pass

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
        try:
            cmd, args = line.split(maxsplit=1)
        except ValueError:
            return self
        cmd = cmd.lower()

        for action in self.actions:
            if cmd == action.name or cmd in action.aliases:
                action = action(self.game)
                action.parse_args(args)
                stack.push(self)
                return action

        shell.print_line("Unrecognised command: {}".format(cmd))
        return self

class Quit(Action):
    """
    Quits the game
    """
    name = "quit"
    aliases = ["exit", "q"]

    def __call__(self, shell, stack):
        stack.pop()
        return None

ActionLoop.add_action(Quit)
