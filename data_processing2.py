# 找到最可能的标签
import os
import pandas as pd
import csv
from collections import Counter

path = 'data/B_test'
for root,dirs,files in os.walk(path):
    flags = [ [] for i in range(len(files)) ]
    for i, file in enumerate(files):
        print(i, os.path.join(root, file))
        file_p = os.path.join(root, file)
        data = pd.read_csv(file_p, encoding='gb2312')
        flags[i] = data[data['label']==1]['id'].values.tolist()
        print(len(flags[i]))

res = []
# for v in flags[0]:
#     i = 0
#     for i in range(len(flags)):
#         if v not in flags[i]:
#             break
#     if i == len(flags)-1:
#         res.append(v)


def vote():
    for i in range(len(flags)):
        res.extend(flags[i])

    count = Counter(res)
    data['label'] = 0
    for k,v in count.items():
        if v >= len(flags)//2:
            print(k)
            data.loc[data['id'] == k, 'label'] = 1

    data.to_csv('sumbit_vote.csv', index=0)


def sum_data():
    for i in range(len(flags)):
        for k in flags[i]:
            if k not in res:
                res.extend(flags[i])
                break
    count = Counter(res)
    print("len of res: ", len(set(res)))

    # res_list = list(set(res))
    # res_list.sort()
    # for i in res_list:
    #     print(i)
    print(" labels count in res: ")
    print(count)
    test_file = pd.read_csv('B_testdataset/Result.csv')
    res_dan = pd.read_csv('B_testdataset/Result_dangan.csv')
    data = pd.merge(res_dan[['id','fangcha','jiaquan']], test_file, on='id', how='right')
    data['pred'] = 0
    data['label'] = 0
    for k,v in count.items():
        if v > 1:
            # print(k)
            data.loc[data['id'] == k, 'label'] = 1

    data.loc[data['id'].isin(set(res)),'pred'] = 1
    # data.to_csv('B_testdataset/Result_ans.csv', index=0)
    sum_csv = data[['id','label']]
    sum_csv.to_csv('B_testdataset/submit_test.csv', index=0)




def choose_data():
    potential = [179418058, 179458306, 855996491, 1606708811, 1912367373, 2071313507, 2323237963, 2347718608, 2238809293,
                 2496032641, 2427050072, 2717225077, 2759232590, 179569820, 179433516, 2852503463, 2172970175, 2186749200,
                 2212416005, 2251440776, 2256064355, 2319973783, 2347718610, 2445049876, 2523401557, 2540517219, 2576321385,
                 2602819207, 2759317616, 2825175309]
    # test_file = pd.read_csv('test_dataset/Result3_.csv')
    # test_file['label'] = 0
    # test_file.loc[test_file['ID'].isin(potential),'label'] = 1
    # test_file.to_csv('test_dataset/Result3_.csv', index=0)
    sum_csv = pd.read_csv('sumbit_test.csv')
    sum_csv['label'] = 0
    sum_csv.loc[sum_csv['id'].isin(potential),'label'] = 1
    sum_csv.to_csv('sumbit_test.csv', index=0)




def sum_data_A():
    for i in range(len(flags)):
        for k in flags[i]:
            if k not in res:
                res.extend(flags[i])
                break
    count = Counter(res)
    print("len of res: ", len(set(res)))

    # res_list = list(set(res))
    # res_list.sort()
    # for i in res_list:
    #     print(i)
    print(" labels count in res: ")
    print(count)
    test_file = pd.read_csv('test_dataset/Result3_.csv')
    test_file['pred'] = 0
    # sum_csv = pd.read_csv('sumbit_test.csv')
    # sum_csv['label'] = 0
    # for k,v in count.items():
    #     print(k)
    #     test_file.loc[test_file['id'] == k, 'pred'] = 1

    test_file.loc[test_file['ID'].isin(set(res)),'pred'] = 1
    # sum_csv.to_csv('submit_test.csv', index=0)

    test_file.to_csv('test_dataset/Result3_.csv', index=0)




if __name__ == '__main__':
    sum_data()