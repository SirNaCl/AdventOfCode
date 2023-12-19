import pathlib
import pytest
import solution as sol

PUZZLE_DIR = pathlib.Path(__file__).parent


@pytest.fixture
def example1():
    puzzle_input = (PUZZLE_DIR / "example1.txt").read_text().strip()
    return sol.parse(puzzle_input)


@pytest.fixture
def example2():
    puzzle_input = (PUZZLE_DIR / "example2.txt").read_text().strip()
    return sol.parse(puzzle_input)


@pytest.mark.skip(reason="Not implemented")
def test_parse_example1(example1):
    """Test that input is parsed properly."""
    assert example1 == ...


def test_part1_example1(example1):
    """Test part 1 on example input."""
    assert sol.part1(example1) == 19114


def test_part2_example1(example1):
    """Test part 2 on example input."""
    assert sol.part2(example1) == 167409079868000


@pytest.mark.skip(reason="Not implemented")
def test_part2_example2(example2):
    """Test part 2 on example input."""
    assert sol.part2(example2) == ...
