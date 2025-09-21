from typing import Any, Dict
import logging

from BaseClasses import Item, Location, Region, Tutorial, ItemClassification
from worlds.generic.Rules import set_rule
from .ItemPool import spheres_table, all_items_table
from .Options import ArcardelagoOptions

from ..AutoWorld import World, WebWorld
from NetUtils import SlotType

class ArcardelagoItem(Item):
    game: str = "Arcardelago"

class ArcardelagoLocation(Location):
    Arcardelago : str = "Arcardelago"

class ArcardelagoWeb(WebWorld):
    englishTut = Tutorial("",
                     """A guide for setting up Arcardelago on your computer.""",
                     "English",
                     "setup_en.md",
                     "setup/en",
                     ["Smg065"])
    tutorials = [englishTut]

class ArcardelagoWorld(World):
    """
    Arcardelago is a game that uses items at it's locations as in-game items.
    """
    game : str = "Arcardelago"
    version : str = "V0.1"
    web = ArcardelagoWeb()
    topology_present = True
    options_dataclass = ArcardelagoOptions
    options : ArcardelagoOptions
    card_colors : list[str] = ["Red", "Green", "Violet", "Orange", "Blue", "Yellow"]
    #Items
    item_name_to_id = {}
    for each_key, each_item in all_items_table.items():
        item_name_to_id[each_key] = each_item.acid
    #Locations (Cards)
    location_name_to_id = {}
    cards_per_color : int = 20
    for each_card in range(1, cards_per_color + 1):
        for each_color in card_colors:
            id : int = (card_colors.index(each_color) * cards_per_color) + each_card
            location_name_to_id[each_color + " Card " + str(each_card)] = id

    #def generate_early(self):
    #    self.multiworld.player_types[self.player] = SlotType.spectator

    def generate_early(self):
        player = self.player
        multiworld = self.multiworld

        #Basic setup
        menu_region : Region = Region("Menu", player, multiworld)
        multiworld.regions.append(menu_region)
        self.spawning_sphere = self.random.choice(list(spheres_table.keys()))
        progusefulItem = self.create_item(self.spawning_sphere)
        multiworld.push_precollected(progusefulItem)

        #Victory Condition
        all_bosses : ArcardelagoLocation = ArcardelagoLocation(player, "All Bosses", None, menu_region)
        all_bosses.place_locked_item(self.create_event("Victory"))
        menu_region.locations.append(all_bosses)
        multiworld.completion_condition[player] = lambda state: state.has("Victory", player)
        set_rule(all_bosses, lambda state: state.has_all(list(spheres_table.keys()), player))

        #Colored Spheres
        color_to_region : Dict[str, Region] = {}
        for color_name in self.card_colors:
            each_sphere_region : Region = Region(color_name + " Region", player, multiworld)
            color_to_region[color_name] = each_sphere_region
            menu_region.connect(each_sphere_region, "Got " + color_name + " Sphere", lambda state, sphere_color = color_name: state.has(sphere_color + " Sphere", player))
            multiworld.regions.append(each_sphere_region)
        
        #Create the Cards
        for location_name, location_id in self.location_name_to_id.items():
            origin_region : Region = color_to_region[location_name.split(" ")[0]]
            each_card : ArcardelagoLocation = ArcardelagoLocation(player, location_name, location_id, origin_region)
            origin_region.locations.append(each_card)
            
        return super().generate_early()

    def create_item(self, name: str) -> Item:
        item_data = all_items_table[name]
        item_classification = None
        item_id = item_data.acid
        match item_data.type:
            #Spheres are Proguseful
            case "Sphere":
                item_classification = ItemClassification.progression | ItemClassification.useful
                #ItemClassification.useful
            case "Filler":
                item_classification = ItemClassification.filler
        item_output = ArcardelagoItem(name, item_classification, item_id, self.player)
        return item_output

    def create_event(self, name: str):
        return ArcardelagoItem(name, ItemClassification.progression, None, self.player)

    def create_items(self) -> None:
        spawn_items : list = []
        spawn_items.extend(list(spheres_table.keys()))
        spawn_items.remove(self.spawning_sphere)
        core_item_count : int = 0
        #Core Items
        for each_item in spawn_items:
            for _ in range(all_items_table[each_item].qty):
                self.multiworld.itempool.append(self.create_item(each_item))
                core_item_count += 1
        for _ in range(120 - core_item_count):
            self.multiworld.itempool.append(self.create_item("Filler"))

    def locations_of_slots_items(self) -> list[list[int]]:
        myItems : list[Item] = self.get_items_from(self.player)
        output : list[list[int | str]] = []
        for each_item in myItems:
            output.append([each_item.location.player, each_item.location.name, each_item.flags])
        return output

    def get_items_from(self, target_player) -> list[Item]:
        return list(filter(lambda a: a.player == target_player, self.multiworld.itempool))

    def fill_slot_data(self) -> Dict[str, Any]:
        options = {}
        options["difficulty"] = self.options.difficulty.value
        enemies = self.locations_of_slots_items()
        options["enemies"] = enemies
        options["player_name"] = self.multiworld.player_name[self.player]
        options["seed"] = self.random.randint(-6500000, 6500000)
        options["version"] = self.version
        return options