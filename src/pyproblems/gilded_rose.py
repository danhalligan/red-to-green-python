"""Gilded Rose inventory exercise."""

from dataclasses import dataclass


@dataclass
class Item:
    """An inventory item with a sell-by date and quality score."""

    name: str
    sell_in: int
    quality: int


def update_quality(items: list[Item]) -> list[Item]:
    """Update each item's sell-in and quality values for one day."""
    for item in items:
        if (
            item.name != "Aged Brie"
            and item.name != "Backstage passes to a TAFKAL80ETC concert"
        ):
            if item.quality > 0:
                if item.name != "Sulfuras, Hand of Ragnaros":
                    item.quality -= 1
        else:
            if item.quality < 50:
                item.quality += 1
                if item.name == "Backstage passes to a TAFKAL80ETC concert":
                    if item.sell_in < 11 and item.quality < 50:
                        item.quality += 1
                    if item.sell_in < 6 and item.quality < 50:
                        item.quality += 1

        if item.name != "Sulfuras, Hand of Ragnaros":
            item.sell_in -= 1

        if item.sell_in < 0:
            if item.name != "Aged Brie":
                if item.name != "Backstage passes to a TAFKAL80ETC concert":
                    if item.quality > 0:
                        if item.name != "Sulfuras, Hand of Ragnaros":
                            item.quality -= 1
                else:
                    item.quality -= item.quality
            elif item.quality < 50:
                item.quality += 1

    return items
