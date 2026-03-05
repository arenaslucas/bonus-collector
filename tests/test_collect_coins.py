import sys
import os
from unittest.mock import patch, MagicMock

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TestCollectCoins:
    def test_successful_collection(self):
        with patch.dict(os.environ, {"EMAIL": "test@example.com", "PASSWORD": "testpass"}):
            with patch("sys.argv", ["collect_coins.py"]):
                with patch("collect_coins.RocketBotRoyale") as mock_client:
                    mock_client_instance = MagicMock()
                    mock_client.return_value = mock_client_instance
                    mock_client_instance.account.return_value.wallet = {"coins": 500}
                    
                    from collect_coins import main
                    main()
                
                mock_client.assert_called_once_with("test@example.com", "testpass")
                mock_client_instance.collect_timed_bonus.assert_called_once()

    def test_missing_credentials(self):
        with patch.dict(os.environ, {}, clear=True):
            with patch("collect_coins.parse_args") as mock_args:
                mock_args.return_value = MagicMock(email=None, password=None, no_logging=False)
                
                from collect_coins import main
                main()
                
                mock_args.assert_called()

    def test_authentication_error(self):
        with patch.dict(os.environ, {"EMAIL": "test@example.com", "PASSWORD": "testpass"}):
            with patch("sys.argv", ["collect_coins.py"]):
                with patch("collect_coins.RocketBotRoyale") as mock_client:
                    mock_client.side_effect = Exception("Invalid credentials")
                    
                    from collect_coins import main
                    main()
                
                mock_client.assert_called_once()

    def test_collect_bonus_error(self):
        with patch.dict(os.environ, {"EMAIL": "test@example.com", "PASSWORD": "testpass"}):
            with patch("sys.argv", ["collect_coins.py"]):
                with patch("collect_coins.RocketBotRoyale") as mock_client:
                    mock_client_instance = MagicMock()
                    mock_client.return_value = mock_client_instance
                    mock_client_instance.collect_timed_bonus.side_effect = Exception("Not available")
                    
                    from collect_coins import main
                    main()
                
                mock_client_instance.collect_timed_bonus.assert_called_once()

    def test_no_logging_flag(self):
        with patch.dict(os.environ, {"EMAIL": "test@example.com", "PASSWORD": "testpass"}):
            with patch("sys.argv", ["collect_coins.py", "--no-logging"]):
                with patch("collect_coins.RocketBotRoyale") as mock_client:
                    mock_client_instance = MagicMock()
                    mock_client.return_value = mock_client_instance
                    mock_client_instance.account.return_value.wallet = {"coins": 500}
                    
                    from collect_coins import main
                    main()
                
                mock_client_instance.collect_timed_bonus.assert_called_once()
