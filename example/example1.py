import logging
import time

from py3dbp import Bin, BinType, Item, Packer, Painter, log

from .utils import PrintPackingResult


def example1() -> None:
    """
    This example is used to demonstrate the mixed packing of cube and cylinder.
    """
    packer = Packer()
    box = Bin(
        partno="example1",
        WHD=(5.6875, 10.75, 15.0),
        max_weight=70.0,
        corner=0,
        bin_type=BinType.openSide,
    )
    packer.addBin(box)
    packer.addItem(Item("50g [powder 1]", "test", "cube", (2, 2, 4), 1, 1, 100, True, "red"))
    packer.addItem(Item("50g [powder 2]", "test", "cube", (2, 2, 4), 2, 1, 100, True, "blue"))
    packer.addItem(Item("50g [powder 3]", "test", "cube", (2, 2, 4), 3, 1, 100, True, "gray"))
    packer.addItem(Item("50g [powder 4]", "test", "cube", (2, 2, 4), 3, 1, 100, True, "orange"))
    packer.addItem(Item("50g [powder 5]", "test", "cylinder", (2, 2, 4), 3, 1, 100, True, "lawngreen"))
    packer.addItem(Item("50g [powder 6]", "test", "cylinder", (2, 2, 4), 3, 1, 100, True, "purple"))
    packer.addItem(Item("50g [powder 7]", "test", "cylinder", (1, 1, 5), 3, 1, 100, True, "yellow"))
    packer.addItem(Item("250g [powder 8]", "test", "cylinder", (4, 4, 2), 4, 1, 100, True, "pink"))
    packer.addItem(Item("250g [powder 9]", "test", "cylinder", (4, 4, 2), 5, 1, 100, True, "brown"))
    packer.addItem(Item("250g [powder 10]", "test", "cube", (4, 4, 2), 6, 1, 100, True, "cyan"))
    packer.addItem(Item("250g [powder 11]", "test", "cylinder", (4, 4, 2), 7, 1, 100, True, "olive"))
    packer.addItem(Item("250g [powder 12]", "test", "cylinder", (4, 4, 2), 8, 1, 100, True, "darkgreen"))
    packer.addItem(Item("250g [powder 13]", "test", "cube", (4, 4, 2), 9, 1, 100, True, "orange"))

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
    example1()
