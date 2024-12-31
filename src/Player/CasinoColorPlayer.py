import os
from typing import List
from rich.console import Console
from rich.table import Table
from art import tprint

from Dto.Game.CasinoColorGameResult import CasinoColorGameResult
from Dto.Game.CasinoColorGameSession import CasinoColorGameSession
from Entity.CasinoHistoryRecord import CasinoHistoryRecord
from Game.CasinoColorGame import CasinoColorGame, COLOR_CODE_RED, COLOR_CODE_BLACK, COLOR_CODE_ZERO, COLOR_CODE_TITLE_MAP, GAME_RESULT_CODE_WIN, GAME_RESULT_CODE_LOSE, GAME_RESULT_CODE_TITLE_MAP
from Model.CasinoColorModel import CasinoColorModel
from Service.HistoryService import HistoryService
from Service.ModelService import ModelService

MIN_BID_AMOUNT = 5000
REGULAR_BID_AMOUNT = 10000
MAX_BID_AMOUNT = 80000
MIN_BID_RATE = 50
MIN_ITERATIONS_COUNT = 100
MAX_HISTORY_LENGTH = 1000000
PREDICTION_CONTEXT_LENGTH = 100
PREDICTION_TOP_CONTEXT_LENGTH = 20

TRAIN_MODE_RUNTIME = 1
TRAIN_MODE_HISTORY = 2

TRAIN_MODE = TRAIN_MODE_HISTORY

class CasinoColorPlayer:
    def __init__(
        self,
        history_service: HistoryService,
        model_service: ModelService,
        casino_color_game: CasinoColorGame
    ):
        self.history_service = history_service
        self.model_service = model_service
        self.casino_color_game = casino_color_game

    def play(self):
        casino_color_game_session = CasinoColorGameSession()

        model = CasinoColorModel()
        self.model_service.get_data(model)
        history_records = []
        train_history_records = []
        if not TRAIN_MODE == TRAIN_MODE_HISTORY:
            history_records = self.history_service.get_records(model)
        else: train_history_records = self.history_service.get_records(model)

        regular_bid_losses_streak_size = 0

        while True:
            bid_color = COLOR_CODE_RED
            bid_amount = MIN_BID_AMOUNT

            output = None
            prediction_probabilities = None
            predicted_game_result = None
            if len(history_records) > 0:
                output, prediction_probabilities = model.get_prediction(
                    self.get_model_context(history_records[-PREDICTION_CONTEXT_LENGTH:])
                )
                predicted_game_result = prediction_probabilities.argmax().item()
            if (
                    casino_color_game_session.get_prediction_rate() >= MIN_BID_RATE and
                    casino_color_game_session.get_iterations_count() >= MIN_ITERATIONS_COUNT and
                    predicted_game_result == GAME_RESULT_CODE_WIN and
                    (not TRAIN_MODE or TRAIN_MODE == TRAIN_MODE_HISTORY)
            ):
                bid_amount = REGULAR_BID_AMOUNT * (2 ** regular_bid_losses_streak_size)

            if bid_amount >= MAX_BID_AMOUNT:
                bid_amount = MAX_BID_AMOUNT

            if not TRAIN_MODE == TRAIN_MODE_HISTORY:
                casino_color_game_result = self.casino_color_game.play(bid_color, bid_amount)
            else:
                casino_color_game_result = CasinoColorGameResult(bid_color, bid_amount)

                if len(train_history_records) == 0: exit()

                train_history_record = train_history_records.pop(0)

                if train_history_record.get_is_win():
                    casino_color_game_result.mark_as_win()
                else: casino_color_game_result.mark_as_fail()

                casino_color_game_result.set_result_color(train_history_record.get_game_result_color())
                casino_color_game_result.set_result_color_streak_size(train_history_record.get_result_color_streak_size())

            if bid_amount >= REGULAR_BID_AMOUNT:
                if casino_color_game_result.get_is_win(): regular_bid_losses_streak_size = 0
                else: regular_bid_losses_streak_size += 1

                if bid_amount >= MAX_BID_AMOUNT:
                    regular_bid_losses_streak_size = 0

            if casino_color_game_result.get_is_win():
                casino_color_game_session.inc_wins_count()
                casino_color_game_session.add_revenue(bid_amount)
            else:
                casino_color_game_session.inc_losses_count()
                casino_color_game_session.add_revenue(-bid_amount)

            if casino_color_game_result.get_result_color() == COLOR_CODE_RED:
                casino_color_game_session.inc_reds_count()
            elif casino_color_game_result.get_result_color() == COLOR_CODE_BLACK:
                casino_color_game_session.inc_blacks_count()
            elif casino_color_game_result.get_result_color() == COLOR_CODE_ZERO:
                casino_color_game_session.inc_zeros_count()

            if casino_color_game_result.get_is_win() == predicted_game_result:
                casino_color_game_session.inc_correct_predictions_count()

                if predicted_game_result == GAME_RESULT_CODE_WIN:
                    casino_color_game_session.inc_wins_correct_predictions_count()
                else:
                    casino_color_game_session.inc_losses_correct_predictions_count()
            else:
                casino_color_game_session.inc_incorrect_predictions_count()

                if predicted_game_result == GAME_RESULT_CODE_WIN:
                    casino_color_game_session.inc_wins_incorrect_predictions_count()
                else:
                    casino_color_game_session.inc_losses_incorrect_predictions_count()

            top_results = history_records[-PREDICTION_TOP_CONTEXT_LENGTH:]
            top_reds_count = sum(1 for r in top_results if r.get_game_result_color() == COLOR_CODE_RED)
            top_blacks_count = sum(1 for r in top_results if r.get_game_result_color() == COLOR_CODE_BLACK)
            top_zeros_count = sum(1 for r in top_results if r.get_game_result_color() == COLOR_CODE_ZERO)

            history_record = CasinoHistoryRecord(
                casino_color_game_result.get_is_win(),
                casino_color_game_result.get_result_color(),
                casino_color_game_session.get_reds_count(),
                casino_color_game_session.get_blacks_count(),
                casino_color_game_session.get_zeros_count(),
                top_reds_count,
                top_blacks_count,
                top_zeros_count,
                casino_color_game_result.get_result_color_streak_size()
            )
            history_records.append(history_record)
            if len(history_records) > MAX_HISTORY_LENGTH:
                history_records.pop(0)

            if not TRAIN_MODE == TRAIN_MODE_HISTORY:
                self.history_service.save_records(model, history_records)

            loss = None
            weights = None
            if output is not None and len(history_records) > 0:
                base_weights = [0.45, 0.55]
                adjustment_factor = 0.40

                weights = base_weights.copy()
                wins_predictions = casino_color_game_session.get_wins_correct_predictions_count() + casino_color_game_session.get_wins_incorrect_predictions_count()
                loss_predictions = casino_color_game_session.get_losses_correct_predictions_count() + casino_color_game_session.get_losses_incorrect_predictions_count()
                if wins_predictions + loss_predictions > 0:
                    if wins_predictions > loss_predictions:
                        weights[GAME_RESULT_CODE_LOSE] += adjustment_factor
                        weights[GAME_RESULT_CODE_WIN] -= adjustment_factor
                    elif wins_predictions < loss_predictions:
                        weights[GAME_RESULT_CODE_LOSE] -= adjustment_factor
                        weights[GAME_RESULT_CODE_WIN] += adjustment_factor

                    total_weight = sum(weights)
                    weights = [w / total_weight for w in weights]

                loss = model.correct(output, casino_color_game_result.get_is_win(), weights)
                if not TRAIN_MODE == TRAIN_MODE_HISTORY:
                    self.model_service.save_data(model)

            if not TRAIN_MODE == TRAIN_MODE_HISTORY or len(train_history_records) == 0 or casino_color_game_session.get_iterations_count() % 100 == 0:
                self.print_game_result(
                    casino_color_game_session,
                    casino_color_game_result,
                    loss,
                    prediction_probabilities,
                    predicted_game_result,
                    top_reds_count,
                    top_blacks_count,
                    top_zeros_count,
                    weights
                )

    def get_model_context(self, history_records: List[CasinoHistoryRecord]):
        trend_reds, trend_blacks, trend_zeros = self.calculate_trend(history_records[-PREDICTION_TOP_CONTEXT_LENGTH:])
        P_0_0, P_0_1, P_0_2, P_1_0, P_1_1, P_1_2, P_2_0, P_2_1, P_2_2 = self.calculate_color_transition_probabilities(history_records[-PREDICTION_TOP_CONTEXT_LENGTH:])

        iterations_count = len(history_records)

        win_streak = 0
        fail_streak = 0

        if iterations_count > 0:
            for record in reversed(history_records):
                if record.get_is_win():
                    if fail_streak > 0:
                        break
                    win_streak += 1
                else:
                    if win_streak > 0:
                        break
                    fail_streak += 1

        context = [
            [
                r.get_is_win(),
                r.get_game_result_color(),
                r.get_result_color_streak_size(),
                win_streak,
                fail_streak,
                r.get_top_reds_count(),
                r.get_top_blacks_count(),
                r.get_top_zeros_count(),
                r.get_top_reds_count() / iterations_count,
                r.get_top_blacks_count() / iterations_count,
                r.get_top_zeros_count() / iterations_count,
                trend_reds,
                trend_blacks,
                trend_zeros,
                P_0_0,
                P_0_1,
                P_0_2,
                P_1_0,
                P_1_1,
                P_1_2,
                P_2_0,
                P_2_1,
                P_2_2,
                int(r.get_timestamp() * 1_000_000)
            ] for r in history_records
        ]

        return context

    def calculate_trend(self, history_records: List[CasinoHistoryRecord]):
        iterations_count = len(history_records)

        if iterations_count > 1:
            half_point = iterations_count // 2

            first_half = history_records[:half_point]
            second_half = history_records[half_point:]

            first_half_reds = sum(1 for r in first_half if r.get_game_result_color() == COLOR_CODE_RED)
            first_half_blacks = sum(1 for r in first_half if r.get_game_result_color() == COLOR_CODE_BLACK)
            first_half_zeros = sum(1 for r in first_half if r.get_game_result_color() == COLOR_CODE_ZERO)

            second_half_reds = sum(1 for r in second_half if r.get_game_result_color() == COLOR_CODE_RED)
            second_half_blacks = sum(1 for r in second_half if r.get_game_result_color() == COLOR_CODE_BLACK)
            second_half_zeros = sum(1 for r in second_half if r.get_game_result_color() == COLOR_CODE_ZERO)

            trend_reds = second_half_reds - first_half_reds
            trend_blacks = second_half_blacks - first_half_blacks
            trend_zeros = second_half_zeros - first_half_zeros
        else:
            trend_reds = trend_blacks = trend_zeros = 0

        return trend_reds, trend_blacks, trend_zeros

    def calculate_color_transition_probabilities(self, history_records: List[CasinoHistoryRecord]):
        transitions = [[0, 0, 0] for _ in range(3)]

        for i in range(len(history_records) - 1):
            current_color = history_records[i].get_game_result_color()
            next_color = history_records[i + 1].get_game_result_color()
            transitions[current_color][next_color] += 1

        normalized_transitions = [[0, 0, 0] for _ in range(3)]
        for i in range(3):
            total = sum(transitions[i])
            if total > 0:
                normalized_transitions[i] = [x / total for x in transitions[i]]

        return (
            normalized_transitions[0][0],  # P(0->0)
            normalized_transitions[0][1],  # P(0->1)
            normalized_transitions[0][2],  # P(0->2)
            normalized_transitions[1][0],  # P(1->0)
            normalized_transitions[1][1],  # P(1->1)
            normalized_transitions[1][2],  # P(1->2)
            normalized_transitions[2][0],  # P(2->0)
            normalized_transitions[2][1],  # P(2->1)
            normalized_transitions[2][2],  # P(2->2)
        )

        return [prob for row in transitions for prob in row]

    def clear_console(self):
        if os.name == 'nt':
            os.system('cls')
        else:
            os.system('clear')

    def print_game_result(
        self,
        casino_color_game_session,
        casino_color_game_result,
        loss,
        prediction_probabilities,
        predicted_game_result,
        top_reds_count,
        top_blacks_count,
        top_zeros_count,
        weights
    ):
        self.clear_console()
        tprint("L2 Bot", font="starwars")

        console = Console()
        table = Table(title="Game Session Results", show_header = True, header_style = "bold magenta")

        table.add_column("Metric", style="bold cyan", justify="right")
        table.add_column("Value", style="bold yellow", justify="left")

        table.add_row("Iteration (i)", str(casino_color_game_session.get_iterations_count()))
        table.add_row(
            "Total correct predictions / Total incorrect predictions",
            f"{casino_color_game_session.get_correct_predictions_count()} / {casino_color_game_session.get_incorrect_predictions_count()}",
        )
        table.add_row(
            "Total win rate / Total prediction rate",
            f"{casino_color_game_session.get_win_rate()} / {casino_color_game_session.get_prediction_rate()}",
        )
        table.add_row(
            "Wins prediction rate / Loss prediction rate",
            f"{casino_color_game_session.get_wins_prediction_rate()} / {casino_color_game_session.get_loss_prediction_rate()}",
        )
        table.add_row(
            "Wins correct predictions / Wins incorrect predictions",
            f"{casino_color_game_session.get_wins_correct_predictions_count()} / {casino_color_game_session.get_wins_incorrect_predictions_count()}",
        )
        table.add_row(
            "Loss correct predictions / Loss incorrect predictions",
            f"{casino_color_game_session.get_losses_correct_predictions_count()} / {casino_color_game_session.get_losses_incorrect_predictions_count()}",
        )
        table.add_row("Loss", f"{loss}")
        table.add_row("Prediction probabilities", f"{prediction_probabilities}")
        table.add_row("Weights", f"{weights}")
        table.add_row(
            "Wins / Losses",
            f"{casino_color_game_session.get_wins_count()} / {casino_color_game_session.get_losses_count()}",
        )
        table.add_row(
            "Reds / Blacks / Zeros",
            f"{casino_color_game_session.get_reds_count()} / {casino_color_game_session.get_blacks_count()} / {casino_color_game_session.get_zeros_count()}",
        )
        table.add_row(
            "[TOP] Reds / Blacks / Zeros",
            f"{top_reds_count} / {top_blacks_count} / {top_zeros_count}",
        )
        table.add_row("Game result / Predicted game result", f"{GAME_RESULT_CODE_TITLE_MAP[casino_color_game_result.get_is_win()]} / {GAME_RESULT_CODE_TITLE_MAP.get(predicted_game_result, 'None')}")
        table.add_row("Result color streak size", f"{casino_color_game_result.get_result_color_streak_size()}")
        table.add_row("Revenue", f"{casino_color_game_session.get_revenue()}")

        console.print(table)
