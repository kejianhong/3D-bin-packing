import logging
import time

from py3dbp import Bin, BinType, Item, Packer, log

from .utils import PrintPackingResult


def example2() -> None:
    """
    This case is used to demonstrate an example of a packing complex situation.
    """

    packer = Packer()
    box = Bin("example2", (30, 10, 15), 99, 0, bin_type=BinType.openTop)
    packer.addBin(box)
    packer.addItem(Item("test1", "test", "cube", (9, 8, 7), 1, 1, 100, True, "red"))
    packer.addItem(Item("test2", "test", "cube", (4, 25, 1), 1, 1, 100, True, "blue"))
    packer.addItem(Item("test3", "test", "cube", (2, 13, 5), 1, 1, 100, True, "gray"))
    packer.addItem(Item("test4", "test", "cube", (7, 5, 4), 1, 1, 100, True, "orange"))
    packer.addItem(Item("test5", "test", "cube", (10, 5, 2), 1, 1, 100, True, "lawngreen"))
    packer.addItem(Item("test6", "test", "cube", (6, 5, 2), 1, 1, 100, True, "purple"))
    packer.addItem(Item("test7", "test", "cube", (5, 2, 9), 1, 1, 100, True, "yellow"))
    packer.addItem(Item("test8", "test", "cube", (10, 8, 5), 1, 1, 100, True, "pink"))
    packer.addItem(Item("test9", "test", "cube", (1, 3, 5), 1, 1, 100, True, "brown"))
    packer.addItem(Item("test10", "test", "cube", (8, 4, 7), 1, 1, 100, True, "cyan"))
    packer.addItem(Item("test11", "test", "cube", (2, 5, 3), 1, 1, 100, True, "olive"))
    packer.addItem(Item("test12", "test", "cube", (1, 9, 2), 1, 1, 100, True, "darkgreen"))
    packer.addItem(Item("test13", "test", "cube", (7, 5, 4), 1, 1, 100, True, "orange"))
    packer.addItem(Item("test14", "test", "cube", (10, 2, 1), 1, 1, 100, True, "lawngreen"))
    packer.addItem(Item("test15", "test", "cube", (3, 2, 4), 1, 1, 100, True, "purple"))
    packer.addItem(Item("test16", "test", "cube", (5, 7, 8), 1, 1, 100, True, "yellow"))
    packer.addItem(Item("test17", "test", "cube", (4, 8, 3), 1, 1, 100, True, "white"))
    packer.addItem(Item("test18", "test", "cube", (2, 11, 5), 1, 1, 100, True, "brown"))
    packer.addItem(Item("test19", "test", "cube", (8, 3, 5), 1, 1, 100, True, "cyan"))
    packer.addItem(Item("test20", "test", "cube", (7, 4, 5), 1, 1, 100, True, "olive"))
    packer.addItem(Item("test21", "test", "cube", (2, 4, 11), 1, 1, 100, True, "darkgreen"))
    packer.addItem(Item("test22", "test", "cube", (1, 3, 4), 1, 1, 100, True, "orange"))
    packer.addItem(Item("test23", "test", "cube", (10, 5, 2), 1, 1, 100, True, "lawngreen"))
    packer.addItem(Item("test24", "test", "cube", (7, 4, 5), 1, 1, 100, True, "purple"))
    packer.addItem(Item("test25", "test", "cube", (2, 10, 3), 1, 1, 100, True, "yellow"))
    packer.addItem(Item("test26", "test", "cube", (3, 8, 1), 1, 1, 100, True, "pink"))
    packer.addItem(Item("test27", "test", "cube", (7, 2, 5), 1, 1, 100, True, "brown"))
    packer.addItem(Item("test28", "test", "cube", (8, 9, 5), 1, 1, 100, True, "cyan"))
    packer.addItem(Item("test29", "test", "cube", (4, 5, 10), 1, 1, 100, True, "olive"))
    packer.addItem(Item("test30", "test", "cube", (10, 10, 2), 1, 1, 100, True, "darkgreen"))

    start = time.time()
    packer.pack(
        bigger_first=True,
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
    example2()
