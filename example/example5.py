import logging
import time

from py3dbp import Bin, BinType, Item, Packer, log

from .utils import PrintPackingResult


def example5() -> None:
    packer = Packer()
    box = Bin(
        partno="example5",
        WHD=(5, 4, 3),
        max_weight=100,
        corner=0,
        bin_type=BinType.openSide,
    )
    packer.addBin(box)
    packer.addItem(Item(partno="Box-3", name="test", typeof="cube", WHD=(2, 5, 2), weight=1, level=1, loadbear=100, updown=True, color="pink"))
    packer.addItem(Item(partno="Box-3", name="test", typeof="cube", WHD=(2, 3, 2), weight=1, level=2, loadbear=100, updown=True, color="pink"))  # Try switching WHD=(2, 2, 2) and (2, 3, 2) to compare the results
    packer.addItem(Item(partno="Box-4", name="test", typeof="cube", WHD=(5, 4, 1), weight=1, level=3, loadbear=100, updown=True, color="brown"))

    start = time.time()
    packer.pack(bigger_first=True, distribute_items=False, fix_point=True, check_stable=True, support_surface_ratio=0.75)
    stop = time.time()
    PrintPackingResult(packer)
    log.info(f"used time: {stop - start}")


if __name__ == "__main__":
    log.setLevel(logging.DEBUG)
    example5()
