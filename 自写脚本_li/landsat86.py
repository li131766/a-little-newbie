import os
from osgeo import gdal
import numpy as np
os.environ['PROJ_LIB'] = r'C:\software\anaconda\envs\py37\Lib\site-packages\osgeo\data\proj'
file_path = r'E:\工作相关\中科云遥\工作\通用水模型\影像下载\landsat\测试\LC09_L2SP_122044_20220404_20220406_02_T1'
band1_fn = ""  # red band
band2_fn = ""  # green band
band3_fn = ""  # blue band
for filename in os.listdir(file_path):
    if 'B4' in filename:
        band1_fn =os.path.join(file_path,filename)
    elif 'B3' in filename:
        band2_fn = os.path.join(file_path, filename)
    elif 'B2' in filename:
        band3_fn = os.path.join(file_path, filename)

# 读取第一个tif
in_ds = gdal.Open(band1_fn)
in_band = in_ds.GetRasterBand(1)

# 创建输出tif数据集
gtiff_driver = gdal.GetDriverByName('GTiff')
out_ds = gtiff_driver.Create(r'E:\工作相关\中科云遥\工作\通用水模型\影像下载\landsat\测试\test\true_color.tiff', in_band.XSize, in_band.YSize, 3,
                             in_band.DataType)

# 将投影坐标与仿射矩阵写入
out_ds.SetProjection(in_ds.GetProjection())
out_ds.SetGeoTransform(in_ds.GetGeoTransform())

# 将波段内图像转为数组
in_data = in_band.ReadAsArray()

# 将第一个tif参数与波段参数写入 真彩色tif数据集
out_band = out_ds.GetRasterBand(1)
out_band.WriteArray(in_data)

# 读取第二个tif
in_ds = gdal.Open(band2_fn)
out_band = out_ds.GetRasterBand(2)
out_band.WriteArray(in_ds.ReadAsArray())

# 读取第三个tif
out_ds.GetRasterBand(3).WriteArray(gdal.Open(band3_fn).ReadAsArray())

# save
out_ds.FlushCache()

for i in range(1, 4):
    out_ds.GetRasterBand(i).ComputeStatistics(False)

out_ds.BuildOverviews('average', [2, 4, 8, 16, 32])
# del memory
del out_ds
