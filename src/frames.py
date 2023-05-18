# Frames Class


class Frames:
    def __init__(self, percentage_threshold: int) -> None:
        """
        Initializes the Frames object.

        Args:
        - percentage_threshold (int): The threshold percentage for the notok frames.

        Attributes:
        - ok (int): Count of "ok" frames.
        - notok (int): Count of "notok" frames.
        - percentage_threshold (int): The threshold percentage for the notok frames.
        """
        self.ok: int = 0
        self.notok: int = 0
        self.percentage_threshold = percentage_threshold

    def add_ok(self) -> None:
        """
        Increments the count of "ok" frames and resets the counts if "ok" count exceeds "notok" count.
        """
        self.ok += 1
        if self.ok > self.notok:
            self.reset()

    def add_notok(self) -> None:
        """
        Increments the count of "notok" frames.
        """
        self.notok += 1

    def reset(self) -> None:
        """
        Resets the counts of "ok" and "notok" frames.
        """
        self.ok = 0
        self.notok = 0

    def crossed_threshold(self) -> bool:
        """
        Checks if the percentage of "notok" frames crossed the threshold.

        Returns:
        - crossed_threshold (bool): True if the threshold is crossed, False otherwise.
        """
        if self.ok + self.notok == 0:
            return False
        if (self.notok / (self.ok + self.notok)) * 100 > self.percentage_threshold:
            return True
        return False
