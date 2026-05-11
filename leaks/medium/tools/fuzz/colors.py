from colorama import Fore, Style


# define color functions
def c(s, t):
    return f"{t}{s}{Style.RESET_ALL}"


def red(s):
    return c(s, Fore.RED)


def green(s):
    return c(s, Fore.GREEN)


def yellow(s):
    return c(s,Fore.YELLOW)