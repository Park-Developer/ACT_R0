def calc_avg(data_list:list):
    sum=0

    for data in data_list:
        sum+=float(data)

    avg=sum/len(data_list)
    return int(avg)

if __name__=="__main__":
    pass