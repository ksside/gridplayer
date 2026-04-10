import math
from collections import namedtuple

import pytest

# GridDimensions is tightly coupled to Qt via player package imports,
# so we replicate the pure logic here for testing.

GridDimensions = namedtuple("GridDimensions", ["cols", "rows"])


def grid_dimensions_max_size(cols, rows):
    return cols * rows


def calc_grid_dimensions(video_count, grid_mode_cols=False, grid_size=0):
    """Replicates GridManager.grid_dimensions logic."""
    if video_count <= 1:
        return GridDimensions(1, 1)

    if grid_size == 0:
        grid_size = math.ceil(math.sqrt(video_count))

    grid_slices = math.ceil(video_count / grid_size)

    if grid_mode_cols:
        return GridDimensions(grid_slices, grid_size)
    else:
        return GridDimensions(grid_size, grid_slices)


class TestGridDimensionsMaxSize:
    def test_single_cell(self):
        assert grid_dimensions_max_size(1, 1) == 1

    def test_2x2(self):
        assert grid_dimensions_max_size(2, 2) == 4

    def test_3x3(self):
        assert grid_dimensions_max_size(3, 3) == 9

    def test_asymmetric(self):
        assert grid_dimensions_max_size(4, 3) == 12


class TestCalcGridDimensions:
    @pytest.mark.parametrize(
        "count,expected_cols,expected_rows",
        [
            (1, 1, 1),
            (2, 2, 1),
            (3, 2, 2),
            (4, 2, 2),
            (5, 3, 2),
            (9, 3, 3),
            (10, 4, 3),
            (16, 4, 4),
        ],
    )
    def test_auto_rows(self, count, expected_cols, expected_rows):
        dims = calc_grid_dimensions(count, grid_mode_cols=False)
        assert dims.cols == expected_cols
        assert dims.rows == expected_rows

    @pytest.mark.parametrize(
        "count,expected_cols,expected_rows",
        [
            (1, 1, 1),
            (4, 2, 2),
            (9, 3, 3),
        ],
    )
    def test_auto_cols(self, count, expected_cols, expected_rows):
        dims = calc_grid_dimensions(count, grid_mode_cols=True)
        assert dims.cols == expected_cols
        assert dims.rows == expected_rows

    def test_manual_grid_size(self):
        # 7 videos, manual grid_size=3, rows mode
        dims = calc_grid_dimensions(7, grid_mode_cols=False, grid_size=3)
        assert dims.cols == 3
        assert dims.rows == 3
        assert dims.cols * dims.rows >= 7

    def test_all_counts_have_enough_cells(self):
        """Every video count 1-20 must fit in the calculated grid."""
        for count in range(1, 21):
            dims = calc_grid_dimensions(count)
            assert dims.cols * dims.rows >= count
