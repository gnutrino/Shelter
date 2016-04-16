from . import Action

class Quit(Action):
    """
    Quits the game
    """
    name = "quit"
    aliases = ["exit"]

    def __call__(self, shell, stack):
        if shell.confirmation_dialogue("Are you sure you want to quit?"):
            stack.pop()
        return None

class Skip(Action):
    """
    End the current day and skip to the next
    """
    name = "skip"
    aliases = ["end", "next"]

    def __call__(self, shell, stack):
        stack.pop()
        return self.game.StartDay
