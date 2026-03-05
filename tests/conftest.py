import sys
from unittest.mock import MagicMock
import importlib

mock_rbrapi = MagicMock()
mock_errors = MagicMock()

class AuthError(Exception):
    pass

class BonusError(Exception):
    pass

class LootBoxError(Exception):
    pass

mock_errors.AuthenticationError = AuthError
mock_errors.CollectTimedBonusError = BonusError
mock_errors.LootBoxError = LootBoxError
mock_rbrapi.errors = mock_errors
mock_rbrapi.RocketBotRoyale = MagicMock(name='RocketBotRoyale')

sys.modules['rbrapi'] = mock_rbrapi
sys.modules['rbrapi.errors'] = mock_errors
