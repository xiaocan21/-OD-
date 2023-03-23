import pandas as pd
import numpy as np

# 读取数据
data = pd.read_csv('F:/railway_datasets/Metro_train1/2019-01-01B.csv', parse_dates=[0,5])

# 将时间按小时取整
data['time'] = data['time'].dt.floor('H')
data['time1'] = data['time1'].dt.floor('H')

# 将数据按小时分组，并统计每小时内每个OD对的人数
hourly_od = pd.DataFrame({'count' : data.groupby(['time', 'stationID', 'stationID1']).size()}).reset_index()

# 获取所有站点的编号
all_stations = np.union1d(hourly_od['stationID'].unique(), hourly_od['stationID1'].unique())

# 生成空的OD矩阵
od_matrix = pd.DataFrame(0, index=all_stations, columns=all_stations)

# 将每小时内每个OD对的人数填充到OD矩阵中
for _, row in hourly_od.iterrows():
    hour = row['time']
    start_station = row['stationID']
    end_station = row['stationID1']
    count = row['count']
    od_matrix.loc[start_station, end_station] += count

# 打印OD矩阵
print(od_matrix)
#od_matrix.to_csv(path_or_buf='F:/railway_datasets/Metro_train1/OD.csv', index=False)
#生成每个小时的OD矩阵
od_matrices = {}

# 将每个小时内每个OD对的人数填充到对应的OD矩阵中
for _, row in hourly_od.iterrows():
    hour = row['time']
    start_station = row['stationID']
    end_station = row['stationID1']
    count = row['count']
    
    # 如果该小时的OD矩阵不存在，则创建一个新的OD矩阵
    if hour not in od_matrices:
        od_matrices[hour] = pd.DataFrame(0, index=all_stations, columns=all_stations)
    
    # 将该OD对的人数填充到对应的OD矩阵中
    od_matrices[hour].loc[start_station, end_station] += count

# 将每个小时的OD矩阵保存到不同的excel工作表中
with pd.ExcelWriter('od_matrices.xlsx') as writer:
    for hour in od_matrices:
        od_matrix = od_matrices[hour]
        sheet_name = f'{hour.hour:02d}'
        od_matrix.to_excel(writer, sheet_name=sheet_name)
