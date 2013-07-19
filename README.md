mpo2stereo
======================

A simple python script to transform a MPO (Multi-Picture Object) image file from a stereo 3D camera (such as the Fujifilm FinePix Real 3D W3) into a side-by-side stereographic photo.  Since the script was written specifically for easy stereo viewing, it makes some basic assumptions including:

1. The MPO file contains only two JPEG-Exif images (though the [MPO specification](http://www.cipa.jp/english/hyoujunka/kikaku/pdf/DC-007_E.pdf) allow for more)
2. Each image has the same dimensions
3. The input files have a `.mpo` or `.jpg` extension

### Usage:

`mpo2stereo.py` makes use of the [Python Imaging Library (PIL)](http://www.pythonware.com/products/pil/).  

    Usage: mpo2stereo.py [options] mpofiles(s)

    Options:
      -h, --help      show this help message and exit
      -p, --parallel  produce parallel rather than crosseye stereos.

If called as

    mpo2stereo.py myfile.mpo

The script will output either a parallel or crosseye formatted stereo image with filename `myfile_parallel.jpg` or `myfile_crosseye.jpg`, respectfully.  
