import random

from utils import generate_random_string, generate_random_digit
from enums import Interval, StrategyParams, StrategyType, ExchangeType
from simple_term_menu import TerminalMenu
from rich.prompt import Prompt, Confirm, IntPrompt
from rich.console import Console

console = Console()


class BotGenerator:
    def __init__(self) -> None:
        self.name = None
        self.exchange = None
        self.strategy = None
        self.strategy_config = None
        self.interval = None
        self.symbol = None
        self.is_active = None

    def generate(self) -> dict:
        self.name = Prompt.ask("What is the name of the bot?", default=f"Bot#{generate_random_digit(4)}")

        # Setup currency pair config
        self.set_strategy()

        # Setup strategy config
        self.set_strategy_config()

        # Setup interval
        self.set_interval()

        # Target symbol
        self.symbol = Prompt.ask("What is the target symbol?", default="BTCUSDT")

        # Active status
        self.is_active = Confirm.ask("Do you want to activate this bot?", default=False)

        # Display bot overview using rich
        self.display_bot_overview()

        while not Confirm.ask("Are you happy with your bot settings?", default=True):
            options = [
                "Change name",
                "Change exchange",
                "Change strategy",
                "Change strategy config",
                "Change interval",
                "Change symbol",
                "Change active status",
            ]
            terminal_menu = TerminalMenu(options)
            menu_entry_index = terminal_menu.show()
            if (menu_entry_index == 0):
                self.name = Prompt.ask("What is the name of the bot?", default=f"Bot#{generate_random_digit(4)}")
            elif (menu_entry_index == 1):
                self.set_exchange()
            elif (menu_entry_index == 2):
                self.set_strategy()
                self.set_strategy_config()
            elif (menu_entry_index == 3):
                self.set_strategy_config()
            elif (menu_entry_index == 4):
                self.set_interval()
            elif (menu_entry_index == 5):
                self.symbol = Prompt.ask("What is the target symbol?", default="BTCUSDT")
            elif (menu_entry_index == 6):
                self.is_active = Confirm.ask("Do you want to activate this bot?", default=False)
            
            self.display_bot_overview()

        return self

    def set_exchange(self, current_exchange=None):
        if current_exchange:
            console.print(f"Current exchange: {current_exchange.value}", style="bold yellow")

        console.print("Please select the exchange to use?")
        options = [
            ExchangeType.BINANCE.value,
            'Cancel'
        ]
        terminal_menu = TerminalMenu(options)
        menu_entry_index = terminal_menu.show()
        if (menu_entry_index == len(options) - 1):
            return

        console.print(f"You have selected {options[menu_entry_index]}!\n")
        self.exchange = ExchangeType(options[menu_entry_index])
        return self.exchange

    def set_strategy(self, current_strategy=None):
        # Setup strategy
        if current_strategy:
            console.print(f"Current strategy: {current_strategy.value}", style="bold yellow")

        console.print("What strategy would you like to use?")
        options = [
            StrategyType.AVERAGE_DIRECTIONAL_INDEX.value,
            StrategyType.BOLLINGER_BANDS.value,
            StrategyType.COMMODITY_CHANNEL_INDEX.value,
            StrategyType.MACD.value,
            StrategyType.MACD_RSI.value,
            StrategyType.MOVING_AVERAGE_CROSSOVER.value,
            StrategyType.RSI.value,
            StrategyType.STOCHASTIC_OSCILLATOR.value,
            StrategyType.WILLIAMS_R.value,
            "Cancel"
        ]
        terminal_menu = TerminalMenu(options)
        menu_entry_index = terminal_menu.show()
        if (menu_entry_index == len(options) - 1):
            return
        
        console.print(f"You have selected {options[menu_entry_index]}!")
        self.strategy = StrategyType(options[menu_entry_index])
        return self.strategy


    def set_strategy_config(self, strategy=None, current_strategy_config=None):
        if strategy:
            self.strategy = strategy
        if current_strategy_config:
            console.print(f"Current strategy config:", style="bold yellow")
            for key, value in current_strategy_config.items():
                console.print(f"{key}: {value}", style="bold yellow")

        if not Confirm.ask("\nDo you want to continue?", default=True):
            return
        
        print()

        # Setup strategy config
        strategy_config = {}
        for key, value in StrategyParams[self.strategy.name].value.items():
            strategy_config[key] = IntPrompt.ask(
                f"What is the {key} for {self.strategy.value}?", default=random.randint(value[0], value[1])
            )

        self.strategy_config = strategy_config
        return self.strategy_config


    def set_interval(self, current_interval=None):
        if current_interval:
            console.print(f"Current interval: {current_interval}")
        console.print("What interval would you like to use?")
        options = [
            Interval.MINUTE_1.value,
            Interval.MINUTE_3.value,
            Interval.MINUTE_5.value,
            Interval.MINUTE_15.value,
            Interval.MINUTE_30.value,
            Interval.HOUR_1.value,
            Interval.HOUR_2.value,
            Interval.HOUR_4.value,
            Interval.HOUR_6.value,
            Interval.HOUR_8.value,
            Interval.HOUR_12.value,
            Interval.DAY_1.value,
        ]
        terminal_menu = TerminalMenu(options)
        menu_entry_index = terminal_menu.show()
        self.interval = Interval(options[menu_entry_index])
        print(f"You have selected {self.interval.value}!")
        return self.interval

    def display_bot_overview(self):
        console.print(f"=========== Overview ==========", style="bold green")
        console.print(f"Name: {self.name}", style="italic green")
        console.print(f"Exchange: {self.exchange}", style="italic green")
        console.print(f"Strategy: {self.strategy.value}", style="italic green")
        console.print(f"Strategy Config: {self.strategy_config}", style="italic green")
        console.print(f"Interval: {self.interval.value}", style="italic green")
        console.print(f"Symbol: {self.symbol}", style="italic green")
        console.print(f"Active: {self.is_active}", style="italic green")
    
    def __repr__(self) -> str:
        return f"BotGenerator(name={self.name}, strategy={self.strategy}, strategy_config={self.strategy_config}, interval={self.interval}, symbol={self.symbol})"