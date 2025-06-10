from py3dbp import Packer, Painter, log


def PrintPackingResult(packer: Packer) -> None:
    for bin in packer.bins:
        volume = bin.width * bin.height * bin.depth
        log.info(f"bin is: {bin.string()}")

        fit_items_string = "FITTED ITEMS:\n"
        volume_t = 0.0
        volume_f = 0.0

        for item in bin.items:
            fit_items_string = f"{fit_items_string}{item.string()}\n"
            volume_t += item.getVolume()
        log.debug(f"{fit_items_string}")

        unfit_items_string = "UNFITTED ITEMS:\n"
        for item in bin.unfitted_items:
            unfit_items_string = f"{unfit_items_string}{item.string()}\n"
            volume_f += item.getVolume()
        log.debug(f"{unfit_items_string}")
        log.info(f"space utilization: {round(volume_t / volume * 100, 2)}")
        log.info(f"residual volume: {volume - volume_t}")
        log.info(f"unpack item volume: {volume_f}")
        log.info(f"gravity distribution: {bin.gravity}")

        painter = Painter(bin)
        fig = painter.plotItemsAndBin(title=bin.partno, alpha=0.5, write_num=False, fontsize=10)
    fig.show()
