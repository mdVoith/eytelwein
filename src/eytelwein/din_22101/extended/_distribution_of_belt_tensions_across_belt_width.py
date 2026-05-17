import math


def _distance_belt_edge_deepest_level_of_trough(
    part_of_belt_lying_on_side_idler: float, troughing_angle: float
) -> float:
    """
    Calculate the distance from the belt edge to the deepest level of the trough.

    :param part_of_belt_lying_on_side_idler: The part of the belt lying on the side idler.
    :param troughing_angle: The angle of the troughing.
    :return: The distance from the belt edge to the deepest level of the trough.
    """
    return part_of_belt_lying_on_side_idler * math.sin(troughing_angle)
