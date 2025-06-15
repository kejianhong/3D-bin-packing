import copy
import dataclasses
from dataclasses import dataclass
from typing import List, Tuple

import numpy as np
from numpy.typing import NDArray

from .constants import DELTA, RT_ALL, Axis, BinType, RotationType, RT_NotUpdown
from .item import Item
from .logger import log


@dataclass
class Rectangle:
    left_back_x: float
    left_back_y: float
    right_front_x: float
    right_front_y: float
    center_x: float = dataclasses.field(init=False)
    center_y: float = dataclasses.field(init=False)
    length: float = dataclasses.field(init=False)
    width: float = dataclasses.field(init=False)

    def __post_init__(self) -> None:
        self.center_x = (self.left_back_x + self.right_front_x) / 2.0
        self.center_y = (self.left_back_y + self.right_front_y) / 2.0
        self.length = max(self.left_back_x, self.right_front_x) - min(self.left_back_x, self.right_front_x)
        self.width = max(self.left_back_y, self.right_front_y) - min(self.left_back_y, self.right_front_y)


def checkIntersect(rect1: Rectangle, rect2: Rectangle) -> bool:
    """
    Check whether two rectangles are intersected with each other or not.
    """
    center_distance_x = max(rect1.center_x, rect2.center_x) - min(rect1.center_x, rect2.center_x)
    center_distance_y = max(rect1.center_y, rect2.center_y) - min(rect1.center_y, rect2.center_y)
    return center_distance_x < (rect1.length + rect2.length) / 2.0 and center_distance_y < (rect1.width + rect2.width) / 2.0


def rectIntersect(item1: Item, item2: Item, axis1: Axis, axis2: Axis) -> bool:
    """
    Check whether the projection rectangle of the two items are intersected with each other or not.
    """
    item1_dimension = item1.getDimension()
    item2_dimension = item2.getDimension()
    item1_rect = Rectangle(
        left_back_x=item1.position[axis1.value],
        left_back_y=item1.position[axis2.value],
        right_front_x=item1.position[axis1.value] + item1_dimension[axis1.value],
        right_front_y=item1.position[axis2.value] + item1_dimension[axis2.value],
    )
    item2_rect = Rectangle(
        left_back_x=item2.position[axis1.value],
        left_back_y=item2.position[axis2.value],
        right_front_x=item2.position[axis1.value] + item2_dimension[axis1.value],
        right_front_y=item2.position[axis2.value] + item2_dimension[axis2.value],
    )

    return checkIntersect(rect1=item1_rect, rect2=item2_rect)


def itemIntersect(item1: Item, item2: Item) -> bool:
    """
    Check whether two 3d items are intersected with each other or not.
    :param item1: Item one.
    :param item2: Item two.
    """
    return (
        rectIntersect(item1, item2, Axis.WIDTH, Axis.HEIGHT)
        and rectIntersect(item1, item2, Axis.HEIGHT, Axis.DEPTH)
        and rectIntersect(item1, item2, Axis.WIDTH, Axis.DEPTH)
    )  # fmt: skip


def combineLineSegment(line_segment: List[List[float]]) -> List[List[float]]:
    """
    Merge the line segments if they are intersected. O(nlog(n)) for the sort algorithm.
    """
    line_segment.sort(key=lambda line: line[0])
    merge_line_segment = [line_segment[0]]
    for index in range(1, len(line_segment)):
        last_line = merge_line_segment[-1]
        curr_line = line_segment[index]
        if curr_line[0] <= last_line[1]:
            merge_line = [last_line[0], max(last_line[1], curr_line[1])]
            merge_line_segment[-1] = merge_line
        else:
            merge_line_segment.append(curr_line)
    return merge_line_segment


class Bin:
    def __init__(
        self,
        partno: str,
        WHD: Tuple[float, float, float],
        max_weight: float,
        corner: int = 0,
        bin_type: BinType = BinType.openTop,
    ):
        self.partno: str = partno
        self.width: float = WHD[0]
        self.height: float = WHD[1]
        self.depth: float = WHD[2]
        self.max_weight: float = max_weight
        self.corner_size: float = corner
        self.items: List[Item] = []  # Items in the bin.
        self.fit_items: NDArray[np.float_] = np.array([[0, WHD[0], 0, WHD[1], 0, 0]])  # Represent the back-left-down and front-right-up point of the corner item. Each row represents one item.
        self.unfitted_items: List[Item] = []  # Items can not put into the bin.
        self.unconsidered_items: List[Item] = []  # Items would not consider to put into the bin because it doesn't int the binding.
        self.fix_point: bool = False
        self.check_stable: bool = False
        self.support_surface_ratio: float = 0
        self.bin_type: BinType = bin_type  # Can only be 0 or 1.
        self.gravity: List[float] = []  # used to put gravity distribution

    def string(self) -> str:
        return f"{self.partno}({self.width}x{self.height}x{self.depth}), weight={self.max_weight}, volume={self.getVolume()}"

    def getVolume(self) -> float:
        return self.width * self.height * self.depth

    def getTotalWeight(self) -> float:
        total_weight = 0.0
        for item in self.items:
            total_weight += item.weight
        return total_weight

    def putItem(self, item: Item, pivot: List[float]) -> bool:
        """
        Check whether the current item can put into the bin.
        :param item: The item to put into the bin.
        :param pivot: The position where the item to put into.
        """
        # Check the total weight.
        if self.getTotalWeight() + item.weight > self.max_weight:
            log.info(f"Adding the current item [{item.partno}] will exceed the total weight: {item.weight}(curr) + {self.getTotalWeight()}(already) > {self.max_weight}(max).")
            return False

        valid_item_position = copy.deepcopy(item.position)
        item.position = copy.deepcopy(pivot)
        rotate = RT_ALL if item.updown == True else RT_NotUpdown
        for rt_type in rotate:
            fit = True
            item.rotation_type = rt_type
            [w, h, d] = item.getDimension()

            # The item can not put into the bin in the pivot with the current rotation type. Therefore, rotate it.
            if (
                self.width < pivot[0] + w or
                self.height < pivot[1] + h or
                self.depth < pivot[2] + d
            ):  # fmt: skip
                log.info(f"The current item [{item.partno}] can not put into the pivot {pivot}, due to outside the bin.")
                continue

            # Check whether the current item will intersect with the items which have been put into the bin.
            for current_item_in_bin in self.items:
                if itemIntersect(current_item_in_bin, item):
                    # Will go back to for loop.
                    log.info(f"The current item [{item.partno}] is intersected with the item [{current_item_in_bin.partno}].")
                    fit = False
                    break

            if fit:
                # Fix point float prob
                [x, y, z] = [copy.deepcopy(pivot[0]), copy.deepcopy(pivot[1]), copy.deepcopy(pivot[2])]
                if self.fix_point:
                    while True:
                        # fix height
                        y, is_y_change = self.checkHeight([x, x + w, y, y + h, z, z + d])
                        # fix width
                        x, is_x_change = self.checkWidth([x, x + w, y, y + h, z, z + d])
                        # fix depth
                        z, is_z_change = self.checkDepth([x, x + w, y, y + h, z, z + d])
                        if not (is_x_change | is_y_change | is_z_change):
                            log.warning(f"Fix item position from {pivot} to [{x},{y},{z}].")
                            break

                    # check stability on item
                    # rule:
                    # 1. Define a support ratio, if the ratio below the support surface does not exceed this ratio, compare the second rule.
                    # 2. If there is no support under any vertices of the bottom of the item, then fit = False.
                    if self.check_stable:
                        # Cal the surface area of item.
                        item_area_lower = int(w * h)
                        # Cal the surface area of the underlying support.
                        support_area_upper = 0
                        for item_corner in self.fit_items:
                            # Verify that the lower support surface area is greater than the upper support surface area * support_surface_ratio.
                            # Lower of the item to put is equal to the upper of the item putting into the bin.
                            if z == item_corner[5]:
                                area = (
                                    len(set([j for j in range(int(x), int(x + int(w)))]) & set( [j for j in range(int(item_corner[0]), int(item_corner[1]))]))
                                    * len(set([j for j in range(int(y), int(y + int(h)))]) & set( [j for j in range(int(item_corner[2]), int(item_corner[3]))]))
                                )  # fmt: skip
                                support_area_upper += area

                        # If not , get four vertices of the bottom of the item.
                        log.debug(f"Item [{item.partno}], dimension={item.getDimension()}, supported area = [{support_area_upper}], minimal supported rea = [{item_area_lower * self.support_surface_ratio}].")
                        if support_area_upper / item_area_lower < self.support_surface_ratio:
                            four_vertices = [
                                [x, y],
                                [x + w, y],
                                [x, y + h],
                                [x + w, y + h],
                            ]
                            #  If any vertices is not supported, fit = False.
                            c = [False, False, False, False]
                            for item_corner in self.fit_items:
                                if z == item_corner[5]:
                                    for jdx, j in enumerate(four_vertices):
                                        if (item_corner[0] <= j[0] <= item_corner[1]) and (item_corner[2] <= j[1] <= item_corner[3]):
                                            c[jdx] = True
                            log.debug(f"Item [{item.partno}] has [{sum(c)}] supported corners.")
                            if False in c:
                                continue

                if fit:
                    item.position = [x, y, z]
                    for current_item_in_bin in self.items:
                        if itemIntersect(current_item_in_bin, item):
                            # For debug, actually will never happen if the program is correct.
                            log.error(f"Current item = [{item.partno}], position = {item.position} collides with the item [{current_item_in_bin.partno}], position = {current_item_in_bin.position}.")
                            raise Exception("Collision check failed.")
                    self.fit_items = np.append(self.fit_items, np.array([[x, x + w, y, y + h, z, z + d]]), axis=0)
                    self.items.append(copy.deepcopy(item))
                    return True

        # Any rotation type can not put the item into the bin. Resume the position of the item.
        item.rotation_type = RotationType.RT_WHD
        item.position = valid_item_position
        return False

    def checkDepth(self, unfix_point: List[float]) -> Tuple[float, bool]:
        """
        Fix item position z.
        :param unfix_point: The back-left-down and front-right-up point coordinate of the item. [x_min, x_max, y_min, y_max, z_min, z_max].
        """
        z_: List[List[float]] = [[0, 0], [self.depth, self.depth]]
        for fix_item_corner in self.fit_items:
            rect1 = Rectangle(left_back_x=unfix_point[0], left_back_y=unfix_point[2], right_front_x=unfix_point[1], right_front_y=unfix_point[3])
            rect2 = Rectangle(left_back_x=fix_item_corner[0], left_back_y=fix_item_corner[2], right_front_x=fix_item_corner[1], right_front_y=fix_item_corner[3])
            if checkIntersect(rect1, rect2):
                z_.append([fix_item_corner[4], fix_item_corner[5]])
        top_depth = unfix_point[5] - unfix_point[4]
        # find diff set on z_.
        z_ = combineLineSegment(z_)
        for index in range(len(z_) - 1):
            if z_[index + 1][0] - z_[index][1] >= top_depth:
                log.info(f"Fix z(depth) from [{unfix_point[4]}] to [{z_[index][1]}].")
                return z_[index][1], np.abs(z_[index][1] - unfix_point[4]) > DELTA
        return unfix_point[4], False

    def checkWidth(self, unfix_point: List[float]) -> Tuple[float, bool]:
        """
        Fix item position x.
        :param unfix_point: The back-left-down and front-right-up point coordinate of the item. [x_min, x_max, y_min, y_max, z_min, z_max].
        """
        x_: List[List[float]] = [[0, 0], [self.width, self.width]]
        for fix_item_corner in self.fit_items:
            rect1 = Rectangle(left_back_x=unfix_point[2], left_back_y=unfix_point[4], right_front_x=unfix_point[3], right_front_y=unfix_point[5])
            rect2 = Rectangle(left_back_x=fix_item_corner[2], left_back_y=fix_item_corner[4], right_front_x=fix_item_corner[3], right_front_y=fix_item_corner[5])
            if checkIntersect(rect1, rect2):
                x_.append([fix_item_corner[0], fix_item_corner[1]])
        top_width = unfix_point[1] - unfix_point[0]
        # find diff set on x_bottom and x_top.
        # x_ = sorted(x_, key=lambda x_: x_[1])
        x_ = combineLineSegment(x_)
        for index in range(len(x_) - 1):
            if x_[index + 1][0] - x_[index][1] >= top_width:
                log.info(f"Fix x(width) from [{unfix_point[0]}] to [{x_[index][1]}].")
                return x_[index][1], np.abs(x_[index][1] - unfix_point[0]) > DELTA
        return unfix_point[0], False

    def checkHeight(self, unfix_point: List[float]) -> Tuple[float, bool]:
        """
        Fix item position y.
        :param unfix_point: The back-left-down and front-right-up point coordinate of the item. [x_min, x_max, y_min, y_max, z_min, z_max].
        """
        y_: List[List[float]] = [[0, 0], [self.height, self.height]]
        for fix_item_corner in self.fit_items:
            rect1 = Rectangle(left_back_x=unfix_point[0], left_back_y=unfix_point[4], right_front_x=unfix_point[1], right_front_y=unfix_point[5])
            rect2 = Rectangle(left_back_x=fix_item_corner[0], left_back_y=fix_item_corner[4], right_front_x=fix_item_corner[1], right_front_y=fix_item_corner[5])
            if checkIntersect(rect1, rect2):
                y_.append([fix_item_corner[2], fix_item_corner[3]])
        item_height = unfix_point[3] - unfix_point[2]
        # find diff set on y_bottom and y_top.
        y_ = combineLineSegment(y_)
        for index in range(len(y_) - 1):
            if y_[index + 1][0] - y_[index][1] >= item_height:
                log.info(f"Fix y(height) from [{unfix_point[2]}] to [{y_[index][1]}].")
                return y_[index][1], np.abs(y_[index][1] - unfix_point[2]) > DELTA

        return unfix_point[2], False

    def generateCorner(self) -> None:
        """
        Generate 8 corners as the items and put them into the bin.
        """
        if self.corner_size != 0:
            x = self.width - self.corner_size
            y = self.height - self.corner_size
            z = self.depth - self.corner_size
            pos: List[List[float]] = [  # Position of 8 corner items in the bin.
                [0, 0, 0],
                [0, 0, z],
                [0, y, z],
                [0, y, 0],
                [x, y, 0],
                [x, 0, 0],
                [x, 0, z],
                [x, y, z],
            ]
            corner_size = self.corner_size
            for index in range(8):
                corner_item = Item(
                    partno="corner{}".format(index),
                    name="corner",
                    typeof="cube",
                    WHD=(corner_size, corner_size, corner_size),
                    weight=0,
                    level=0,
                    loadbear=0,
                    updown=True,
                    color="#000000",
                )
                corner_item.position = pos[index]
                self.items.append(corner_item)

                # Represent the back-left-down and front-right-up point of the corner item. [x_min, x_max, y_min, y_max, z_min, z_max]
                corner = [
                    corner_item.position[0],
                    corner_item.position[0] + self.corner_size,
                    corner_item.position[1],
                    corner_item.position[1] + self.corner_size,
                    corner_item.position[2],
                    corner_item.position[2] + self.corner_size,
                ]

                self.fit_items = np.append(self.fit_items, np.array([corner]), axis=0)
        else:
            log.warning(f"There is no generated corner because the corner size is {self.corner_size}.")
