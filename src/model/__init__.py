from .user import UserModel
from .usersettings import UserSettingsModel
from .portfolio import PortfolioModel
from .portfoliohistory import PortfolioHistoryModel
from .apikey import ApiKeyModel
from .symbol import SymbolModel
from .currencypair import CurrencyPairModel
from .currencypairconfig import CurrencyPairConfigModel
from .strategyconfig import StrategyConfigModel
from .signal import SignalModel
from .balance import BalanceModel
from .balancehistory import BalanceHistoryModel
from .order import OrderModel
from .address import AddressModel

from sqlalchemy.orm import relationship

# Mapping relationships
PortfolioModel.balances = relationship(BalanceModel, backref="portfolio")
# PortfolioModel.history = relationship(PortfolioHistoryModel, backref="portfolio")
# BalanceModel.history = relationship(BalanceHistoryModel, backref="balance")

SymbolModel.currency_pairs = relationship(CurrencyPairModel, backref="symbols")

UserModel.settings = relationship(UserSettingsModel, backref="users")
UserModel.api_keys = relationship(ApiKeyModel, backref="users")
UserModel.portfolio = relationship(PortfolioModel, backref="users", uselist=False)
UserModel.address = relationship(AddressModel, backref="users")
UserModel.orders = relationship(OrderModel, backref="users")
UserModel.currency_pair_configs = relationship(CurrencyPairConfigModel, backref="users")

CurrencyPairConfigModel.signal = relationship(
    SignalModel, backref="currency_pair_configs", uselist=False
)
CurrencyPairConfigModel.orders = relationship(
    OrderModel, backref="currency_pair_configs"
)
CurrencyPairConfigModel.strategy_config = relationship(
    StrategyConfigModel, backref="currency_pair_configs"
)
