'''
提供GeoJson 和 shpfile 相互转换的方法
'''
from osgeo import gdal, ogr, osr
import json
import os

# 受postgis影响，重新设置环境变量
# os.environ['CPL_ZIP_ENCODING'] = 'UTF-8'
os.environ['PROJ_LIB'] = r'C:\software\anaconda\envs\py37\Lib\site-packages\osgeo\data\proj'


# os.environ['GDAL_DATA'] = r'D:\anaconda3\envs\pytorch_GPU\Library\share'

def shp2geojson(shp_path, geojson_outpath):
    ds = ogr.Open(shp_path)
    geojson = ogr.GetDriverByName("GeoJSON")
    geojson.CopyDataSource(ds, geojson_outpath)


# geojson 转 shapefile
def geojson2shp(geojson, shp_path):
    # gdal.SetConfigOption("GDAL_FILENAME_IS_UTF8", "")
    gdal.SetConfigOption("SHAPE_ENCODING", "GBK")
    geoj_driver = ogr.GetDriverByName("GeoJSON")
    g_ds = geoj_driver.Open(geojson)
    dv = ogr.GetDriverByName("ESRI Shapefile")
    dv.CopyDataSource(g_ds, shp_path)




if __name__ == "__main__":
    shp_path = r"D:\work\通用水模型\数据清洗\训练\20221123新增样本\新增负样本\shp\221123新增负样本.shp"
    geojson_outpath = r"D:\work\通用水模型\数据清洗\训练\20221123新增样本\新增负样本\shp\221123新增负样本.json"
    # shp2geojson(shp_path, geojson_outpath)
    geojson2shp(geojson_outpath, shp_path)
