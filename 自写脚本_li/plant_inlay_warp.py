# -*- coding: utf-8 -*-
"""
Created on Tue Apr  5 20:18:49 2022

@author: 陨星落云
"""
import os
from osgeo import gdal
os.environ['PROJ_LIB'] = r'C:\software\anaconda\envs\py37\Lib\site-packages\osgeo\data\proj'
def inlay(inpath,outpath):

    file_path = []
    for file in os.listdir(path):
        file_path.append(os.path.join(path,file))

    vrtfile = gdal.BuildVRT(file_path[0], file_path)
    dsT3 = gdal.Warp(outpath , #文件的输出路径及文件名
                     vrtfile,  # 拼接好的影像（待裁剪）
                     format='GTiff', # 输出影像的格式
                     dstSRS='EPSG:4326', # 参考：WGS84
                     cropToCutline=True, # 将目标图像的范围指定为cutline 矢量图像的范围。
                     dstNodata=0, # 目标图像无值时填充值
                     outputType=gdal.GDT_Byte)


if __name__ == "__main__":
    path = r"E:\工作相关\中科云遥\工作\通用水模型\影像下载\鸽子卫星\批处理_脚本测试\测试数据"
    outpath=r"E:\工作相关\中科云遥\工作\通用水模型\影像下载\鸽子卫星\批处理_脚本测试\测试结果\test.tif"
    inlay(path,outpath)