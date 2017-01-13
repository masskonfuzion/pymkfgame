#############################################################################
# Copyright 2016 Mass KonFuzion
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#############################################################################

import math

EPSILON = 1e-5
DEGTORAD = math.pi / 180.0
RADTODEG = 180.0 / math.pi

COSS = [ math.cos(th * DEGTORAD) for th in range(0, 360) ]  # Note that Python allows negative indexes, which happen to work flawlessly here. In other languages, you'll need to correct indiexes out of range of 0..360
SINN = [ math.sin(th * DEGTORAD) for th in range(0, 360) ]
TANN = [ math.tan(th * DEGTORAD) for th in range(0, 360) ]

def coss(deg):
    int_part = int(deg)
    dec_part = deg - int_part

    return COSS[int_part] + dec_part * (COSS[(int_part + 1) % 360] - COSS[int_part])

def sinn(deg):
    int_part = int(deg)
    dec_part = deg - int_part

    return SINN[int_part] + dec_part * (SINN[(int_part + 1) % 360] - SINN[int_part])


def tann(deg):
    int_part = int(deg)
    dec_part = deg - int_part

    return TANN[int_part] + dec_part * (TANN[(int_part + 1) % 360] - TANN[int_part])

def isZero(num, threshold=EPSILON):
    """ Return true if a number is near 0

        NOTE: no error testing here.. Don't be an idiot
    """
    return float(num) < threshold

def floatEq(a, b, threshold=EPSILON):
    return abs(a - b) < threshold

def floatLt(a, b, threshold=EPSILON):
    return a < b + threshold

def floatLte(a, b, threshold=EPSILON):
    return a <= b + threshold

def floatGt(a, b, threshold=EPSILON):
    return a > b - threshold

def floatGte(a, b, threshold=EPSILON):
    return a >= b - threshold

def floatStr(n):
    if n < EPSILON:
        return str(0.0)
    else:
        return str(float(n))


