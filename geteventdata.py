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
#第几个地震
#i= 11





def geteventdata(number, station_latitude, station_longitude, network, station, channels):
    global event_time
    # 替换为地震目录 Excel 文件路径
    excel_file = '/home/sun_shuang/Documents/Selected_Data/local.xlsx'
    global event_time
    df1 = pd.read_excel(excel_file)
    row = df1.iloc[number-1]  # 第几个地震如果是第一个则数字是0
    mag = row.iloc[0]
    # print(mag)
    event_latitude = row.iloc[3]
    # print(event_latitude)
    event_longitude = row.iloc[2]
    # print(event_longitude)
    event_depth = row.iloc[4]
    # print(event_depth)
    time_str = row.iloc[5]
    filenames = row.iloc[1]
    if "UTC" in time_str:
        time_str = time_str.replace("UTC", "").strip()

        event_time = UTCDateTime(time_str)
        print(event_time)

    distance = locations2degrees(event_latitude, event_longitude,
                                 station_latitude, station_longitude)
    # print(distance)
    # 计算 P 波到时
    model = TauPyModel(model="iasp91")
    arrivals = model.get_travel_times(source_depth_in_km=event_depth,
                                      distance_in_degree=distance,
                                      phase_list=["P"])
    p_arrival = arrivals[0].time if arrivals else None
    if p_arrival:
        print(p_arrival)
        t0 = event_time + p_arrival - 5 * 60  # P波到时前 5 分钟
        t1 = event_time + p_arrival + 20 * 60

        datelist = pd.date_range(t0.datetime, t1.datetime)
        pbar = tqdm(datelist)
        # 指定将数据保存的文件夹
        save_folder = f"/work/sun_shuang/localdata1/{filenames}"
        if not os.path.exists(save_folder):
            # 如果文件夹不存在，则创建它
            os.makedirs(save_folder)
            print(f"文件夹 {save_folder} 被创建。")
        st = Stream()
        data_fetched = False  # 标记是否成功获取了数据
        for day in pbar:
            # today = f"{day}".replace(" ", "T").replace(":", ".")
            ts_str = event_time.strftime("%Y-%m-%dT%H.%M.%S")
            fn = os.path.join(save_folder, f"{network}.{station}.{ts_str}")
            

            if os.path.exists(fn):
                continue
            else:
                for channel in channels:
                    try:
                        tr = c.get_waveforms(network, station, "", channel, t0, t1)
                        st += tr
                        data_fetched = True  # 成功获取数据，更新标记
                    except FDSNNoDataException as e:
                        log_message = f"No data for station: {network}.{station}.{channel} at {event_time}\n"
                        write_to_log(log_message)
                        #print("No data on FDSN server for %s" % fn)
                        #pbar.set_description("No data on FDSN server for %s" % fn)
                        continue
            if data_fetched:
                st.write(f"{fn}.mseed", format="mseed", encoding='STEIM2')
            else:
                print(f"No data fetched for Stream, skipping writing to {fn}.mseed")


def write_to_log(message):
    """将消息写入日志文件"""
    with open(log_file_path, "a") as log_file:
        log_file.write(message)

# 定义全局日志文件路径

excel_path = '/home/sun_shuang/Documents/Selected_Data/stations.xlsx'  # 替换成台站 Excel 文件路径

df = pd.read_excel(excel_path)
for i in range(50,75):
    log_file_path = f'/home/sun_shuang/Documents/downloaderrors/{i}.log'
    for index, row in df.iterrows():
        network = row.iloc[0]  # 替换成你的实际网络列名
        station = row.iloc[1]  # 替换成你的实际台站列名
        channels = [row.iloc[4], row.iloc[5], row.iloc[6],  row.iloc[7]]
        '''
        channelP = row.iloc[4]  # 替换成你的实际通道列名，并根据分隔符分割通道名称
        channel1 = row.iloc[5]
        channel2 = row.iloc[6]
        channelZ = row.iloc[7]
        '''
        station_latitude = row.iloc[2]
        station_longitude = row.iloc[3]
        geteventdata(i, station_latitude, station_longitude, network, station, channels)





