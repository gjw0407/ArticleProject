import pandas as pd
import os

# read recent file in python : https://frhyme.github.io/python-libs/python_read_recent_file_in_python/

print(os.getcwd())
files_Path = os.getcwd() + "\\article\\" # 파일들이 들어있는 폴더
file_name_and_time_lst = []

print(files_Path)

for f_name in os.listdir(f"{files_Path}"):
    written_time = os.path.getctime(f"{files_Path}{f_name}")
    file_name_and_time_lst.append((f_name, written_time))

sorted_file_lst = sorted(file_name_and_time_lst, key=lambda x: x[1], reverse=True)

recent_file = sorted_file_lst[0]
recent_file_name = recent_file[0]
df = pd.read_pickle(files_Path+recent_file_name)

print(df)
