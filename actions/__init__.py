class Action(object):
    """
    Base class for actions
    """
    def __init__(self, game):
        self.game = game

    def parse_args(self, args):
        """
        Parse the arg string and set up and return the action to run

        Arguments:
        args -- the argument string, unsplit
        """
        return self

    def __str__(self):
        return self.name

    def completion_matches(self, text):
        """Used to return a list of completions given arguments in text"""
        return []

    @classmethod
    def names(cls):
        """returns a list of all possible names for this Action, starting with
        the action name and then any defined aliases"""
        return [cls.name] + cls.aliases

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
        game = self.game
        if game.action_points <= 0:
            return game.StartDay

        shell.print_line("{} action points remaining.".format(game.action_points))
        line = shell.readline("> ")
        if not line.strip():
            return self

        try:
            cmd, args = line.split(maxsplit=1)
        except ValueError:
            cmd = line.rstrip()
            args = ''
        cmd = cmd.lower()

        action = self.get_action(cmd)
        if action is None:
            shell.print_line("Unrecognised command: {}".format(cmd))
            return self

        action = action(self.game)
        action = action.parse_args(args)
        stack.push(self)
        return action

    def handle_eof(self, shell, stack):
        """Used to handle EOF Exception in mainloop, returns the quit action to
        correctly give confirmation dialogue"""
        stack.push(self)
        return self.get_action("quit")(self.game)

    def get_action(self, name):
        """get action by name, also checks aliases"""
        for action in self.actions:
            if name == action.name or name in action.aliases:
                return action

        return None

    def complete(self, text, state):
        """
        Command line completion
        """

        nargs = len(text.split())
        # Nothing typed yet
        if nargs == 0:
            matches = [action.name for action in self.actions]
        # started typing the command but haven't finished
        elif nargs == 1 and text[-1] != ' ':
            matches = []
            for action in self.actions:
                matches += [(name + ' ') for name in action.names() if name.startswith(text)]

        # otherwise find out what action we typed and defer to that to get a
        # choice list
        else:
            cmd, args = text.split(maxsplit=1)
            matches = self.get_action(cmd)
            if action is None:
                return None
            action = action(self.game)
            matches = action.completion_matches(args)

        matches.append(None)
        return matches[state]

#Add actions to loop
from .general import *
ActionLoop.add_action(Quit)
ActionLoop.add_action(Skip)
