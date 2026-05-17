from eytelwein.belt_conveyor_design.constants import PulleyLoadFactor


def test_from_percent_value_above_100():
    assert PulleyLoadFactor.from_percent_value(101) == PulleyLoadFactor.above_100


def test_from_percent_value_above_60_up_to_100():
    assert (
        PulleyLoadFactor.from_percent_value(61) == PulleyLoadFactor.above_60_up_to_100
    )


def test_from_percent_value_above_30_up_to_60():
    assert PulleyLoadFactor.from_percent_value(31) == PulleyLoadFactor.above_30_up_to_60


def test_from_percent_value_up_to_30():
    assert PulleyLoadFactor.from_percent_value(30) == PulleyLoadFactor.up_to_30


def test_from_percent_value_edge_case_100():
    assert (
        PulleyLoadFactor.from_percent_value(100) == PulleyLoadFactor.above_60_up_to_100
    )


def test_from_percent_value_edge_case_60():
    assert PulleyLoadFactor.from_percent_value(60) == PulleyLoadFactor.above_30_up_to_60


def test_from_percent_value_edge_case_30():
    assert PulleyLoadFactor.from_percent_value(30) == PulleyLoadFactor.up_to_30


def test_str_method_returns_correct_value():
    assert str(PulleyLoadFactor.above_100) == "above_100"
    assert str(PulleyLoadFactor.above_60_up_to_100) == "above_60_up_to_100"
    assert str(PulleyLoadFactor.above_30_up_to_60) == "above_30_up_to_60"
    assert str(PulleyLoadFactor.up_to_30) == "up_to_30"


def test_get_max_value_above_100():
    assert PulleyLoadFactor.above_100.get_max_value() == 140


def test_get_max_value_above_60_up_to_100():
    assert PulleyLoadFactor.above_60_up_to_100.get_max_value() == 100


def test_get_max_value_above_30_up_to_60():
    assert PulleyLoadFactor.above_30_up_to_60.get_max_value() == 60


def test_get_max_value_up_to_30():
    assert PulleyLoadFactor.up_to_30.get_max_value() == 30
