import pytest

from exercises.pythonic_python.the_gilded_rose.gilded_rose import (
    Item,
    update_quality,
)


def updated_item(sell_in, quality, name="normal item"):
    item = Item(name=name, sell_in=sell_in, quality=quality)
    result = update_quality([item])
    assert result[0] is item
    return item


@pytest.mark.parametrize(
    ("sell_in", "quality", "expected_quality"),
    [(5, 10, 9), (0, 10, 8), (-10, 10, 8), (5, 0, 0), (5, 1, 0), (5, 50, 49)],
)
def test_normal_item_quality_changes(sell_in, quality, expected_quality):
    item = updated_item(sell_in, quality, "normal")

    assert item.quality == expected_quality
    assert item.sell_in == sell_in - 1


@pytest.mark.parametrize(
    ("sell_in", "quality", "expected_quality"),
    [(5, 10, 11), (0, 10, 12), (-10, 10, 12), (5, 49, 50), (5, 50, 50)],
)
def test_aged_brie_quality_increases_with_a_maximum_of_50(
    sell_in, quality, expected_quality
):
    item = updated_item(sell_in, quality, "Aged Brie")

    assert item.quality == expected_quality
    assert item.sell_in == sell_in - 1


@pytest.mark.parametrize("sell_in", [5, 0, -10])
def test_sulfuras_is_unchanged(sell_in):
    item = updated_item(sell_in, 80, "Sulfuras, Hand of Ragnaros")

    assert item.sell_in == sell_in
    assert item.quality == 80


@pytest.mark.parametrize(
    ("sell_in", "quality", "expected_quality"),
    [
        (11, 10, 11),
        (10, 10, 12),
        (6, 10, 12),
        (5, 10, 13),
        (1, 10, 13),
        (0, 10, 0),
        (-10, 10, 0),
        (10, 50, 50),
        (5, 50, 50),
    ],
)
def test_backstage_passes_increase_then_drop_after_the_concert(
    sell_in, quality, expected_quality
):
    item = updated_item(sell_in, quality, "Backstage passes to a TAFKAL80ETC concert")

    assert item.quality == expected_quality
    assert item.sell_in == sell_in - 1


@pytest.mark.parametrize(
    ("sell_in", "quality", "expected_quality"),
    [(5, 10, 8), (0, 10, 6), (-10, 10, 6), (5, 0, 0), (0, 0, 0), (-10, 0, 0)],
)
def test_conjured_items_degrade_twice_as_fast(sell_in, quality, expected_quality):
    item = updated_item(sell_in, quality, "Conjured Mana Cake")

    assert item.quality == expected_quality
    assert item.sell_in == sell_in - 1


def test_update_quality_handles_multiple_items():
    items = [Item("normal item", 5, 10), Item("Aged Brie", 3, 10)]

    assert update_quality(items) is items
    assert [(item.sell_in, item.quality) for item in items] == [(4, 9), (2, 11)]
