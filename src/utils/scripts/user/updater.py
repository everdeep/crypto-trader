import os
import bcrypt

from bot import BotGenerator
from database import Database

from model import UserModel, ApiKeyModel, PortfolioModel, BalanceModel, CurrencyPairModel, CurrencyPairConfigModel
from enums import ExchangeType
from utils import generate_random_string
from simple_term_menu import TerminalMenu
from rich.prompt import Prompt, Confirm, FloatPrompt
from rich.console import Console

console = Console()


class UserUpdater:
    def update(self):
        session = Database().get_session()
        email = Prompt.ask("\nWhat is the email of the user you would like to update?")
        while not Confirm.ask(f"Are you sure you want to update {email}?", default=True):
            email = Prompt.ask("What is the email of the user you would like to update?")

        # Fetch user
        user: UserModel = session.query(UserModel).filter(UserModel.email == email).first()
        if user is None:
            console.print(f"User with email {email} does not exist!\n", style="bold red")
            return

        while True:
            console.print("\nWhat would you like to update?")
            options = ["Email", "Password", "Admin status", "Balance", "API key", "Bot", "Back"]
            terminal_menu = TerminalMenu(options)
            menu_entry_index = terminal_menu.show()
            console.print(f"You have selected {options[menu_entry_index]}!\n")

            if menu_entry_index == 0:
                new_email = Prompt.ask(
                    "What is the new email of the user?",
                    default=f"{generate_random_string(10)}.{generate_random_string(5)}@yopmail.com",
                )
                result = session.query(UserModel).filter(UserModel.email == new_email).first()
                if result is None:
                    user.email = new_email
                    session.commit()
                    console.print(f"Email updated successfully!", style="bold green")
                else:
                    console.print(f"Email {new_email} already exists!", style="bold red")
            elif menu_entry_index == 1:
                new_password = Prompt.ask("What is the new password of the user?", default=generate_random_string(10))
                user.password = bcrypt.hashpw(new_password.encode("utf-8"), bcrypt.gensalt())
                session.commit()
                console.print(f"Password updated successfully!", style="bold green")
            elif menu_entry_index == 2:
                user.is_admin = Confirm.ask("Do you want to make this user an admin?", default=False)
                session.commit()
                console.print(f"Admin status updated successfully!\n", style="bold green")
            elif menu_entry_index == 3:
                self.update_balance(session, user)
            elif menu_entry_index == 4:
                self.update_api_key(session, user)
            elif menu_entry_index == 5:
                self.update_bot(session, user)
            elif menu_entry_index == 6:
                break

    def display_portfolio_summary(self, portfolio, user_id, email):
        console.print(f"Portfolio: {portfolio.id}, User: {email}", style="bold magenta")
        console.print("====================================", style="bold magenta")
        for balance in portfolio.balances:
            console.print(f"Asset: {balance.asset} -> ${balance.total}", style="italic magenta")
        print()

    def update_balance(self, session, user):
        portfolio = session.query(PortfolioModel).filter_by(user_id=user.id).first()
        self.display_portfolio_summary(portfolio, user.id, user.email)

        while True:
            console.print("Do you want to update or add a balance?")
            options = ["Update", "Add", "Back"]
            terminal_menu = TerminalMenu(options)
            menu_entry_index = terminal_menu.show()
            console.print(f"You have selected {options[menu_entry_index]}!\n")

            if menu_entry_index == 0:
                console.print("What asset would you like to update?")
                console.print("Warning: This will reset the total balance of the asset!", style="bold yellow")
                console.print("Any currently locked balances will remain due to order updates.", style="bold yellow")
                options = [balance.asset for balance in portfolio.balances]
                terminal_menu = TerminalMenu(options)
                sub_menu_index = terminal_menu.show()
                console.print(f"You have selected {options[sub_menu_index]}!\n")
                new_balance = FloatPrompt.ask("What is the new balance?", default=0.0)
                balance = (
                    session.query(BalanceModel)
                    .filter_by(portfolio_id=portfolio.id, asset=options[sub_menu_index])
                    .first()
                )
                balance.total -= balance.free
                balance.total += new_balance
                balance.free = new_balance
                session.commit()
                console.print(f"Balance updated successfully!\n", style="bold green")
            elif menu_entry_index == 1:
                asset = Prompt.ask("What is the asset name?", default="BTC")
                total = FloatPrompt.ask("How much balance do you want to set?", default=0.0)
                console.print("What exchange is this balance on?")
                options = [
                    ExchangeType.BINANCE.value,
                ]
                terminal_menu = TerminalMenu(options)
                sub_menu_index = terminal_menu.show()
                console.print(f"You have selected {options[sub_menu_index]}!\n")
                balance = BalanceModel(
                    asset=asset,
                    exchange=ExchangeType(options[sub_menu_index]),
                    total=total,
                    locked=0.0,
                    free=total,
                    portfolio_id=portfolio.id,
                )
                session.add(balance)
                session.commit()
                console.print(f"Balance added successfully!\n", style="bold green")
            elif menu_entry_index == 2:
                break

    def update_api_key(self, session, user):
        apikey = session.query(ApiKeyModel).filter_by(user_id=user.id).first()
        use_default_key = Confirm.ask("Do you want to use the default api key?", default=True)
        if not use_default_key:
            print("What exchange are you using?")
            options = [
                ExchangeType.BINANCE.value,
            ]
            terminal_menu = TerminalMenu(options)
            menu_entry_index = terminal_menu.show()
            apikey.exchange = ExchangeType(options[menu_entry_index])
            print(f"You have selected {apikey.exchange.value}!")
            apikey.api_key = Prompt.ask("What is the api key of the user?")
            apikey.api_secret = Prompt.ask("What is the api secret of the user?")
        else:
            apikey.exchange = ExchangeType.BINANCE
            apikey.api_key = os.getenv("BINANCE_API_KEY")
            apikey.api_secret = os.getenv("BINANCE_API_SECRET")

        session.commit()
        console.print(f"API key updated successfully!\n", style="bold green")

    def update_bot(self, session, user):
        options = [bot.currency_pair for bot in user.currency_pair_configs]
        terminal_menu = TerminalMenu(options)
        menu_entry_index = terminal_menu.show()
        bot: CurrencyPairConfigModel = user.currency_pair_configs[menu_entry_index]
        while True:
            console.print("What would you like to do?")
            options = ["Update symbol", "Update exchange", "Update strategy", "Update strategy config", "Enable/Disable bot", "Decomission", "Back"]
            terminal_menu = TerminalMenu(options)
            menu_entry_index = terminal_menu.show()
            console.print(f"You have selected {options[menu_entry_index]}!\n")

            if menu_entry_index == 0:
                console.print("Warning: This will not automatically transfer funds for you!", style="bold yellow")
                console.print("Please ensure you have sufficient funds in your account.", style="bold yellow")
                console.print(
                    "If you are unsure, please use the summary option to find the current user balance.",
                    style="bold yellow",
                )
                new_currency_pair = Prompt.ask("\nWhat is the new currency pair?", default=bot.currency_pair)
                bot.currency_pair = new_currency_pair
                session.commit()
                console.print(f"Currency pair updated successfully!\n", style="bold green")
            elif menu_entry_index == 1:
                exchange = BotGenerator().set_exchange(bot.exchange)
                if exchange is None:
                    continue
                bot.exchange = exchange
                session.commit()
                console.print(f"Exchange updated successfully!\n", style="bold green")
            elif menu_entry_index == 2:
                new_strategy = BotGenerator().set_strategy(bot.strategy)
                if new_strategy is None:
                    continue
                bot.strategy = new_strategy
                session.commit()
                console.print(f"Strategy updated successfully!\n", style="bold green")
            elif menu_entry_index == 3:
                new_strategy_config = BotGenerator().set_strategy_config(bot.strategy, bot.strategy_config)
                if new_strategy_config is None:
                    continue

                for key, value in new_strategy_config.items():
                    for strategy_config in bot.strategy_config:
                        if strategy_config.key == key:
                            strategy_config.value = value
                session.commit()
                console.print(f"Strategy config updated successfully!\n", style="bold green")
            elif menu_entry_index == 4:
                console.print("What would you like to do?")
                options = ["Enable", "Disable", "Back"]
                terminal_menu = TerminalMenu(options)
                sub_menu_index = terminal_menu.show()
                console.print(f"You have selected {options[sub_menu_index]}!\n")
                if sub_menu_index == 0:
                    bot.active = True
                elif sub_menu_index == 1:
                    bot.active = False
                elif sub_menu_index == 2:
                    return

                session.commit()
                console.print(f"Bot active status updated successfully!\n", style="bold green")
            
            elif menu_entry_index == 5:
                bot.is_active = False
                bot.is_decommissioned = True
                session.commit()
                console.print(f"Bot decommissioned successfully!\n", style="bold green")
            elif menu_entry_index == 5:
                break
