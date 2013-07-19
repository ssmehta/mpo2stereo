#!/usr/bin/env python

from __future__ import print_function
from optparse import OptionParser
from PIL import Image
from StringIO import StringIO
import errno, glob, os, sys


class MPOError(Exception):
    """Error class to distinguish improper file errors from possible IOErrors"""
    def __init__(self, value): self.value = value
    def __str__(self): return repr(self.value)


def split_mpo(filename):
    """Reads a given MPO file and finds the break between the two JPEG images."""
    
    with open(filename, 'rb') as f:
        data = f.read()
        
        # Look for the hex string 0xFFD9FFD8FFE1:
        #   0xFFD9 represents the end of the first JPEG image
        #   0xFFD8FFE1 marks the start of the appended JPEG image
        idx = data.find(b'\xFF\xD8\xFF\xE1', 1)
        
        if idx > 0:
            return Image.open(StringIO(data[: idx])), Image.open(StringIO(data[idx :]))
        else:
            raise MPOError(filename)


if __name__ == '__main__':
    # Parse arguments
    parser = OptionParser('usage: %prog [options] mpofiles(s)')
    parser.add_option("-p", '--parallel', action = 'store_true', dest = 'parallel',
                      default = False, help = 'produce parallel rather than crosseye stereos.')
    (options, args) = parser.parse_args()
    
    if len(args) == 0:
        parser.error('invalid argument - requires at least one MPO file to read')
    elif len(args) == 1 and '*' in args[0]:
        args = glob.glob(args[0])
    
    
    # Process the given MPO files
    for i, filename in enumerate(args):
        try:
            # Load the right and left images (ordered for crosseye stereo)
            img_right, img_left = split_mpo(filename)
            
            # Create the stereo image
            size = (2 * img_right.size[0], img_right.size[1])
            img_stereo = Image.new('RGB', size)
            
            if options.parallel:
                img_stereo.paste(img_right, (0, 0))
                img_stereo.paste(img_left, (img_right.size[0], 0))
            else:
                img_stereo.paste(img_left, (0, 0))
                img_stereo.paste(img_right, (img_right.size[0], 0))
            
            # Save the stereo image
            stereo_type = 'parallel' if options.parallel else 'crosseye'
            filename = filename[:-4] +'_'+ stereo_type +'.jpg'
            
            print('Writing '+ filename +' (%d/%d)' % (i + 1, len(args)))
            img_stereo.save(filename)
        
        except MPOError:
            print(filename +' is not a valid MPO file')
        except IOError as e:
            print(filename +':')
            print('errno:', e.errno)
            print('err code:', errno.errorcode[e.errno])
            print('err message:', os.strerror(e.errno))
