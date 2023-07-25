import os
from internal_types import Option


def formatCommandName(file: str) -> str:
    commandName = os.path.basename(file).replace(".py", "")
    formatted = purple(f"[{commandName}]")
    return formatted


def confirm(prompt: str, default: bool) -> bool:
    hint = " (Y/n)" if default else " (y/N)"
    print(prompt + hint)
    resp = None
    while resp not in ["y", "n", ""]:
        resp = input("> ")

    if resp == "":
        return default

    return resp == "y"


def chooseFromList(options: list[Option]) -> str:
    choices = {}
    i = 1
    for option in options:
        choices[option["key"]] = option["value"]

        key = option["key"] if option["key"] else "<cr>"
        display = option["display"] if "display" in option else option["value"]
        output = bold(str(display)) if key == "<cr>" else str(display)

        print(key + ": " + output + ",")

        i += 1

    resp = "NONE"

    while resp not in choices:
        resp = input("> ")

    return choices[resp]


class color:
    PURPLE = "\033[95m"
    CYAN = "\033[96m"
    DARKCYAN = "\033[36m"
    BLUE = "\033[94m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"
    END = "\033[0m"


def bold(text: str):
    return color.BOLD + str(text) + color.END


def red(text: str):
    return color.RED + str(text) + color.END


def yellow(text: str):
    return color.YELLOW + str(text) + color.END


def green(text: str):
    return color.GREEN + str(text) + color.END


def purple(text: str):
    return color.PURPLE + str(text) + color.END


def blue(text: str) -> str:
    return color.BLUE + text + color.END


def promptHeader(commandName: str, index: int, count: int) -> str:
    return f"\n{formatCommandName(commandName)} - {str(index)}/{str(count)}"
