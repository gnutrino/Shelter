#!/usr/bin/env python3
"""
Main engine functions
"""
from gameshell import GameShell

class ScreenStack(object):
    """
    Class to hold a stack of screens
    """
    def __init__(self):
        self._stack = []
        self.current_screen = None

    def push(self, screen=None):
        """
        Pushes screen onto the screen stack

        Arguments:
        screen -- screen to push or None. If none it will push the current
                  screen onto the stack
        """
        if screen is None:
            screen = self.current_screen
        self._stack.append(screen)

    def pop(self):
        """
        Pop a screen from the stack and return it. Throws IndexError
        if the stack is empty

        Returns:
        screen -- the screen from the top of the stack.
        """
        return self._stack.pop()

class Sequence(object):
    """
    Convenience class to represent a sequence of screens where each screen
    follows sub-screen semantics to move on to the next (i.e returns None).
    Designed to make sequential screen sequences clearer rather than having to
    chase return values manually.
    """

    def __init__(self, *screens):
        """
        Initialises the sequence with screens to run

        Arguemnts:
        *screens -- screens to run as part of the sequnce given in the order
                    they should be run
        """
        self.screens = screens

    def __call__(self, shell, stack):
        for screen in reversed(self.screens):
            stack.push(screen)
        return None

def mainloop(screen, shell=None):
    """
    Runs the mainloop starting from screen. Implements a basic Finite State Machine with
    a stack for handling different game screens.

    Arguments:
    screen -- screen to start from, screens should be callables that take the
              game shell and screen stack as arguments and return the next
              screen to be displayed or None. Returning None will run the
              screen at the top of the screen stack or exit if the screen stack
              is empty
    shell -- GameShell instance to use for IO, if not provide a new instance of
             GameShell will be created
    """

    if shell is None:
        shell = GameShell()
    screen_stack = ScreenStack()

    while True:
        if screen is None:
            try:
                screen = screen_stack.pop()
            except IndexError:
                break

        screen_stack.current_screen = screen

        if hasattr(screen, 'complete'):
            shell.set_completer(screen.complete())

        try:
            screen = screen(shell, screen_stack)
        except EOFError:
            #if we recieve EOF we take this as a sign we want to move back a
            #screen
            shell.print_line()
            screen = None

if __name__ == "__main__":
    from game import Game
    mainloop(Game.NewGame)