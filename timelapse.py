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
import scipy.ndimage

DEBUG = False

if DEBUG:
    import pdb
    import Image as Img

def get_offset(arr1, arr2, arr1_rect=None, arr2_rect=None, hamming=False):
    """Get the translation offset between two similar image matrices that are 
    displaced by some (x, y).  

    A correlation calculated between arr1 and arr2 is used to determine 
    the amount that arr2 should be translated to align with arr1.

    If arr1_rect or arr2_rect are given, only the regions defined by those 
    rectangles are considered in the correlation. This has the benefit 
    of possibly speeding up the calculation.

    If hamming is True then a hamming window is applied to both image matrices
    before correlation, which might help align some combinations of images
    better.

    Args:
        arr1: A 2D numpy array representing an image.
        arr2: A 2D numpy array representing an image that will be attempted to
            align with arr1.
        arr1_rect: A tuple of coordinate pairs ((x1, y1), (x2, y2)) defining 
            a rectangle in arr1 to use for alignment.
        arr2_rect: A tuple of coordinate pairs ((x1, y1), (x2, y2)) defining 
            a rectangle in arr2 to use for alignment.
        hamming: If True, a hamming window is applied to both arrays before
            correlation.
    
    Returns:
        A tuple (x, y) representing the offset of the top left corner of arr2
        when aligned with the top left corner of arr1.

    Requires:
        If arr1_rect or arr2_rect are given, they must define rectangles within
        the bounds of arr1 and arr2, respectively.
    """
    
    if arr1_rect is None:
        (h, w) = arr1.shape
        arr1_rect = ((0, 0), np.unravel_index(arr1.size-1, (w, h)))
    if arr2_rect is None:
        (h, w) = arr2.shape
        arr2_rect = ((0, 0), np.unravel_index(arr2.size-1, (w, h)))
    # TODO: assert arr1_rect and arr2_rect are within arr1, arr2 bounds
    
    """Slice out the sub rectangles"""
    subrect1 = arr1[arr1_rect[0][1]:arr1_rect[1][1], arr1_rect[0][0]:arr1_rect[1][0]]
    subrect2 = arr2[arr2_rect[0][1]:arr2_rect[1][1], arr2_rect[0][0]:arr2_rect[1][0]]

    if hamming:
      """Create the hamming template for subrect1 and 2 """
      hamm255_1 = np.empty(subrect1.shape)
      hamm255_1.fill(255)
      hamm255_2 = np.empty(subrect2.shape)
      hamm255_2.fill(255)

      hamm255_1 = np.outer(np.hamming(hamm255_1.shape[0]),
          np.hamming(hamm255_1.shape[1]))
      hamm255_2 = np.outer(np.hamming(hamm255_2.shape[0]),
          np.hamming(hamm255_2.shape[1]))
      subrect1 = subrect1 * hamm255_1
      subrect2 = subrect2 * hamm255_2

    """Do the cross-correlation, which requires flipping arr2"""
    xcorr = scipy.signal.fftconvolve(subrect1, subrect2[::-1, ::-1])
    
    if DEBUG:
        _show_array(xcorr)
        _save_array(xcorr, "images/xcorr_test.png")

    xcorr_max = np.unravel_index(xcorr.argmax(), xcorr.shape)
    offset = (xcorr_max[1] - arr2_rect[1][0], xcorr_max[0] - arr2_rect[1][1])
    
    return offset
    
# TODO:  Needs a flag for expanding image to avoid crop
# TODO:  Why flip the shifting???
def shift(arr, shift):
    sflip = (shift[1], shift[0]) 
    return scipy.ndimage.shift(arr, sflip)
    
def align(im1, im2, arr1_rect=None):
    return shift(im2, get_offset(im1, im2, arr1_rect=arr1_rect, hamming=True))

def _show_array(arr):
    _array_to_image(arr).show()

def _save_array(arr, filename):
    _array_to_image(arr).save(filename)

def _array_to_image(arr):
    img = arr * 255 / arr.max()
    img = Img.fromarray(np.uint8(img))
    return img

def convertTo():
    raise NotImplementedError

def convertFrom():
    raise NotImplementedError
