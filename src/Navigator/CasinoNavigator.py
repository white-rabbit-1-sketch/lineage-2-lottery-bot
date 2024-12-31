from Service.NavigatorService import NavigatorService

RETRY_IMG_PATH = "/img/casino/retry.jpg"
BACK_IMG_PATH = "/img/casino/back.jpg"
ENTRY_IMG_PATH = "/img/casino/entry.jpg"
RED_IMG_PATH = "/img/casino/red.jpg"
BLACK_IMG_PATH = "/img/casino/black.jpg"
ZERO_IMG_PATH = "/img/casino/zero.jpg"
SUCCESS_IMG_PATH = "/img/casino/success.jpg"
LOSS_IMG_PATH = "/img/casino/fail.jpg"

class CasinoNavigator:
    def __init__(self, navigator_service: NavigatorService, window_title: str):
        self.navigator_service = navigator_service
        self.window_title = window_title

    def activate(self):
        self.navigator_service.activate_window(self.window_title)

    def is_retry_available(self) -> bool:
        return self.navigator_service.find_image(RETRY_IMG_PATH)

    def retry(self, throw_on_error: bool = True) -> None:
        self.navigator_service.click_image(RETRY_IMG_PATH, 50, 15, throw_on_error)

    def back(self, throw_on_error: bool = True) -> None:
        self.navigator_service.click_image(BACK_IMG_PATH, 15, 15, throw_on_error)

    def set_bid(self, bid_amount: int, throw_on_error: bool = True) -> None:
        self.navigator_service.click_image(ENTRY_IMG_PATH, 50, 50, throw_on_error)
        self.navigator_service.input(str(bid_amount))

    def chose_red(self, throw_on_error: bool = True) -> None:
        self.navigator_service.click_image(ENTRY_IMG_PATH, 150, 50, throw_on_error)

    def chose_black(self, throw_on_error: bool = True) -> None:
        self.navigator_service.click_image(ENTRY_IMG_PATH, 200, 50, throw_on_error)

    def is_red_result(self) -> bool:
        return self.navigator_service.find_image(RED_IMG_PATH)

    def is_black_result(self) -> bool:
        return self.navigator_service.find_image(BLACK_IMG_PATH)

    def is_zero_result(self) -> bool:
        return self.navigator_service.find_image(ZERO_IMG_PATH)

    def is_success_result(self) -> bool:
        return self.navigator_service.find_image(SUCCESS_IMG_PATH)

    def is_loss_result(self) -> bool:
        return self.navigator_service.find_image(LOSS_IMG_PATH)