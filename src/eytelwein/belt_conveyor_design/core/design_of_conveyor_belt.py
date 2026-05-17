from eytelwein.belt_conveyor_design.constants import BeltCoverCharacteristicsAssessments


def addition_to_minimum_cover_thickness(
    feeding_condition: BeltCoverCharacteristicsAssessments,
    cycle_time: BeltCoverCharacteristicsAssessments,
    top_size: BeltCoverCharacteristicsAssessments,
    bulk_density: BeltCoverCharacteristicsAssessments,
    abrasivity: BeltCoverCharacteristicsAssessments,
) -> tuple[int, int]:
    """
    Calculates the recommended addition to the minimum cover thickness for a conveyor belt based on several assessment criteria.
    Parameters:
        feeding_condition (BeltCoverCharacteristicsAssessments): Assessment of the feeding condition.
        cycle_time (BeltCoverCharacteristicsAssessments): Assessment of the cycle time.
        top_size (BeltCoverCharacteristicsAssessments): Assessment of the top size of the material.
        bulk_density (BeltCoverCharacteristicsAssessments): Assessment of the bulk density of the material.
        abrasivity (BeltCoverCharacteristicsAssessments): Assessment of the material's abrasivity.
    Returns:
        tuple[int, int]: A tuple representing the recommended range (in millimeters) to be added to the minimum cover thickness.
    """
    evaluation = 0
    evaluation += feeding_condition.to_int()
    evaluation += cycle_time.to_int()
    evaluation += top_size.to_int()
    evaluation += bulk_density.to_int()
    evaluation += abrasivity.to_int()

    if evaluation < 7:
        return (0, 1)
    elif evaluation < 9:
        return (1, 3)
    elif evaluation < 12:
        return (3, 6)
    elif evaluation < 14:
        return (6, 10)
    else:
        return (11, 15)
