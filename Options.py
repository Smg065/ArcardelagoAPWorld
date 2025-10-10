from dataclasses import dataclass
from Options import Choice, PerGameCommonOptions, Range, OptionCounter

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

class AdjacencyOdds(Range):
    """The chances that the map will need to warp to the next location. Default 3.
    """
    range_start = 1
    range_end = 10
    default = 3

class BranchingOdds(Range):
    """The chances that the map will branch out. Default 5.
    """
    range_start = 1
    range_end = 10
    default = 5

class CardsPerRegion(Range):
    """The number of cards that each region has. Default 20.
    """
    range_start = 5
    range_end = 100
    default = 20

class MapRadius(Range):
    """The radius of the map generated. Default 25.
    """
    range_start = 20
    range_end = 100
    default = 25

class TilesPerPip(Range):
    """How many map tiles need to spawn for 1 map pip to spawn. Default 25.
    9 = 1 Tile Radius of buffer space
    25 = 2 Tile Radius of buffer space
    49 = 3 Tile Radius of buffer space
    81 = 4 Tile Radius of buffer space
    """
    range_start = 9
    range_end = 100

    one_radius = 9
    two_radius = 25
    three_radius = 49
    four_radius = 81
    
    default = 25

class NodePercentages(OptionCounter):
    """The percentage of various map nodes. Must add up to 100.
    Home will add an extra node to the location you spawn at.
    There will always be 1 boss.
    Warps only acount for non-vital warp points.
    Obstacles are not implimented yet.

    Auto:           A point you travel along instantly. Add path texture.   Default 05%
    Intersection:   A free point. Usually used for intersections.           Default 15%
    Shop:           A location to turn money into cards and items.          Default 05%
    Treasure:       An instant reward is at this location.                  Default 05%
    Release Altar:  Release cards to pass this locaiton.                    Default 05%
    Warp:           Internal/shortcut warp. 2 nodes for the price of 1.     Default 05%
    Event:          A choice or minigame that can boost or hinder you.      Default 10%
    Enemy:          Enemy cards which must be defeated to pass.             Default 40%
    """
    min = 0
    max = 100
    default = {
        "Auto" : 5,
        "Intersection" : 15,
        "Shop" : 5,
        "Treasure" : 5,
        "Releaser" : 5,
        "Warp" : 5,
        "Event" : 10,
        "Enemy" : 40
    }

@dataclass
class ArcardelagoOptions(PerGameCommonOptions):
    difficulty : Difficulty
    adjacency_odds : AdjacencyOdds
    branching_odds : BranchingOdds
    cards_per_region : CardsPerRegion
    map_radius : MapRadius
    tiles_per_pip : TilesPerPip
    node_percentages : NodePercentages
