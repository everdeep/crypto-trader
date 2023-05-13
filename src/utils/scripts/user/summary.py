from database import Database
from model import UserModel, PortfolioModel
from simple_term_menu import TerminalMenu
from rich.prompt import Prompt, Confirm
from rich.console import Console

console = Console()


class UserSummary:
    def start(self):
        session = Database().get_session()

        while True:
            options = ["General", "Single user", "Back"]
            terminal_menu = TerminalMenu(options)
            menu_entry_index = terminal_menu.show()

            if menu_entry_index == 0:
                while True:
                    options = ["Total users", "Total admins", "List Users", "List P&L", "Back"]
                    terminal_menu = TerminalMenu(options)
                    sub_menu_index = terminal_menu.show()

                    if sub_menu_index == 0:
                        total_users = session.query(UserModel).count()
                        console.print(f"Total users: {total_users}\n", style="bold green")
                    elif sub_menu_index == 1:
                        total_admins = session.query(UserModel).filter_by(is_admin=True).count()
                        console.print(f"Total admins: {total_admins}\n", style="bold green")
                    elif sub_menu_index == 2:
                        users = session.query(UserModel).all()
                        console.print("Users", style="bold green")
                        console.print("====================================", style="bold magenta")
                        for user in users:
                            console.print(f"ID: {user.id} -> {user.email}", style="italic magenta")
                        print()
                    elif sub_menu_index == 3:
                        users = session.query(UserModel).all()
                        console.print("Portfolios", style="bold green")
                        console.print("====================================", style="bold magenta")
                        for user in users:
                            portfolio = user.portfolio
                            console.print(
                                f"ID: {portfolio.id} -> {user.email} | P&L: ${portfolio.total_earnings}",
                                style="italic magenta",
                            )
                        print()
                    elif sub_menu_index == 4:
                        break
            elif menu_entry_index == 1:
                # Get email
                email = Prompt.ask("Please enter the email of the user")
                while not Confirm.ask(f"Is the following email correct? {email}", default=True):
                    email = Prompt.ask("Please enter the email of the user")

                # Fetch user
                user = session.query(UserModel).filter(UserModel.email == email).first()
                if user is None:
                    console.print(f"User with email {email} does not exist!\n", style="bold red")
                    return

                while True:
                    console.print("\nWhat would you like a summary on?")
                    options = ["User details", "Portfolio", "Active bots", "Bot configs", "Orders", "Back"]
                    terminal_menu = TerminalMenu(options)
                    sub_menu_index = terminal_menu.show()
                    console.print(f"You have selected {options[sub_menu_index]}!\n")

                    if sub_menu_index == 0:
                        self.display_user_summary(user)
                    elif sub_menu_index == 1:
                        portfolio = session.query(PortfolioModel).filter_by(user_id=user.id).first()
                        self.display_portfolio_summary(portfolio, user.email)
                    elif sub_menu_index == 2:
                        self.display_bot_summary(user)
                    elif sub_menu_index == 3:
                        self.display_bot_config_summary(user)
                    elif sub_menu_index == 4:
                        self.display_order_summary(user)
                    elif sub_menu_index == 5:
                        break
            elif menu_entry_index == 2:
                break

    def display_user_summary(self, user):
        console.print(f"User: {user.email}", style="bold magenta")
        console.print("====================================", style="bold magenta")
        console.print(f"ID: {user.id}", style="italic magenta")
        console.print(f"Admin: {user.is_admin}", style="italic magenta")
        console.print(f"Active: {user.is_active}", style="italic magenta")
        console.print(f"Verified: {user.is_verified}", style="italic magenta")
        console.print(f"Name: {user.first_name} {user.last_name}", style="italic magenta")
        console.print(f"DOB: {user.dob}", style="italic magenta")
        console.print(f"Address: {user.address}", style="italic magenta")
        console.print(f"API keys: {user.api_keys}", style="italic magenta")
        console.print(f"Created at: {user.created_at}", style="italic magenta")
        console.print(f"Settings: {user.settings}", style="italic magenta")
        print()

    def display_portfolio_summary(self, portfolio, email):
        console.print(f"Portfolio: {portfolio.id}, User: {email}", style="bold magenta")
        console.print("====================================", style="bold magenta")
        for balance in portfolio.balances:
            console.print(f"Asset: {balance.asset} -> ${balance.total}", style="italic magenta")
        print()

    def display_bot_summary(self, user):
        console.print(f"Active bots for user: {user.email}", style="bold magenta")
        for bot in user.currency_pair_configs:
            console.print("====================================", style="bold magenta")
            if not bot.is_active:
                continue

            console.print(f"ID: {bot.id}", style="italic magenta")
            console.print(f"Name: {bot.bot_name}", style="italic magenta")
            console.print(f"Exchange: {bot.exchange}", style="italic magenta")
            console.print(f"Currency pair: {bot.currency_pair}", style="italic magenta")
            console.print(f"Initial balance: {bot.allocated_balance}", style="italic magenta")
            console.print(f"Currency: {bot.currency_free + bot.currency_locked}", style="italic magenta")
            console.print(f"Asset: {bot.asset_free + bot.asset_locked}", style="italic magenta")
            console.print(f"Strategy: {bot.strategy}", style="italic magenta")
            console.print(f"Interval: {bot.interval}", style="italic magenta")
            console.print(f"Updated at: {bot.updated_at}", style="italic magenta")
            console.print(f"Signal: {bot.signal.signal.name}", style="italic magenta")
            # console.print(f"Config: {bot.strategy_config}", style="italic magenta")
            print()

    def display_bot_config_summary(self, user):
        console.log("Select a symbol to view the config for:", style="bold cyan")
        options = [bot.currency_pair for bot in user.currency_pair_configs]
        terminal_menu = TerminalMenu(options)
        sub_menu_index = terminal_menu.show()

        for bot in user.currency_pair_configs:
            if bot.currency_pair != options[sub_menu_index]:
                continue
            console.print(f"Bot config for user: {user.email} -> {bot.currency_pair}", style="bold magenta")
            console.print("====================================", style="bold magenta")
            console.print(f"ID: {bot.id}", style="italic magenta")
            console.print(f"Name: {bot.bot_name}", style="italic magenta")
            console.print(f"Exchange: {bot.exchange}", style="italic magenta")
            console.print(f"Currency pair: {bot.currency_pair}", style="italic magenta")
            console.print(f"Strategy: {bot.strategy}", style="italic magenta")
            console.print(f"Interval: {bot.interval}", style="italic magenta")
            console.print(f"Updated at: {bot.updated_at}", style="italic magenta")
            console.print(f"Signal: {bot.signal}", style="italic magenta")
            console.print(f"Config:", style="italic magenta")
            for config in bot.strategy_config:
                console.print(f"--> {config.key}: {config.value}", style="italic magenta")
            print()

    def display_order_summary(self, user):
        options = ["All orders", "Orders for a crypto", "Back"]
        terminal_menu = TerminalMenu(options)
        sub_menu_index = terminal_menu.show()

        if sub_menu_index == 0:
            console.print(f"Active orders for user: {user.email}", style="bold magenta")
            for order in user.orders:
                console.print("====================================", style="bold magenta")
                console.print(f"ID: {order.id}", style="italic magenta")
                console.print(f"User ID: {order.user_id}", style="italic magenta")
                console.print(f"Currency pair: {order.currency_pair}", style="italic magenta")
                console.print(f"Order ID: {order.order_id}", style="italic magenta")
                console.print(f"Bot ID: {order.bot_id}", style="italic magenta")
                console.print(f"Exchange: {order.exchange}", style="italic magenta")
                console.print(f"Cost: {order.cost}", style="italic magenta")
                console.print(f"Last price: {order.last_price}", style="italic magenta")
                console.print(f"Amount: {order.amount}", style="italic magenta")
                console.print(f"Side: {order.side}", style="italic magenta")
                console.print(f"Status: {order.status}", style="italic magenta")
                console.print(f"Type: {order.type}", style="italic magenta")
                console.print(f"Limit price: {order.limit_price}", style="italic magenta")
                console.print(f"Is autotraded: {order.is_autotraded}", style="italic magenta")
                console.print(f"Created at: {order.created_at}", style="italic magenta")
                console.print(f"Updated at: {order.updated_at}", style="italic magenta")
                print()
        if sub_menu_index == 1:
            options = [balance.asset for balance in user.portfolio.balances]
            terminal_menu = TerminalMenu(options)
            sub_menu_index = terminal_menu.show()

            console.print(f"Active orders for user: {user.email}", style="bold magenta")
            for order in user.orders:
                if options[sub_menu_index] not in order.currency_pair:
                    continue
                console.print("====================================", style="bold magenta")
                console.print(f"ID: {order.id}", style="italic magenta")
                console.print(f"User ID: {order.user_id}", style="italic magenta")
                console.print(f"Currency pair: {order.currency_pair}", style="italic magenta")
                console.print(f"Order ID: {order.order_id}", style="italic magenta")
                console.print(f"Bot ID: {order.bot_id}", style="italic magenta")
                console.print(f"Exchange: {order.exchange}", style="italic magenta")
                console.print(f"Cost: {order.cost}", style="italic magenta")
                console.print(f"Last price: {order.last_price}", style="italic magenta")
                console.print(f"Amount: {order.amount}", style="italic magenta")
                console.print(f"Side: {order.side}", style="italic magenta")
                console.print(f"Status: {order.status}", style="italic magenta")
                console.print(f"Type: {order.type}", style="italic magenta")
                console.print(f"Limit price: {order.limit_price}", style="italic magenta")
                console.print(f"Is autotraded: {order.is_autotraded}", style="italic magenta")
                console.print(f"Created at: {order.created_at}", style="italic magenta")
                console.print(f"Updated at: {order.updated_at}", style="italic magenta")
                print()
