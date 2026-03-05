import sys
import os
from unittest.mock import patch, MagicMock

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TestBuyCrate:
    def test_successful_purchase(self):
        with patch.dict(os.environ, {"EMAIL": "test@example.com", "PASSWORD": "testpass"}):
            with patch("sys.argv", ["buy_crate.py"]):
                with patch("sys.exit"):
                    with patch("buy_crate.RocketBotRoyale") as mock_client:
                        mock_client_instance = MagicMock()
                        mock_client.return_value = mock_client_instance
                        mock_client_instance.account.return_value.wallet = {"coins": 2000}
                        
                        mock_award = MagicMock()
                        mock_award.award_id = "golden_chest"
                        mock_client_instance.buy_crate.return_value = mock_award
                        
                        from buy_crate import main
                        main()
                    
                    mock_client.assert_called_once_with("test@example.com", "testpass")
                    mock_client_instance.buy_crate.assert_called_once()

    def test_insufficient_coins(self):
        with patch.dict(os.environ, {"EMAIL": "test@example.com", "PASSWORD": "testpass"}):
            with patch("sys.argv", ["buy_crate.py"]):
                with patch("buy_crate.RocketBotRoyale") as mock_client:
                    mock_client_instance = MagicMock()
                    mock_client.return_value = mock_client_instance
                    mock_client_instance.account.return_value.wallet = {"coins": 500}
                    
                    with patch("sys.exit", side_effect=SystemExit(0)):
                        from buy_crate import main
                        try:
                            main()
                        except SystemExit:
                            pass
                    
                    mock_client_instance.buy_crate.assert_not_called()

    def test_authentication_error(self):
        exit_mock = MagicMock()
        with patch.dict(os.environ, {"EMAIL": "test@example.com", "PASSWORD": "testpass"}):
            with patch("sys.argv", ["buy_crate.py"]):
                with patch("buy_crate.RocketBotRoyale") as mock_client:
                    mock_client.side_effect = Exception("Invalid credentials")
                    
                    with patch("sys.exit", exit_mock):
                        from buy_crate import main
                        try:
                            main()
                        except SystemExit:
                            pass
                    
                    mock_client.assert_called_once()

    def test_lootbox_error(self):
        exit_mock = MagicMock()
        with patch.dict(os.environ, {"EMAIL": "test@example.com", "PASSWORD": "testpass"}):
            with patch("sys.argv", ["buy_crate.py"]):
                with patch("buy_crate.RocketBotRoyale") as mock_client:
                    mock_client_instance = MagicMock()
                    mock_client.return_value = mock_client_instance
                    mock_client_instance.account.return_value.wallet = {"coins": 2000}
                    mock_client_instance.buy_crate.side_effect = Exception("Out of stock")
                    
                    with patch("sys.exit", exit_mock):
                        from buy_crate import main
                        try:
                            main()
                        except SystemExit:
                            pass
                    
                    mock_client_instance.buy_crate.assert_called_once()

    def test_no_logging_flag(self):
        with patch.dict(os.environ, {"EMAIL": "test@example.com", "PASSWORD": "testpass"}):
            with patch("sys.argv", ["buy_crate.py", "--no-logging"]):
                with patch("sys.exit"):
                    with patch("buy_crate.RocketBotRoyale") as mock_client:
                        mock_client_instance = MagicMock()
                        mock_client.return_value = mock_client_instance
                        mock_client_instance.account.return_value.wallet = {"coins": 2000}
                        
                        mock_award = MagicMock()
                        mock_award.award_id = "golden_chest"
                        mock_client_instance.buy_crate.return_value = mock_award
                        
                        from buy_crate import main
                        main()
                    
                    mock_client_instance.buy_crate.assert_called_once()
