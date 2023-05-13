import sys

sys.path.append("../..")

import typer
from simple_term_menu import TerminalMenu
from rich.console import Console

from user import UserGenerator, UserUpdater, UserSummary
from bot import BotUpdater

console = Console()
app = typer.Typer()


@app.command()
def summary():
    while True:
        console.print("What would you like a summary of?")
        options = ["User", "Exit"]
        terminal_menu = TerminalMenu(options)
        menu_entry_index = terminal_menu.show()

        if menu_entry_index == 0:
            UserSummary().start()
        elif menu_entry_index == 1:
            break
    
    console.print("Goodbye!")


@app.command()
def add():
    while True:
        console.print("What would you like to add?")
        options = ["User", "Exit"]
        terminal_menu = TerminalMenu(options)
        menu_entry_index = terminal_menu.show()

        if menu_entry_index == 0:
            user = UserGenerator().generate()
            console.print("\nUser created successfully!\n", style="bold green")
            console.print(user, "\n")
        elif menu_entry_index == 1:
            break
    
    console.print("Goodbye!")
    

@app.command()
def update():
    while True:
        console.print("What would you like to update?")
        options = ["User", "Bots", "Exit"]
        terminal_menu = TerminalMenu(options)
        menu_entry_index = terminal_menu.show()

        if menu_entry_index == 0:
            UserUpdater().update()
        elif menu_entry_index == 1:
            BotUpdater().update()
        else:
            break
    
    console.print("Goodbye!")


if __name__ == "__main__":
    app()
