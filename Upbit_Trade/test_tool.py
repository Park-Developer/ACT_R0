import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

def draw_plot(x,y):
    fig, ax = plt.subplots()
    ax.plot(x, y)
    plt.show()

def save_csvFile(data_list:dict):
    data_df = pd.DataFrame(data_list)
    data_df.to_csv('test.csv', index=False)

def read_csvFile(csvfile):
    data=pd.read_csv(csvfile)
    return data

if __name__=="__main__":
    print(read_csvFile("./test.csv"))