class CasinoColorGameResult:
    def __init__(
        self,
        bid_color: int,
        bid_amount:int,
        is_win: bool = False
    ):
        self.bid_color = bid_color
        self.bid_amount = bid_amount
        self.result_color = None
        self.is_win = is_win
        self.wins_streak_size = 0
        self.losses_streak_size = 0
        self.result_color_streak_size = 0

    def get_bid_color(self) -> int:
        return self.bid_color

    def set_bid_color(self, bid_color: int) -> None:
        self.bid_color = bid_color

    def get_bid_amount(self) -> int:
        return self.bid_amount

    def set_bid_amount(self, bid_amount: int) -> None:
        self.bid_amount = bid_amount

    def get_result_color(self) -> int:
        return self.result_color

    def set_result_color(self, result_color: int) -> None:
        self.result_color = result_color

    def get_is_win(self) -> bool:
        return self.is_win

    def mark_as_win(self) -> None:
        self.is_win = True

    def mark_as_fail(self) -> None:
        self.is_win = False

    def get_wins_streak_size(self) -> int:
        return self.wins_streak_size

    def set_wins_streak_size(self, wins_streak_size: int) -> None:
        self.wins_streak_size = wins_streak_size

    def inc_wins_streak_size(self) -> None:
        self.wins_streak_size += 1

    def get_losses_streak_size(self) -> int:
        return self.losses_streak_size

    def set_losses_streak_size(self, losses_streak_size: int) -> None:
        self.losses_streak_size = losses_streak_size

    def inc_losses_streak_size(self) -> None:
        self.losses_streak_size += 1

    def get_result_color_streak_size(self) -> int:
        return self.result_color_streak_size

    def set_result_color_streak_size(self, result_color_streak_size: int) -> None:
        self.result_color_streak_size = result_color_streak_size

    def inc_result_color_streak_size(self) -> None:
        self.result_color_streak_size += 1

