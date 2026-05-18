from eytelwein.belt_conveyor_design.core.design_of_conveyor_belt import (
    addition_to_minimum_cover_thickness,
)
from eytelwein.belt_conveyor_design.constants import BeltCoverCharacteristicsAssessments


def test_addition_to_minimum_cover_thickness_favourable_conditions():
    result = addition_to_minimum_cover_thickness(
        BeltCoverCharacteristicsAssessments.FAVOURABLE,
        BeltCoverCharacteristicsAssessments.FAVOURABLE,
        BeltCoverCharacteristicsAssessments.FAVOURABLE,
        BeltCoverCharacteristicsAssessments.FAVOURABLE,
        BeltCoverCharacteristicsAssessments.FAVOURABLE,
    )
    assert result == (0, 1)


def test_addition_to_minimum_cover_thickness_unfavourable_conditions():
    result = addition_to_minimum_cover_thickness(
        BeltCoverCharacteristicsAssessments.UNFAVOURABLE,
        BeltCoverCharacteristicsAssessments.UNFAVOURABLE,
        BeltCoverCharacteristicsAssessments.UNFAVOURABLE,
        BeltCoverCharacteristicsAssessments.UNFAVOURABLE,
        BeltCoverCharacteristicsAssessments.UNFAVOURABLE,
    )
    assert result == (11, 15)


def test_addition_to_minimum_cover_thickness_mixed_conditions():
    result = addition_to_minimum_cover_thickness(
        BeltCoverCharacteristicsAssessments.FAVOURABLE,
        BeltCoverCharacteristicsAssessments.AVERAGE,
        BeltCoverCharacteristicsAssessments.UNFAVOURABLE,
        BeltCoverCharacteristicsAssessments.AVERAGE,
        BeltCoverCharacteristicsAssessments.FAVOURABLE,
    )
    assert result == (3, 6)


def test_addition_to_minimum_cover_thickness_edge_case_low():
    result = addition_to_minimum_cover_thickness(
        BeltCoverCharacteristicsAssessments.FAVOURABLE,
        BeltCoverCharacteristicsAssessments.FAVOURABLE,
        BeltCoverCharacteristicsAssessments.FAVOURABLE,
        BeltCoverCharacteristicsAssessments.FAVOURABLE,
        BeltCoverCharacteristicsAssessments.AVERAGE,
    )
    assert result == (0, 1)


def test_addition_to_minimum_cover_thickness_edge_case_high():
    result = addition_to_minimum_cover_thickness(
        BeltCoverCharacteristicsAssessments.UNFAVOURABLE,
        BeltCoverCharacteristicsAssessments.UNFAVOURABLE,
        BeltCoverCharacteristicsAssessments.UNFAVOURABLE,
        BeltCoverCharacteristicsAssessments.UNFAVOURABLE,
        BeltCoverCharacteristicsAssessments.AVERAGE,
    )
    assert result == (11, 15)
