#! /usr/bin/env python

import sys
import os

import argparse
from osgeo import gdal, ogr, osr
from pygeotools.lib import iolib, geolib


def getparser():
    parser = argparse.ArgumentParser(description="Clip Shape file to the specified extent of input Raster", \
            formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('src_fn', type=str, help='Source raster to determine extent')
    parser.add_argument('-src_shp', type=str, help='Source shp to be cliped')
    parser.add_argument('-out_fn', type=str, help='Output name of clipped shp')
    parser.add_argument('-outdir', default='.', help='Output directory')
    return parser


def main(argv=None):
    parser = getparser()
    args = parser.parse_args()

    if len(sys.argv[1:]) == 0:
        sys.exit("Usage: %s [src_fn] [-outdir] [-dst_ndv]" % os.path.basename(sys.argv[0]))

    src_fn = args.src_fn

    shp_fn = args.src_shp
    if shp_fn is None:
        datadir = iolib.get_datadir()
        shp_fn = os.path.join(datadir, 'gamdam/gamdam_merge_refine_line.shp') 

    outdir = args.outdir
    if not os.path.exists(outdir):
        os.makedirs(outdir)
    if not os.path.isabs(outdir):
        outdir = os.path.join(os.getcwd(), outdir)

    out_fn = args.out_fn
    if out_fn is None:
        out_fn = os.path.join(outdir, os.path.splitext(os.path.split(shp_fn)[-1])[0] + '_clip.shp')
    if os.path.splitext(out_fn)[-1] == '':
        out_fn = os.path.join(outdir, out_fn + '.shp')

    shp_ds = ogr.Open(shp_fn)
    lyr = shp_ds.GetLayer()
    lyr_srs = lyr.GetSpatialRef()
    shp_extent = geolib.lyr_extent(lyr)

    src_ds = gdal.Open(src_fn)
    ds_extent = geolib.ds_extent(src_ds,t_srs=lyr_srs)

    if geolib.extent_compare(shp_extent, ds_extent) is False:
        geolib.clip_shp(shp_fn, extent=ds_extent, out_fn=out_fn)
    print(out_fn)

    print('Output file: %s'% os.path.join(outdir, out_fn))

if __name__ == "__main__":
    main()
