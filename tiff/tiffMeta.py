"""
Created on 4/30/18

@author: YJccccc
"""

from osgeo import gdal, ogr, osr


def GetExtent(tif):
    ''' Return list of corner coordinates from a geotransform

        @type gt:   C{tuple/list}
        @param gt: geotransform
        @type cols:   C{int}
        @param cols: number of columns in the dataset
        @type rows:   C{int}
        @param rows: number of rows in the dataset
        @rtype:    C{[float,...,float]}
        @return:   coordinates of each corner
    '''

    gt = tif.GetGeoTransform()
    cols = tif.RasterXSize
    rows = tif.RasterYSize

    pixelSizeX = gt[1]
    pixelSizeY = -gt[5]

    ext = []
    xarr = [0, cols]
    yarr = [0, rows]

    for px in xarr:
        for py in yarr:
            x = gt[0] + (px * gt[1]) + (py * gt[2])
            y = gt[3] + (px * gt[4]) + (py * gt[5])
            ext.append([x, y])
            # print (x,y)
        yarr.reverse()
    return cols, rows, ext,pixelSizeX,pixelSizeY


def ReprojectCoords(coords, src_srs, tgt_srs):
    ''' Reproject a list of x,y coordinates.

        @type geom:     C{tuple/list}
        @param geom:    List of [[x,y],...[x,y]] coordinates
        @type src_srs:  C{osr.SpatialReference}
        @param src_srs: OSR SpatialReference object
        @type tgt_srs:  C{osr.SpatialReference}
        @param tgt_srs: OSR SpatialReference object
        @rtype:         C{tuple/list}
        @return:        List of transformed [[x,y],...[x,y]] coordinates
    '''
    trans_coords = []
    transform = osr.CoordinateTransformation(src_srs, tgt_srs)
    for x, y in coords:
        x, y, z = transform.TransformPoint(x, y)
        trans_coords.append([x, y])
    return trans_coords


def bandStats(tif):
    bands = []
    for band in range(tif.RasterCount):
        band += 1
        # print("[ GETTING BAND ]: ", band)

        srcband = tif.GetRasterBand(band)
        if srcband is None:
            continue

        stats = srcband.GetStatistics(True, True)
        if stats is None:
            continue

        info = stats[0], stats[1], stats[2], stats[3]
        bands.append(info)
        # print("[ STATS ] =  Minimum=%.3f, Maximum=%.3f, Mean=%.3f, StdDev=%.3f" % ( \
        #     stats[0], stats[1], stats[2], stats[3]))
    return bands


# filepath = r"/Users/YJccccc/Desktop/DonglianSun_Project/SNPP_VIIRS_375m_floodmap_1826_Sep01_2017_Geographic_geotiff/SNPP_VIIRS_375m_floodmap_1826_Sep01_2017_Geographic.tif"
#
# filepath = ''
#
# # Open the file:
# raster = gdal.Open(filepath)
#
# meta = raster.GetMetadata()
# # print('Basic Info:', meta)
#
# ext = GetExtent(raster)
# dimensions = ext[0], ext[1]
# extent = ext[2]
# origin = ext[2][0]
# pixelSize = ext[3],ext[4]
#
# # print('\nExtent:', extent)
# # print('\nDimensions:(x,y)', dimensions)
# # print('\nOrigion:', origin)
# # print('\npixel Size:(x,y)', pixelSize)
#
# bandInfo = bandStats(raster)
# print('\nCompression')
# # for b in bandInfo:
# #     print('BAND', bandInfo.index(b) + 1, "[ STATS ] =  Minimum=%.3f, Maximum=%.3f, Mean=%.3f, StdDev=%.3f" % ( \
# #         b[0], b[1], b[2], b[3]))
