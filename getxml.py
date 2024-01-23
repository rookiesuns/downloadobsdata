from obspy import read, UTCDateTime
from obspy.clients.fdsn import Client
from obspy.clients.fdsn.client import FDSNNoDataException
import os
from tqdm import tqdm
import pandas as pd
from obspy.taup import TauPyModel
from obspy.geodetics import locations2degrees
import datetime
import traceback
from obspy import Stream

# data provider
c = Client("IRIS")
# 定义全局日志文件路径


save_folder = r'D:\pythonProject\stationxml'
def geteventdata(network, station, channels):

            # today = f"{day}".replace(" ", "T").replace(":", ".")


        for channel in channels:
            fr = os.path.join(save_folder, f"RESP.{network}.{station}.{channel}")
            resp = c.get_stations(network=network, station=station, channel=channel, level="response")

            resp.write(f"{fr}.xml", format="stationxml")

                    #print(f"No data fetched for Stream, skipping writing to {fn}.mseed")

'''
def write_to_log(message):
    """将消息写入日志文件"""
    with open(log_file_path, "a") as log_file:
        log_file.write(message)
'''
'''
excel_path = r'D:\pythonProject\obsgetdata1\stations.xlsx'  # 替换成台站 Excel 文件路径
df = pd.read_excel(excel_path)
for index, row in df.iterrows():
    network = row.iloc[0]  # 替换成你的实际网络列名
    station = row.iloc[1]  # 替换成你的实际台站列名
    
    channels = [row.iloc[4], row.iloc[5], row.iloc[6],  row.iloc[7]]
    
    #channelP = row.iloc[4]  # 替换成你的实际通道列名，并根据分隔符分割通道名称
    #channel1 = row.iloc[5]
    #channel2 = row.iloc[6]
    #channelZ = row.iloc[7]
    
    station_latitude = row.iloc[2]
    station_longitude = row.iloc[3]
    geteventdata(network, station, channels)
'''
network = '7D'  # 替换成你的实际网络列名
station = 'M08A'  # 替换成你的实际台站列名

channels = ['BDH', 'BH1', 'BH2', 'BHZ']
geteventdata(network, station, channels)