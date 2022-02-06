import pandas as pd
import os

cur_file_path = os.path.dirname(__file__)
target_file_path = os.path.join(cur_file_path, "../URL/url.csv")


def read_csv():
    print("Reading URL.csv File")

    if os.path.exists(target_file_path):
        try:
            df = pd.read_csv(target_file_path, header=None, index_col=False)
            print("Reading csv File Successful")
            print("Example URL: " + str(df.iloc[0]))

        except BaseException as e:
            print("Error Occurred: {}".format(e))

        return df.values.tolist()

    else:
        print("File Not Found", target_file_path)
        exit(-1)

