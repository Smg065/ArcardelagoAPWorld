from typing import NamedTuple

BASE_ID = 6500000

class ItemData(NamedTuple):
	acid: int|None = None
	qty: int = 0
	type: str = ""
	default_location: str = ""

spheres_table = {
	"Red Sphere"       :    ItemData(BASE_ID + 1, 1, "Sphere", ""),
	"Green Sphere"     :    ItemData(BASE_ID + 2, 1, "Sphere", ""),
	"Violet Sphere"      :    ItemData(BASE_ID + 3, 1, "Sphere", ""),
	"Orange Sphere"    :    ItemData(BASE_ID + 4, 1, "Sphere", ""),
	"Blue Sphere"      :    ItemData(BASE_ID + 5, 1, "Sphere", ""),
	"Yellow Sphere"    :    ItemData(BASE_ID + 6, 1, "Sphere", "")
}

filler_table = {
	"Filler"           :    ItemData(BASE_ID + 90000, -1, "Filler", "")
}

all_items_table = {
	**spheres_table,
	**filler_table
}