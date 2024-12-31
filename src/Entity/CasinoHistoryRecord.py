from datetime import datetime
from Entity.AbstractHistoryRecord import AbstractHistoryRecord

class CasinoHistoryRecord(AbstractHistoryRecord):
    def __init__(
        self,
        is_win: bool,
        game_result_color: int,
        reds_count: int,
        blacks_count: int,
        zeros_count: int,
        top_reds_count: int,
        top_blacks_count: int,
        top_zeros_count: int,
        result_color_streak_size: int
    ):
        self.is_win = is_win
        self.game_result_color = game_result_color
        self.reds_count = reds_count
        self.blacks_count = blacks_count
        self.zeros_count = zeros_count
        self.top_reds_count = top_reds_count
        self.top_blacks_count = top_blacks_count
        self.top_zeros_count = top_zeros_count
        self.result_color_streak_size = result_color_streak_size
        self.timestamp = datetime.now()

    def get_is_win(self) -> int:
        return self.is_win

    def get_game_result_color(self) -> int:
        return self.game_result_color

    def get_reds_count(self) -> int:
        return self.reds_count

    def get_blacks_count(self) -> int:
        return self.blacks_count

    def get_zeros_count(self) -> int:
        return self.zeros_count

    def get_top_reds_count(self) -> int:
        return self.top_reds_count

    def get_top_blacks_count(self) -> int:
        return self.top_blacks_count

    def get_top_zeros_count(self) -> int:
        return self.top_zeros_count

    def get_result_color_streak_size(self) -> int:
        return self.result_color_streak_size

    def get_timestamp(self):
        return self.timestamp.timestamp()