import logging
import time

from py3dbp import Bin, BinType, Item, Packer, log

from .utils import PrintPackingResult


def example3() -> None:
    """
    This example is used to demonstrate that the algorithm does not optimize.
    """
    packer = Packer()
    box = Bin("example3", (6, 1, 5), 100, 0, bin_type=BinType.openSide)
    packer.addBin(box)
    # If all item WHD=(2, 1, 3) , item can be fully packed into box, but if choose one item and modify WHD=(3, 1, 2) , item can't be fully packed into box.
    packer.addItem(Item(partno="Box-1", name="test", typeof="cube", WHD=(2, 1, 3), weight=1, level=1, loadbear=100, updown=True, color="yellow"))
    packer.addItem(Item(partno="Box-2", name="test", typeof="cube", WHD=(3, 1, 2), weight=1, level=1, loadbear=100, updown=True, color="pink"))  # Try switching WHD=(3, 1, 2) and (2, 1, 3) to compare the results
    packer.addItem(Item(partno="Box-3", name="test", typeof="cube", WHD=(2, 1, 3), weight=1, level=1, loadbear=100, updown=True, color="brown"))
    packer.addItem(Item(partno="Box-4", name="test", typeof="cube", WHD=(2, 1, 3), weight=1, level=1, loadbear=100, updown=True, color="cyan"))
    packer.addItem(Item(partno="Box-5", name="test", typeof="cube", WHD=(2, 1, 3), weight=1, level=1, loadbear=100, updown=True, color="olive"))

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
    example3()
