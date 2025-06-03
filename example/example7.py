import logging
import time

from py3dbp import Bin, BinType, Item, Packer, log

from .utils import PrintPackingResult


def example7() -> None:
    """
    If you have multiple boxes, you can change distribute_items to achieve different packaging purposes.
    1. distribute_items=True , put the items into the box in order, if the box is full, the remaining items will continue to be loaded into the next box until all the boxes are full  or all the items are packed.
    2. distribute_items=False, compare the packaging of all boxes, that is to say, each box packs all items, not the remaining items.
    """

    packer = Packer()
    box = Bin("example7-Bin1", (5, 5, 5), 100, 0, bin_type=BinType.openSide)
    box2 = Bin("example7-Bin2", (3, 3, 5), 100, 0, bin_type=BinType.openSide)
    packer.addBin(box)
    packer.addBin(box2)

    packer.addItem(Item(partno="Box-1", name="test1", typeof="cube", WHD=(5, 4, 1), weight=1, level=1, loadbear=100, updown=True, color="yellow"))
    packer.addItem(Item(partno="Box-2", name="test2", typeof="cube", WHD=(1, 2, 4), weight=1, level=1, loadbear=100, updown=True, color="olive"))
    packer.addItem(Item(partno="Box-3", name="test3", typeof="cube", WHD=(1, 2, 3), weight=1, level=1, loadbear=100, updown=True, color="olive"))
    packer.addItem(Item(partno="Box-4", name="test4", typeof="cube", WHD=(1, 2, 2), weight=1, level=1, loadbear=100, updown=True, color="olive"))
    packer.addItem(Item(partno="Box-5", name="test5", typeof="cube", WHD=(1, 2, 3), weight=1, level=1, loadbear=100, updown=True, color="olive"))
    packer.addItem(Item(partno="Box-6", name="test6", typeof="cube", WHD=(1, 2, 4), weight=1, level=1, loadbear=100, updown=True, color="olive"))
    packer.addItem(Item(partno="Box-7", name="test7", typeof="cube", WHD=(1, 2, 2), weight=1, level=1, loadbear=100, updown=True, color="olive"))
    packer.addItem(Item(partno="Box-8", name="test8", typeof="cube", WHD=(1, 2, 3), weight=1, level=1, loadbear=100, updown=True, color="olive"))
    packer.addItem(Item(partno="Box-9", name="test9", typeof="cube", WHD=(1, 2, 4), weight=1, level=1, loadbear=100, updown=True, color="olive"))
    packer.addItem(Item(partno="Box-10", name="test10", typeof="cube", WHD=(1, 2, 3), weight=1, level=1, loadbear=100, updown=True, color="olive"))
    packer.addItem(Item(partno="Box-11", name="test11", typeof="cube", WHD=(1, 2, 2), weight=1, level=1, loadbear=100, updown=True, color="olive"))
    packer.addItem(Item(partno="Box-12", name="test12", typeof="cube", WHD=(5, 4, 1), weight=1, level=1, loadbear=100, updown=True, color="pink"))
    packer.addItem(Item(partno="Box-13", name="test13", typeof="cube", WHD=(1, 1, 4), weight=1, level=1, loadbear=100, updown=True, color="olive"))
    packer.addItem(Item(partno="Box-14", name="test14", typeof="cube", WHD=(1, 2, 1), weight=1, level=1, loadbear=100, updown=True, color="pink"))
    packer.addItem(Item(partno="Box-15", name="test15", typeof="cube", WHD=(1, 2, 1), weight=1, level=1, loadbear=100, updown=True, color="pink"))
    packer.addItem(Item(partno="Box-16", name="test16", typeof="cube", WHD=(1, 1, 4), weight=1, level=1, loadbear=100, updown=True, color="olive"))
    packer.addItem(Item(partno="Box-17", name="test17", typeof="cube", WHD=(1, 1, 4), weight=1, level=1, loadbear=100, updown=True, color="olive"))
    packer.addItem(Item(partno="Box-18", name="test18", typeof="cube", WHD=(5, 4, 2), weight=1, level=1, loadbear=100, updown=True, color="brown"))

    start = time.time()
    packer.pack(
        bigger_first=True,
        # Change distribute_items=False to compare the packing situation in multiple boxes of different capacities.
        distribute_items=False,
        fix_point=True,
        check_stable=True,
        support_surface_ratio=0.75,
    )
    stop = time.time()
    PrintPackingResult(packer)
    log.info(f"used time: {stop - start}")


if __name__ == "__main__":
    log.setLevel(logging.DEBUG)
    example7()
