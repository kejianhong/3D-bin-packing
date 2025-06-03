import logging
import time

from py3dbp import Bin, BinType, Item, Packer, log

from .utils import PrintPackingResult


def example4() -> None:
    """
    This example can be used to test large batch calculation time and binding functions.
    """

    packer = Packer()

    # Evergreen Real Container (20ft Steel Dry Cargo Container)
    # Unit cm/kg
    box = Bin(
        partno="example4",
        WHD=(589.8, 243.8, 259.1),
        max_weight=28080,
        corner=15,
        bin_type=BinType.openSide,
    )

    packer.addBin(box)

    # dyson DC34 (20.5 * 11.5 * 32.2 ,1.33kg)
    # 64 pcs per case ,  82 * 46 * 170 (85.12)
    for i in range(15):
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

    # washing machine (85 * 60 *60 ,10 kG)
    # 1 pcs per case, 85 * 60 *60 (10)
    for i in range(18):
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
    # 1 per box, 60 * 80 * 200 (80)
    for i in range(15):
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
    # 1 per box , 70 * 100 * 30 (20)
    for i in range(42):
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

    start = time.time()
    packer.pack(
        bigger_first=True,
        distribute_items=False,
        fix_point=True,
        check_stable=True,
        support_surface_ratio=0.75,
        # binding=[("server", "cabint"), ("Dyson", "wash")],
        binding=[("cabint", "wash", "server")],
    )

    stop = time.time()
    PrintPackingResult(packer)
    log.info(f"used time: {stop - start}")


if __name__ == "__main__":
    log.setLevel(logging.DEBUG)
    example4()
