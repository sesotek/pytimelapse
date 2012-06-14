"""This module provides methods for image processing related to
making time-lapses.
"""

"""Copyright 2012 Ian Smith

This library is free software; you can redistribute it and/or
modify it under the terms of the GNU Lesser General Public
License as published by the Free Software Foundation; either
version 2.1 of the License, or (at your option) any later version.

This library is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public
License along with this library; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA
"""

import numpy as np
import scipy

def get_offset(im1, im2, rect=None):
    """Get the offset between two similar images that are displaced by
    some (x, y).

    A correlation calculated between im1 and im2 is used to determine 
    the amount that im2 should be translated to align with im1.

    If rect is given, only th
    
    """
    pass

def deflicker:
    raise NotImplementedException 
