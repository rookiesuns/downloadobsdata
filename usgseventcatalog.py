import requests
from obspy import UTCDateTime
import pandas as pd
from geopy.distance import geodesic


def calculate_distance(lat1, lon1, lat2, lon2):
    # 异常值检查

    coords_1 = (lat1, lon1)
    coords_2 = (lat2, lon2)
    return geodesic(coords_1, coords_2).kilometers



def get_usgs_earthquake_data(start_time, end_time, min_magnitude):
    base_url = "https://earthquake.usgs.gov/fdsnws/event/1/query"

    params = {
        "format": "geojson",
        "starttime": start_time,
        "endtime": end_time,
        "minmagnitude": min_magnitude,
        "orderby": "time"
    }

    response = requests.get(base_url, params=params)

    if response.status_code == 200:
        data = response.json()
        return data.get('features', [])  # 使用 get 避免键不存在的问题
    else:
        print(f"Error: Unable to fetch data. Status code: {response.status_code}")
        return []


def filter_and_save_earthquakes(earthquakes, reference_latitude, reference_longitude):
    columns = ["Magnitude", "Name", "Longitude", "Latitude", "Depth (km)", "Time", "Distance (km)"]
    result_df_near = pd.DataFrame(columns=columns)
    result_df_far = pd.DataFrame(columns=columns)

    for earthquake in earthquakes:
        mag = earthquake['properties']['mag']
        name = earthquake['properties']['place']  # 提取地震名称
        coordinates = earthquake['geometry']['coordinates']
        longitude, latitude, depth = coordinates
        time = UTCDateTime(earthquake['properties']['time'] / 1000.0).strftime('%Y-%m-%d %H:%M:%S UTC')
        distance = calculate_distance(reference_latitude, reference_longitude, latitude, longitude)
        entry = pd.Series([mag, name, longitude, latitude, depth, time, distance], index=columns)

        # 进行距离和震级的筛选
        if distance < 3000 and mag > 3:
            result_df_near = pd.concat([result_df_near, entry.to_frame().T], ignore_index=True)
        if distance > 3400 and mag > 5:
            result_df_far = pd.concat([result_df_far, entry.to_frame().T], ignore_index=True)

    return result_df_near, result_df_far
'''
        if distance < 3000 and mag > 3:
            result_df_near = pd.concat([result_df_near, entry], ignore_index=True)

        if distance > 3400 and mag > 5:
            result_df_far = pd.concat([result_df_far, entry], ignore_index=True)
'''


# 指定时间范围和最小震级
start_time = "2011-11-30T00:00:00"
end_time = "2012-05-30T00:00:00"
min_magnitude = 3.0

# 指定参考地震台站的经纬度
reference_latitude = 46.520901
reference_longitude = -127.9049

# 获取地震事件
earthquakes = get_usgs_earthquake_data(start_time, end_time, min_magnitude)

# 检查地震数据是否为空
if earthquakes:
    # 过滤并保存到Excel表格
    result_df_near, result_df_far = filter_and_save_earthquakes(earthquakes, reference_latitude, reference_longitude)

    # 保存到Excel表格
    result_df_near.to_excel("near_earthquakes1.xlsx", index=False)
    result_df_far.to_excel("far_earthquakes1.xlsx", index=False)
else:
    print("No earthquake data available.")

