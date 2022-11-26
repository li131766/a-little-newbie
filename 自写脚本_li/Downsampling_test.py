'''————尝试编写一个影像重采样的脚本————'''

from osgeo import gdal
import os
import tqdm
os.environ['PROJ_LIB'] = r'C:\software\anaconda\envs\py37\Lib\site-packages\osgeo\data\proj'

def resampling(input_path, out_path , multiple=0.5):
    in_ds = gdal.Open(input_path)             # 打开tif数据
    in_band = in_ds.GetRasterBand(1)          #获取波段
    xsize = in_band.XSize                     # 获取行数
    ysize = in_band.YSize                     # 获取列数
    new_x = xsize / multiple                  # 定义重采样后的行数
    new_y = ysize / multiple                  # 定义重采样后的列数
    transform =list(in_ds.GetGeoTransform())       # 获取反射矩阵信息

    transform[1]= transform[1] * multiple
    transform[5]= transform[5] * multiple

    driver = in_ds.GetDriver()
    out_tif = driver.Create(os.path.join(out_path,"resampling.tif"),
                                         int(new_x),int(new_y),3,in_band.DataType)

    out_tif.SetProjection(in_ds.GetProjection())    #设置投影信息
    out_tif.SetGeoTransform(transform)                 #写入仿射矩阵
    for i  in  tqdm.tqdm(range(1,4)):
        in_band = in_ds.GetRasterBand(i)
        data = in_band.ReadAsArray(buf_xsize= int(xsize/multiple),buf_ysize=int(ysize/multiple))        #设置更大的缓冲读取影像
        out_band = out_tif.GetRasterBand(i)
        out_band.WriteArray(data)
        print('写入波段')
    print('重采样成功')



in_path = r"E:\工作相关\中科云遥\工作\影像\广东水利厅6月一期影像\10_idx_431802_95698_19.tif"
out_path =r"E:\工作相关\中科云遥\工作\影像\新建文件夹"
resampling(in_path, out_path, multiple=13)

