# Frames Class


class Frames:
    def __init__(self, percentage_threshold: int) -> None:
        self.ok: int = 0
        self.notok: int = 0
        self.percentage_threshold = percentage_threshold

    def add_ok(self) -> None:
        self.ok += 1
        if self.ok > self.notok:
            self.reset()

    def add_notok(self) -> None:
        self.notok += 1

    def reset(self) -> None:
        self.ok = 0
        self.notok = 0

    def crossed_threshold(self) -> bool:
        if self.ok + self.notok == 0:
            return False
        if (self.notok / (self.ok + self.notok)) * 100 > self.percentage_threshold:
            return True
        return False
