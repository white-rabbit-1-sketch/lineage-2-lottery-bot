import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Service.NavigatorService import NavigatorService
from Game.CasinoColorGame import CasinoColorGame
from Player.CasinoColorPlayer import CasinoColorPlayer
from Repository.HistoryRepository import HistoryRepository
from Repository.ModelRepository import ModelRepository
from Navigator.CasinoNavigator import CasinoNavigator
from Service.HistoryService import HistoryService
from Service.ModelService import ModelService

VAR_PATH = os.path.abspath("./../var/")
ASSETS_PATH = os.path.abspath("./../assets/")
WINDOW_TITLE = "Asterios"

if __name__ == '__main__':
    history_repository = HistoryRepository(VAR_PATH)
    history_service = HistoryService(history_repository)

    model_repository = ModelRepository(VAR_PATH)
    model_service = ModelService(model_repository)

    navigator_service = NavigatorService(ASSETS_PATH)
    casino_navigator = CasinoNavigator(navigator_service, WINDOW_TITLE)
    casino_color_game = CasinoColorGame(casino_navigator)

    player = CasinoColorPlayer(history_service, model_service, casino_color_game)
    player.play()