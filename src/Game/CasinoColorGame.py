from Dto.Game.CasinoColorGameResult import CasinoColorGameResult
from Navigator.CasinoNavigator import CasinoNavigator

COLOR_CODE_RED = 0
COLOR_CODE_BLACK = 1
COLOR_CODE_ZERO = 2

COLOR_CODE_TITLE_MAP = {
    COLOR_CODE_RED: "red",
    COLOR_CODE_BLACK: "black",
    COLOR_CODE_ZERO: "zero",
}

GAME_RESULT_CODE_WIN = 1
GAME_RESULT_CODE_LOSE = 0

GAME_RESULT_CODE_TITLE_MAP = {
    GAME_RESULT_CODE_WIN: "win",
    GAME_RESULT_CODE_LOSE: "loss",
}

class CasinoColorGame:
    def __init__(self, navigator: CasinoNavigator):
        self.navigator = navigator
        self.is_window_activated = False
        self.previous_bid_color = None
        self.previous_bid_amount = None
        self.previous_result_color = None
        self.wins_streak_size = 0
        self.losses_streak_size = 0
        self.result_color_streak_size = 0

    def play(self, bid_color: int, bid_amount: int) -> CasinoColorGameResult:
        casino_color_game_result = CasinoColorGameResult(bid_color, bid_amount)

        if not self.is_window_activated:
            self.navigator.activate()
            self.is_window_activated = True

        if (
                self.previous_bid_color == bid_color and
                self.previous_bid_amount == bid_amount and
                self.navigator.is_retry_available()
        ):
            self.navigator.retry()
        else:
            self.navigator.back(False)
            self.navigator.set_bid(bid_amount)

            if bid_color == COLOR_CODE_RED or bid_color == COLOR_CODE_ZERO:
                self.navigator.chose_red()
            elif bid_color == COLOR_CODE_BLACK:
                self.navigator.chose_black()

        if self.navigator.is_red_result():
            casino_color_game_result.set_result_color(COLOR_CODE_RED)
        elif self.navigator.is_black_result():
            casino_color_game_result.set_result_color(COLOR_CODE_BLACK)
        elif self.navigator.is_zero_result():
            casino_color_game_result.set_result_color(COLOR_CODE_ZERO)
        else:
            raise Exception("Cannot find game color result")

        if self.navigator.is_success_result():
            casino_color_game_result.mark_as_win()
        elif self.navigator.is_loss_result():
            casino_color_game_result.mark_as_fail()
        else:
            raise Exception("Cannot find game final result")

        if not casino_color_game_result.get_result_color() == COLOR_CODE_ZERO:
            if self.navigator.is_success_result():
                self.losses_streak_size = 0
                self.wins_streak_size += 1
            elif self.navigator.is_loss_result():
                self.losses_streak_size += 1
                self.wins_streak_size = 0
            else:
                raise Exception("Cannot find game final result")

            if casino_color_game_result.get_result_color() == self.previous_result_color:
                self.result_color_streak_size += 1
            else: self.result_color_streak_size = 1

        casino_color_game_result.set_wins_streak_size(self.wins_streak_size)
        casino_color_game_result.set_losses_streak_size(self.losses_streak_size)
        casino_color_game_result.set_result_color_streak_size(self.result_color_streak_size)

        self.previous_bid_color = bid_color
        self.previous_bid_amount = bid_amount
        self.previous_result_color = casino_color_game_result.get_result_color()

        return casino_color_game_result