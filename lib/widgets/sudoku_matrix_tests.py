#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    tkGAME - all-in-one Game library for Tkinter

    Copyright (c) 2014+ Raphaël Seban <motus@laposte.net>

    This program is free software: you can redistribute it and/or
    modify it under the terms of the GNU General Public License as
    published by the Free Software Foundation, either version 3 of
    the License, or (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
    General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.

    If not, see http://www.gnu.org/licenses/
"""

# sudoku_matrix.py module testings
from sudoku_matrix import *

# get stats
from statistics import mean

# get chronometer
from timeit import timeit


# -------------------------- MODULE FUNCTION DEFS ----------------------


# testing matrix' cells location correct numbering
def test_cells_locations (algo_level=9):
    print("\n" + "-" * 60)
    print(
        "\nVerifying all cells are correctly relocated "
        "after a generate/shuffle operation"
    )
    print("\nUsing shuffle algo level:", algo_level)
    print()
    # inits
    matrix = SudokuMatrix()
    # make shufflings
    matrix.generate(level=algo_level)
    # put artificial error
    #~ matrix.algo_shuffle_7()
    # browse indexed cells
    for _i, _cell in enumerate(matrix):
        # carriage return at columns end
        if _i and not _i % matrix.columns: print()
        # show cell location
        print((_cell.row, _cell.column), end="")
        # not the right location?
        if _cell.row * matrix.columns + _cell.column != _i:
            # notify error
            print(" <-- ERROR!")
            exit(1)
        # end if
    # end for
    # succeeded
    print("\n\nAll has been verified OK.")
# end def


# trying with Euler's latin square
def test_euler_latin_square ():
    print("\n" + "-" * 60)
    print("\nTrying with Euler's latin square (module function):\n")
    data = euler_latin_square()
    print(fancy_grid(data))
    print(
        "\ngenerated grid in {:0.6f} sec"
        .format(timeit(euler_latin_square, number=1))
    )
    print(
        "\nverified grid in {:0.6f} sec"
        .format(timeit(lambda:is_correct_grid(data), number=1))
    )
    print("\ngrid is correct:", is_correct_grid(data))
# end def


# trying with LERS2 Sudoku grid module's function
def test_lers2_module ():
    print("\n" + "-" * 60)
    print("\nTrying with LERS2 Sudoku grid (module function):\n")
    data = lers2_sudoku_grid()
    print(fancy_grid(data))
    print(
        "\ngenerated grid in {:0.6f} sec"
        .format(timeit(lers2_sudoku_grid, number=1))
    )
    print(
        "\nverified grid in {:0.6f} sec"
        .format(timeit(lambda:is_correct_grid(data), number=1))
    )
    print("\ngrid is correct:", is_correct_grid(data))
# end def


# main test
def test_main (level=1, qty=10):
    # grid generation test
    matrix = SudokuMatrix()
    # stats data inits
    data1 = list()
    data2 = list()
    print("\n" + "-" * 60)
    print("\nTesting: {}".format(matrix.__class__.__name__))
    print(matrix.__doc__.replace("    ", " "))
    print("Generation complexity level:", level)
    print(
        eval("matrix.algo_shuffle_{}.__doc__".format(level))
        .replace("    ", " ")
    )
    print("Measure samples:")
    # let's make some tests
    for n in range(qty):
        # generate grid
        t = timeit(lambda:matrix.generate(level), number=1)
        # add to stats data
        data1.append(t)
        if not(n % (qty // 5 or 1)):
            print("[LERS2] grid generated in: {:0.6f} sec".format(t))
            t = timeit(matrix.verify_correct, number=1)
            data2.append(t)
            print("[CHECK] verified in: {:0.6f} sec".format(t))
        # end if
        # reveal answer
        matrix.reveal()
        # verify: erroneous grid?
        if not matrix.verify_correct():
            print(matrix)
            print("\n[ERROR] incorrect grid!")
            exit(1)
        # end if
    # end for
    print("\n[STATS] nb of generated grids:", qty)
    print(
        "\n[STATS] grid generation mean time: {:0.6f} sec"
        .format(mean(data1))
    )
    print(
        "[STATS] grid verification mean time: {:0.6f} sec"
        .format(mean(data2))
    )
    print("\n[SUCCESS] all grids have been tested OK.")
# end def


def test_main_all_levels (till=9, qty=10):
    # browse levels
    for _i in range(till):
        # try main test
        test_main(level=_i, qty=qty)
    # end for
# end def


# detailed testing of shuffle algorithms
def test_shuffle (algo=2, qty=10):
    # inits
    algo_name = "algo_shuffle_{}".format(algo)
    algo_method = "{}()".format(algo_name)
    # matrix inits
    matrix = SudokuMatrix()
    # generate answer grid
    matrix.generate()
    matrix.reveal()
    # stdout
    print("\n" + "-" * 60)
    print("\nTesting: {}".format(matrix.__class__.__name__))
    print(matrix.__doc__.replace("    ", " "))
    print("Testing shuffle algorithm: {}".format(algo_method))
    print(
        eval("matrix.{}.__doc__".format(algo_name))
        .replace("    ", " ")
    )
    print(">>> GENUINE matrix:")
    print(fancy_grid(matrix))
    print("matrix is correct: {}".format(matrix.verify_correct()))
    # force shuffling
    for i in range(qty):
        print(
            "\n({}): shuffling matrix with {}"
            .format(i + 1, algo_method)
        )
        exec("matrix.{}".format(algo_method))
        print(fancy_grid(matrix))
        ok = matrix.verify_correct()
        print("matrix is correct: {}".format(ok))
        if not ok:
            print("\n[ERROR] matrix is INCORRECT!")
            exit(1)
        # end if
    # end for
# end def



# ----------------------------- NOW TESTING -------------------------


# session start
print("\n--- BEGIN TEST SESSION ---")

test_main(level=0, qty=1000)

#~ test_main_all_levels(till=9, qty=100)

#~ test_shuffle(algo=0, qty=3)

#~ for level in range(1, 10): test_cells_locations(level)

#~ test_cells_locations()

#~ test_euler_latin_square()

#~ test_lers2_module()

# session end
print("\n--- END OF TEST SESSION ---")
