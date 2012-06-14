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
import scipy.signal
import pdb

def get_offset(im1, im2, im1_rect=None, im2_rect=None, hamming=False):
    """Get the translation offset between two similar images that are 
    displaced by some (x, y).  

    A correlation calculated between im1 and im2 is used to determine 
    the amount that im2 should be translated to align with im1.

    If im1_rect or im2_rect are given, only the regions defined by those 
    rectangles are considered in the correlation. This has the added benefit 
    of possibly speeding up the calculation.

    If hamming is True then a hamming window is applied to both image matrices
    before correlation, which might help align some combinations of images
    better.

    Args:
        im1: A 2D numpy array representing an image.
        im2: A 2D numpy array representing an image that will be attempted to
            align with im1.
        im1_rect: A tuple of coordinate pairs ((x1, y1), (x2, y2)) defining 
            a rectangle in im1 to use for alignment.
        im2_rect: A tuple of coordinate pairs ((x1, y1), (x2, y2)) defining 
            a rectangle in im2 to use for alignment.
        hamming: If True, a hamming window is applied to both arrays before
            correlation.
    
    Returns:
        A tuple (x, y) representing the offset of the top left corner of im2
        when aligned with the top left corner of im1.

    Requires:
        If im1_rect or im2_rect are given, they must define rectangles within
        the bounds of im1 and im2, respectively.
    """
    
    if im1_rect is None:
        (h, w) = im1.shape
        im1_rect = ((0, 0), np.unravel_index(im1.size-1, (w, h)))
    if im2_rect is None:
        (h, w) = im2.shape
        im2_rect = ((0, 0), np.unravel_index(im2.size-1, (w, h)))
    # TODO: assert im1_rect and im2_rect are within im1, im2 bounds
    
    # TODO: if hamming, then hamm up im1 and im2
    
    xcorr = scipy.signal.fftconvolve(im1, im2[::-1, ::-1])
    """Do the cross-correlation, which requires flipping im2"""
    
    xcorr_max = np.unravel_index(xcorr.argmax(), xcorr.shape)
    offset = (xcorr_max[1] - im2_rect[1][0], xcorr_max[0] - im2_rect[1][1])
    
    return offset
    


def deflicker():
    raise NotImplementedException 
