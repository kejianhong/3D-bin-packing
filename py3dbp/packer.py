from dataclasses import dataclass
from typing import List, Set, Tuple

from .bin import Bin
from .constants import Axis, Axis_All, BinType, RotationType
from .item import Item
from .logger import log


@dataclass
class Area:
    width: Set[int]
    depth: Set[int]
    gravity: float


class Packer:
    def __init__(self) -> None:
        self.bins: List[Bin] = []
        self.items: List[Item] = []
        self.unfit_items: List[Item] = []
        self.total_items: int = 0
        self.binding: List[Tuple[str, ...]] = []  # Only consider the item contained in the binding.

    def addBin(self, bin: Bin) -> None:
        self.bins.append(bin)

    def addItem(self, item: Item) -> None:
        self.total_items = len(self.items) + 1
        self.items.append(item)

    @staticmethod
    def pack2Bin(bin: Bin, item: Item, fix_point: bool, check_stable: bool, support_surface_ratio: float) -> None:
        """
        Whether to put the items into the bin. Put the item into the `bin.items` and `bin.fit_items`, otherwise put it into the `bin.unfix_item`.
        :param bin: The target bin.
        :param item: The items to pack.
        :param fix_point: If true, the item will not float in the air.
        :param check_stable: If true, check the support surface ratio of the item satisfy the constraint.
        :param support_surface_ratio: The support surface ratio constraint. The item will not be packed if its support surface ratio smaller than the constraint.
        """
        bin.fix_point = fix_point
        bin.check_stable = check_stable
        bin.support_surface_ratio = support_surface_ratio

        if bin.corner_size != 0 and len(bin.items) == 0:  # Put the corner item into the empty bin if corner exits.
            log.debug(f"Adding corner items.")
            bin.generateCorner()
        elif len(bin.items) == 0:  # No corner item, then try to put the first item into the empty bin.
            response = bin.putItem(item=item, pivot=item.position)
            if not response:
                bin.unfitted_items.append(item)
            return

        # Now the bin is not empty.
        fitted = False
        for axis in Axis_All:
            items_in_bin = reversed(bin.items)  # TODO: first check the latest item putting into the bin.
            for ib in items_in_bin:
                w, h, d = [float(val) for val in ib.getDimension()]
                if axis == Axis.WIDTH:
                    pivot = [ib.position[0] + w, ib.position[1], ib.position[2]]
                elif axis == Axis.HEIGHT:
                    pivot = [ib.position[0], ib.position[1] + h, ib.position[2]]
                elif axis == Axis.DEPTH:
                    pivot = [ib.position[0], ib.position[1], ib.position[2] + d]
                else:
                    raise ValueError(f"Invalid {axis = }.")

                if bin.putItem(item=item, pivot=pivot):
                    fitted = True
                    break
            if fitted:
                break
        if not fitted:
            bin.unfitted_items.append(item)

    def sortBinding(self) -> None:
        """
        Sorted by binding. For the item which doesn't include by the binding, mark it as the unfit item of the bin.
        """
        b: List[List[Item]] = []
        for i in range(len(self.binding)):
            b.append([])
            for item in self.items:
                if item.name in self.binding[i]:
                    b[i].append(item)

        min_c = min([len(i) for i in b])
        sort_bind = []
        for iIndex in range(min_c):
            for jIndex in range(len(b)):
                sort_bind.append(b[jIndex][iIndex])

        for item in self.items:
            if item not in sort_bind:
                self.unfit_items.append(item)

        self.items = sort_bind

    def putOrder(self) -> None:
        """
        Arrange the order of items.
        """
        for bin in self.bins:
            # Open-top container.
            if bin.bin_type == BinType.openTop:
                bin.items.sort(key=lambda item: item.position[0], reverse=False)
                bin.items.sort(key=lambda item: item.position[1], reverse=False)
                bin.items.sort(key=lambda item: item.position[2], reverse=False)
            # General container.
            elif bin.bin_type == BinType.openSide:
                bin.items.sort(key=lambda item: item.position[1], reverse=False)
                bin.items.sort(key=lambda item: item.position[2], reverse=False)
                bin.items.sort(key=lambda item: item.position[0], reverse=False)
            else:
                raise ValueError(f"Bin type [{bin.bin_type}] is invalid.")

    @staticmethod
    def gravityCenter(bin: Bin) -> List[float]:
        """
        Deviation Of Cargo gravity distribution
        """
        w = int(bin.width)
        h = int(bin.height)
        d = int(bin.depth)

        # Cut the x-y plane of the bin into four area.
        #         coordinate of the pallet
        #                   ▲ y(h)
        #                   │
        #                   │
        #         area3     │     area4
        #                   │
        #      ─────────────┼─────────────▶ x(w)
        #                   │
        #          area1    │     area2
        #                   │
        #                   │
        area1: Area = Area(set(range(0, w // 2 + 1)), set(range(0, h // 2 + 1)), gravity=0)
        area2: Area = Area(set(range(w // 2 + 1, w + 1)), set(range(0, h // 2 + 1)), gravity=0)
        area3: Area = Area(set(range(0, w // 2 + 1)), set(range(h // 2 + 1, h + 1)), gravity=0)
        area4: Area = Area(set(range(w // 2 + 1, w + 1)), set(range(h // 2 + 1, h + 1)), gravity=0)
        area: List[Area] = [area1, area2, area3, area4]

        for item in bin.items:
            x_st = int(item.position[0])
            y_st = int(item.position[1])
            width = float(item.width)
            height = float(item.height)
            depth = float(item.depth)
            if item.rotation_type == RotationType.RT_WHD:
                x_ed = int(item.position[0] + width)
                y_ed = int(item.position[1] + height)
            elif item.rotation_type == RotationType.RT_HWD:
                x_ed = int(item.position[0] + height)
                y_ed = int(item.position[1] + width)
            elif item.rotation_type == RotationType.RT_HDW:
                x_ed = int(item.position[0] + height)
                y_ed = int(item.position[1] + depth)
            elif item.rotation_type == RotationType.RT_DHW:
                x_ed = int(item.position[0] + depth)
                y_ed = int(item.position[1] + height)
            elif item.rotation_type == RotationType.RT_DWH:
                x_ed = int(item.position[0] + depth)
                y_ed = int(item.position[1] + width)
            elif item.rotation_type == RotationType.RT_WDH:
                x_ed = int(item.position[0] + width)
                y_ed = int(item.position[1] + depth)
            else:
                raise ValueError(f"Rotation type = [{item.rotation_type}] is invalid.")

            x_set = set(range(x_st, int(x_ed) + 1))
            y_set = set(range(y_st, y_ed + 1))

            # Calculate the gravity distribution.
            for areaIndex in range(len(area)):
                if x_set.issubset(area[areaIndex].width) and y_set.issubset(area[areaIndex].depth):
                    area[areaIndex].gravity += int(item.weight)
                    break
                # include x and !include y
                elif x_set.issubset(area[areaIndex].width) == True and y_set.issubset(area[areaIndex].depth) == False and len(y_set & area[areaIndex].depth) != 0:
                    y = len(y_set & area[areaIndex].depth) / (y_ed - y_st) * int(item.weight)
                    area[areaIndex].gravity += y
                    if areaIndex >= 2:
                        area[areaIndex - 2].gravity += int(item.weight) - y
                    else:
                        area[areaIndex + 2].gravity += int(item.weight) - y
                    break
                # include y and !include x
                elif x_set.issubset(area[areaIndex].width) == False and y_set.issubset(area[areaIndex].depth) == True and len(x_set & area[areaIndex].width) != 0:
                    x = len(x_set & area[areaIndex].width) / (x_ed - x_st) * int(item.weight)
                    area[areaIndex].gravity += x
                    if areaIndex >= 2:
                        area[areaIndex - 2].gravity += int(item.weight) - x
                    else:
                        area[areaIndex + 2].gravity += int(item.weight) - x
                    break
                # !include x and !include y
                elif x_set.issubset(area[areaIndex].width) == False and y_set.issubset(area[areaIndex].depth) == False and len(y_set & area[areaIndex].depth) != 0 and len(x_set & area[areaIndex].width) != 0:
                    all_area = (y_ed - y_st) * (x_ed - x_st)
                    y = len(y_set & area[0].depth)
                    y_2 = y_ed - y_st - y
                    x = len(x_set & area[0].width)
                    x_2 = x_ed - x_st - x
                    area[0].gravity += x * y / all_area * int(item.weight)
                    area[1].gravity += x_2 * y / all_area * int(item.weight)
                    area[2].gravity += x * y_2 / all_area * int(item.weight)
                    area[3].gravity += x_2 * y_2 / all_area * int(item.weight)
                    break

        r = [currArea.gravity for currArea in area]
        result = []
        for val in r:
            result.append(round(val / sum(r) * 100, 2))
        return result

    def pack(
        self,
        bigger_first: bool = False,
        distribute_items: bool = True,
        fix_point: bool = True,
        check_stable: bool = True,
        support_surface_ratio: float = 0.75,
        binding: List[Tuple[str, ...]] = [],
    ) -> None:
        """
        Pack all the item into the bins.
        :param bigger_first: Fill the bigger bin with the bigger item first.
        :param distribute_items:
            If you have multiple boxes, you can change distribute_items to achieve different packaging purposes.
            distribute_items=True , put the items into the box in order, if the box is full, the remaining items will continue to be loaded into the next box until all the boxes are full  or all the items are packed.
            distribute_items=False, compare the packaging of all boxes, that is to say, each box packs all items, not the remaining items.
        :param fix_point: Whether to fix the item in the air.
        :param check_stable: Check the stability of the item. The item which not satisfy the stability will be removed.
        :param support_surface_ratio: Filtered the item which not satisfies the support surface ratio.
        :param binding: Specify the item which wants to put together into bin.
        """

        if len(binding) > 0:  # sorted by binding
            # add binding attribute
            self.binding = binding
            self.sortBinding()

        # Bin : sorted by volume
        self.bins.sort(key=lambda bin: bin.getVolume(), reverse=bigger_first)
        # Item : sorted by volume -> sorted by loadbear -> sorted by level -> binding
        self.items.sort(key=lambda item: item.getVolume(), reverse=bigger_first)
        self.items.sort(key=lambda item: item.loadbear, reverse=True)
        self.items.sort(key=lambda item: item.level, reverse=False)

        for idx, bin in enumerate(self.bins):
            if len(self.binding) > 0:
                bin.unconsidered_items = self.unfit_items
            # pack item to bin
            for item in self.items:
                self.pack2Bin(bin, item, fix_point, check_stable, support_surface_ratio)

            # Deviation Of Cargo Gravity Center
            self.bins[idx].gravity = self.gravityCenter(bin)

            if distribute_items:
                for bin_item in bin.items:
                    no = bin_item.partno
                    for item in self.items:
                        if item.partno == no:
                            self.items.remove(item)
                            break

        # put order of items
        self.putOrder()

        self.unfit_items += list(set([item for bin in self.bins for item in bin.unfitted_items]))
