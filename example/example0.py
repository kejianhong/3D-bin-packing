import logging
import time

from py3dbp import Bin, BinType, Item, Packer, log

from .utils import PrintPackingResult


def example0() -> None:
    """
    This example can be used to compare the fix_point function with and without the fix_point function.
    """

    packer = Packer()

    # Evergreen Real Container (20ft Steel Dry Cargo Container)
    # Unit cm/kg
    box = Bin(
        partno="example0",
        WHD=(589.8, 243.8, 259.1),
        max_weight=28080,
        corner=15,
        bin_type=BinType.openTop,
    )
    packer.addBin(box)

    # Dyson DC34 (20.5 * 11.5 * 32.2 ,1.33kg)
    # 64 pcs per case, 82 * 46 * 170 (85.12)
    for i in range(5):
        packer.addItem(
            Item(
                partno="Dyson DC34 Animal{}".format(str(i + 1)),
                name="Dyson",
                typeof="cube",
                WHD=(170, 82, 46),
                weight=85.12,
                level=1,
                loadbear=100,
                updown=True,
                color="#FF0000",
            )
        )

    # Washing machine (85 * 60 *60 ,10 kG)
    # 1 pcs per case, 85 * 60 *60 (10)
    for i in range(10):
        packer.addItem(
            Item(
                partno="wash{}".format(str(i + 1)),
                name="wash",
                typeof="cube",
                WHD=(85, 60, 60),
                weight=10,
                level=1,
                loadbear=100,
                updown=True,
                color="#FFFF37",
            )
        )

    # 42U standard cabinet (60 * 80 * 200 , 80 kg)
    # 1 psc per box, 60 * 80 * 200 (80)
    for i in range(5):
        packer.addItem(
            Item(
                partno="Cabinet{}".format(str(i + 1)),
                name="cabint",
                typeof="cube",
                WHD=(60, 80, 200),
                weight=80,
                level=1,
                loadbear=100,
                updown=True,
                color="#842B00",
            )
        )

    # Server (70 * 100 * 30 , 20 kg)
    # 1 per box, 70 * 100 * 30 (20)
    for i in range(10):
        packer.addItem(
            Item(
                partno="Server{}".format(str(i + 1)),
                name="server",
                typeof="cube",
                WHD=(70, 100, 30),
                weight=20,
                level=1,
                loadbear=100,
                updown=True,
                color="#0000E3",
            )
        )

    # Calculate packing.
    start = time.time()
    packer.pack(
        bigger_first=True,
        distribute_items=False,
        fix_point=True,  # Try switching fix_point=True/False to compare the results
        check_stable=True,
        support_surface_ratio=0.75,
    )
    stop = time.time()
    PrintPackingResult(packer)
    log.info(f"used time: {stop - start}")


if __name__ == "__main__":
    log.setLevel(logging.DEBUG)
    example0()
