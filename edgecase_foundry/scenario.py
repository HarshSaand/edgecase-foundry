from dataclasses import dataclass


@dataclass(frozen=True)
class Scenario:
    small_count: int
    small_max_amount: float
    final_min_amount: float
    window_minutes: int
    final_channel: str
    require_new_city: bool

    def validate(self) -> None:
        if not 1 <= self.small_count <= 20:
            raise ValueError("small_count must be between 1 and 20")
        if self.small_max_amount <= 0:
            raise ValueError("small_max_amount must be positive")
        if self.final_min_amount <= self.small_max_amount:
            raise ValueError("final amount must exceed the small-purchase limit")
        if not 1 <= self.window_minutes <= 1440:
            raise ValueError("window_minutes must be between 1 and 1440")
        if self.final_channel not in {"online", "chip", "contactless"}:
            raise ValueError("unsupported final channel")
