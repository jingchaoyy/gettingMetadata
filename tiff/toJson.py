"""
Created on 4/30/18

@author: YJccccc
"""
from osgeo import gdal
import tiff.tiffMeta as tifInfo
import json
import os

def tojson(path, filename):
    # filepath = r"/Users/YJccccc/Desktop/DonglianSun_Project/SNPP_VIIRS_375m_floodmap_1826_Sep01_2017_Geographic_geotiff/SNPP_VIIRS_375m_floodmap_1826_Sep01_2017_Geographic.tif"
    filepath = path+filename
    print(filename)

    # Open the file:
    raster = gdal.Open(filepath)

    meta = raster.GetMetadata()
    print('Basic Info:', meta)

    ext = tifInfo.GetExtent(raster)
    dimensions = ext[0], ext[1]
    extent = ext[2]
    box = extent[1][0], extent[1][1], extent[3][0], extent[3][1]
    origin = ext[2][0]
    pixelSize = ext[3], ext[4]

    print('\nExtent:', box)
    print('\nDimensions:(x,y)', dimensions)
    print('\nOrigion:', origin)
    print('\npixel Size:(x,y)', pixelSize)

    bandInfo = tifInfo.bandStats(raster)
    print('\nCompression')
    for b in bandInfo:
        print('BAND', bandInfo.index(b) + 1, "[ STATS ] =  Minimum=%.3f, Maximum=%.3f, Mean=%.3f, StdDev=%.3f" % ( \
            b[0], b[1], b[2], b[3]))

    # adding attributes to directory followed by description
    commands = {}
    commands["File_Name"] = filename.split(".")[0]
    commands["id"] = "123456"
    commands["boxes"] = [" ".join(str(x) for x in box)]
    commands["origin"] = [" ".join(str(x) for x in origin)]
    commands["Pixel_Size"] = [" ".join(str(x) for x in pixelSize)]
    commands["Dimensions"] = [" ".join(str(x) for x in dimensions)]

    # open a json file and write
    with open(
                            "/Users/YJccccc/Desktop/DonglianSun_Project/jsonTest/" + filename.split(".")[0] + ".json",
            'w') as outfile:
        js = json.dumps(commands, indent=2, sort_keys=True)
        outfile.write(js)


if __name__ == "__main__":
    path = "/Users/YJccccc/Desktop/DonglianSun_Project/SNPP_VIIRS_375m_floodmap_1826_Sep01_2017_Geographic_geotiff/"
    files = os.listdir(path)
    print (files)
    for file in files:
        if file.endswith(".tif"):
            print (path+file)
            tojson(path, file)
        else:
            print('not tif')