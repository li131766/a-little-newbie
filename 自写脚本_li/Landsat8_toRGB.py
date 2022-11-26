from osgeo import gdal, osr
import os
import numpy
from tqdm import tqdm

# 受 proj影响，增加环境变量
os.environ['PROJ_LIB'] = r'C:\software\anaconda\envs\py37\Lib\site-packages\osgeo\data\proj'


def landsat8_toRGB(file_path, out_path):
    # 筛选出 landsat 文件中，属于RGB的波段，分别为 波段4：红  波段3：绿   波段2：蓝
    for filename in os.listdir(file_path):
        if 'B4' in filename:
            band4 = os.path.join(file_path, filename)
        elif 'B3' in filename:
            band3 = os.path.join(file_path, filename)
        elif 'B2' in filename:
            band2 = os.path.join(file_path, filename)

    bands = [band4, band3, band2]

    create = True
    for i, b in enumerate(tqdm(bands, desc="合并RGB波段")):
        in_ds = gdal.Open(b)
        if create:
            dr = gdal.GetDriverByName('GTiff')
            out_filepath = os.path.join(out_path, file_path.split("\\")[-1] + ".tiff")  # todo 用os的分割功能，避免linux不通用
            temp_band = in_ds.GetRasterBand(1)
            out_ds = dr.Create(out_filepath, in_ds.RasterXSize, in_ds.RasterYSize, 3, temp_band.DataType)
            del temp_band
            out_ds.SetProjection(in_ds.GetProjection())
            out_ds.SetGeoTransform(in_ds.GetGeoTransform())
            create = False
        in_data = in_ds.ReadAsArray()
        out_band = out_ds.GetRasterBand(i + 1)
        out_band.WriteArray(in_data)
        in_ds = None
    out_ds = None

    # 将投影坐标转换为 GCS_WGC_1984 地理坐标系
    print("重投影...")
    dataset = gdal.Open(out_filepath, gdal.GA_Update)
    dstSRS = osr.SpatialReference()
    # dstSRS = 'EPSG:4326'GeoTransform
    dstSRS.ImportFromEPSG(4326)
    out_filepath_proj = os.path.join(out_path, file_path.split("\\")[-1] + "_GCS.tiff")
    gdal.Warp(out_filepath_proj, dataset, format='GTiff',
              dstSRS=dstSRS, resampleAlg=gdal.GRIORA_Bilinear,
              transformerOptions='GMTED2km.tif')
    dataset = None


if __name__ == "__main__":
    path = r'D:\work\通用水模型\数据清洗\预测\大图\补充大图\有河道'
    out_path = r"D:\work\通用水模型\数据清洗\预测\大图\补充大图\多源预测图"
    landsat8_toRGB(path, out_path)
