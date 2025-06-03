import logging
import time

from py3dbp import Bin, BinType, Item, Packer, log

from .utils import PrintPackingResult


def example6() -> None:
    """
    Check stability on item - second rule
    1. If the ratio below the support surface does not exceed this ratio, then check the second rule.
    2. If there is no support under any of the bottom four vertices of the item, then remove the item.
    """
    packer = Packer()
    box = Bin(
        partno="example6",
        WHD=(5, 4, 7),
        max_weight=100,
        corner=0,
        bin_type=BinType.openTop,
    )
    packer.addBin(box)
    packer.addItem(Item(partno="Box-1", name="test", typeof="cube", WHD=(5, 4, 1), weight=1, level=1, loadbear=100, updown=True, color="yellow"))
    packer.addItem(Item(partno="Box-2", name="test", typeof="cube", WHD=(1, 1, 4), weight=1, level=2, loadbear=100, updown=True, color="olive"))
    packer.addItem(Item(partno="Box-3", name="test", typeof="cube", WHD=(3, 4, 2), weight=1, level=3, loadbear=100, updown=True, color="pink"))
    packer.addItem(Item(partno="Box-4", name="test", typeof="cube", WHD=(1, 1, 4), weight=1, level=4, loadbear=100, updown=True, color="olive"))
    packer.addItem(Item(partno="Box-5", name="test", typeof="cube", WHD=(1, 2, 1), weight=1, level=5, loadbear=100, updown=True, color="pink"))
    packer.addItem(Item(partno="Box-6", name="test", typeof="cube", WHD=(1, 2, 1), weight=1, level=6, loadbear=100, updown=True, color="pink"))
    packer.addItem(Item(partno="Box-7", name="test", typeof="cube", WHD=(1, 1, 4), weight=1, level=7, loadbear=100, updown=True, color="olive"))
    packer.addItem(Item(partno="Box-8", name="test", typeof="cube", WHD=(1, 1, 4), weight=1, level=8, loadbear=100, updown=True, color="olive"))  # Try switching WHD=(1, 1, 3) and (1, 1, 4) to compare the results
    packer.addItem(Item(partno="Box-9", name="test", typeof="cube", WHD=(5, 4, 2), weight=1, level=9, loadbear=100, updown=True, color="brown"))

    start = time.time()
    packer.pack(bigger_first=True, distribute_items=False, fix_point=True, check_stable=True, support_surface_ratio=0.75)
    stop = time.time()
    PrintPackingResult(packer)
    log.info(f"used time: {stop - start}")


if __name__ == "__main__":
    log.setLevel(logging.DEBUG)
    example6()
