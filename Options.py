from dataclasses import dataclass
from Options import Choice, PerGameCommonOptions

class Difficulty(Choice):
    """Difficulty. Default Easy.
    Easy: Easy Settings
    Normal: Normal Settings
    Hard: Hard Settings
    """
    display_name = "Difficulty"
    option_easy = 0
    option_normal = 1
    option_hard = 2

@dataclass
class ArcardelagoOptions(PerGameCommonOptions):
    difficulty : Difficulty