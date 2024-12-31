class CasinoColorGameSession:
    def __init__(self):
        self.wins_count = 0
        self.losses_count = 0
        self.reds_count = 0
        self.blacks_count = 0
        self.zeros_count = 0
        self.correct_predictions_count = 0
        self.incorrect_predictions_count = 0
        self.wins_correct_predictions_count = 0
        self.wins_incorrect_predictions_count = 0
        self.losses_correct_predictions_count = 0
        self.losses_incorrect_predictions_count = 0
        self.revenue = 0

    def get_wins_count(self) -> int:
        return self.wins_count

    def inc_wins_count(self) -> None:
        self.wins_count += 1

    def get_losses_count(self) -> int:
        return self.losses_count

    def inc_losses_count(self) -> None:
        self.losses_count += 1

    def get_reds_count(self) -> int:
        return self.reds_count

    def inc_reds_count(self) -> None:
        self.reds_count += 1

    def get_blacks_count(self) -> int:
        return self.blacks_count

    def inc_blacks_count(self) -> None:
        self.blacks_count += 1

    def get_zeros_count(self) -> int:
        return self.zeros_count

    def inc_zeros_count(self) -> None:
        self.zeros_count += 1

    def get_correct_predictions_count(self) -> int:
        return self.correct_predictions_count

    def inc_correct_predictions_count(self) -> None:
        self.correct_predictions_count += 1

    def get_incorrect_predictions_count(self) -> int:
        return self.incorrect_predictions_count

    def inc_incorrect_predictions_count(self) -> None:
        self.incorrect_predictions_count += 1

    def get_revenue(self) -> int:
        return self.revenue

    def add_revenue(self, revenue: int) -> None:
        self.revenue += revenue

    def get_iterations_count(self) -> int:
        return self.wins_count + self.losses_count

    def get_win_rate(self):
        rate = 0
        if self.get_iterations_count() > 0:
            rate = (self.wins_count / self.get_iterations_count()) * 100

        return rate

    def get_prediction_rate(self):
        rate = 0
        if self.get_iterations_count() > 0:
            rate = (self.correct_predictions_count / self.get_iterations_count()) * 100

        return rate

    def get_wins_correct_predictions_count(self) -> int:
        return self.wins_correct_predictions_count

    def inc_wins_correct_predictions_count(self) -> None:
        self.wins_correct_predictions_count += 1

    def get_wins_incorrect_predictions_count(self) -> int:
        return self.wins_incorrect_predictions_count

    def inc_wins_incorrect_predictions_count(self) -> None:
        self.wins_incorrect_predictions_count += 1

    def get_losses_correct_predictions_count(self) -> int:
        return self.losses_correct_predictions_count

    def inc_losses_correct_predictions_count(self) -> None:
        self.losses_correct_predictions_count += 1

    def get_losses_incorrect_predictions_count(self) -> int:
        return self.losses_incorrect_predictions_count

    def inc_losses_incorrect_predictions_count(self) -> None:
        self.losses_incorrect_predictions_count += 1

    def get_wins_prediction_rate(self):
        rate = 0
        total_predictions_count = self.wins_correct_predictions_count + self.wins_incorrect_predictions_count;
        if total_predictions_count > 0:
            rate = (self.wins_correct_predictions_count / total_predictions_count) * 100

        return rate

    def get_loss_prediction_rate(self):
        rate = 0
        total_predictions_count = self.losses_correct_predictions_count + self.losses_incorrect_predictions_count;
        if total_predictions_count > 0:
            rate = (self.losses_correct_predictions_count / total_predictions_count) * 100

        return rate