import os
import bcrypt

from bot import BotGenerator
from database import Database

from model import UserModel, CurrencyPairConfigModel, StrategyConfigModel, ApiKeyModel, PortfolioModel, BalanceModel
from enums import ExchangeType
from utils import generate_random_string
from simple_term_menu import TerminalMenu
from rich.prompt import Prompt, Confirm, FloatPrompt
from rich.console import Console

console = Console()


class UserGenerator:
    def __init__(self):
        self.email = None
        self.password_plain = None
        self.password = None
        self.is_admin = None
        self.starting_balance = None
        self.api_key = None
        self.api_secret = None
        self.bot = None

    def generate(self):
        email = Prompt.ask(
            "What is the email of the user?",
            default=f"{generate_random_string(10)}.{generate_random_string(5)}@yopmail.com",
        )
        password = Prompt.ask("What is the password of the user?", default=generate_random_string(10))
        self.email = email
        self.password_plain = password
        self.password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
        self.is_admin = Confirm.ask("Do you want to make this user an admin?", default=False)
        self.starting_balance = FloatPrompt.ask("What is the starting balance (USDT) of the user?", default=5000.0)

        # Generate api keys
        self.set_api_key()

        # Setup a bot
        self.set_bot()

        # Display overview
        self.display_overview()

        while not Confirm.ask("Are you happy with these settings?", default=True):
            options = [
                "Change email",
                "Change password",
                "Change admin status",
                "Change starting balance",
                "Change api key",
                "Change bot",
            ]
            terminal_menu = TerminalMenu(options)
            menu_entry_index = terminal_menu.show()
            if menu_entry_index == 0:
                self.email = Prompt.ask(
                    "What is the email of the user?",
                    default=f"{generate_random_string(10)}.{generate_random_string(5)}@yopmail.com",
                )
            elif menu_entry_index == 1:
                self.password_plain = Prompt.ask(
                    "What is the password of the user?", default=generate_random_string(10)
                )
                self.password = bcrypt.hashpw(self.password_plain.encode("utf-8"), bcrypt.gensalt())
            elif menu_entry_index == 2:
                self.is_admin = Confirm.ask("Do you want to make this user an admin?", default=False)
            elif menu_entry_index == 3:
                self.starting_balance = FloatPrompt.ask(
                    "What is the starting balance (USDT) of the user?", default=5000.0
                )
            elif menu_entry_index == 4:
                self.set_api_key()
            elif menu_entry_index == 5:
                self.set_bot()

            self.display_overview()

        self._add_to_db()

        return self

    def set_api_key(self):
        use_default_key = Confirm.ask("Do you want to use the default api key?", default=True)
        if not use_default_key:
            console.print("What exchange are you using?")
            options = [
                ExchangeType.BINANCE.value,
            ]
            terminal_menu = TerminalMenu(options)
            menu_entry_index = terminal_menu.show()
            self.exchange = ExchangeType(options[menu_entry_index])
            console.print(f"You have selected {self.exchange.value}!")
            self.api_key = Prompt.ask("What is the api key of the user?")
            self.api_secret = Prompt.ask("What is the api secret of the user?")
        else:
            self.exchange = ExchangeType.BINANCE
            self.api_key = os.getenv("BINANCE_API_KEY")
            self.api_secret = os.getenv("BINANCE_API_SECRET")

    def set_bot(self):
        is_setup_bot = Confirm.ask("Do you want to setup a bot for this user?", default=True)
        if is_setup_bot:
            self.bot = BotGenerator().generate()

    def _add_to_db(self):
        session = Database().get_session()
        user = UserModel(
            email=self.email,
            _password=self.password,
            is_admin=self.is_admin,
        )
        session.add(user)
        session.flush()

        # Add api key
        api_key = ApiKeyModel(
            user_id=user.id,
            exchange=self.exchange,
            api_key=self.api_key,
            api_secret=self.api_secret,
        )
        session.add(api_key)
        session.flush()

        # Add portfolio
        portfolio = PortfolioModel(user_id=user.id)
        session.add(portfolio)
        session.flush()

        # Add balance
        balance = BalanceModel(
            portfolio_id=portfolio.id,
            exchange=self.exchange,
            asset="USDT",
            free=self.starting_balance,
            locked=0,
            total=self.starting_balance,
        )
        session.add(balance)
        session.flush()

        # Add currency pair config
        currency_pair_config = CurrencyPairConfigModel(
            user_id=user.id,
            currency_pair=self.bot.symbol,
            bot_name=self.bot.name,
            exchange=self.exchange,
            interval=self.bot.interval,
            strategy=self.bot.strategy,
            is_active=self.bot.is_active,
            is_simulated=True,
        )
        session.add(currency_pair_config)
        session.flush()

        # Add strategy config
        for key, value in self.bot.strategy_config.items():
            strategy_config = StrategyConfigModel(
                currency_pair_config_id=currency_pair_config.id,
                strategy=self.bot.strategy,
                key=key,
                value=value,
            )
            session.add(strategy_config)
            session.flush()

        session.commit()
        session.close()

    def display_overview(self):
        console.print("=========== Overview ==========", style="bold green")
        console.print(f"Email: {self.email}", style="italic green")
        console.print(f"Password: {self.password_plain}", style="italic green")
        console.print(f"Admin: {self.is_admin}", style="italic green")
        console.print(f"Starting balance: {self.starting_balance}", style="italic green")
        console.print(f"Exchange: {self.exchange.value}", style="italic green")
        console.print(f"Bot: {self.bot}\n", style="italic green")

    def __repr__(self):
        return f"User: {self.email} | Password: {self.password_plain} | Admin: {self.is_admin} | Starting Balance: {self.starting_balance} | Bot: {self.bot}"

    def __str__(self):
        return f"User: {self.email} | Password: {self.password_plain} | Admin: {self.is_admin} | Starting Balance: {self.starting_balance} | Bot: {self.bot}"
