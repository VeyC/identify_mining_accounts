import pandas as pd
from sklearn.metrics import roc_auc_score,accuracy_score,f1_score
from xgboost import XGBClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.model_selection import train_test_split,StratifiedKFold
from lightgbm import LGBMClassifier
import numpy as np
from collections import Counter
import csv
# 加载数据集
np.random.seed(33)
train_data = pd.read_csv('training_dataset/Result_month.csv')
pred_data = pd.read_csv('test_dataset/Result_month.csv')
train = train_data.iloc[:,:-1]
label = train_data.iloc[:,-1]
train=train.drop(['ID'],axis=1)
x_train = np.array(train)
y_train = np.array(label)
ids = pred_data['ID'].values.tolist()
pred_data=pred_data.drop(['ID'],axis=1)
x_test = np.array(pred_data)
clfs=[
XGBClassifier(booster='gblinear',learning_rate=0.1,n_estimators=40, num_class=2,max_depth=50,
              min_child_weight = 1, gamma=0.3,objective='multi:softmax', random_state=33 ),
XGBClassifier(learning_rate=0.1,n_estimators=20, num_class=2,max_depth=40,
              min_child_weight = 1, gamma=0.3,objective='multi:softmax', random_state=33 ),
RandomForestClassifier(n_estimators=5,max_depth=50, n_jobs=-1,
                       criterion='gini',random_state=33),
RandomForestClassifier(n_estimators=5,max_depth=20, n_jobs=-1,
                       criterion='entropy',random_state=33),
LGBMClassifier(boosting_type='gbdt', objective='binary', num_leaves=70,
                   learning_rate=0.1, n_estimators=50, max_depth=60,
                   bagging_fraction=0.9, feature_fraction=0.9, reg_lambda=0.90, random_state=33),
LGBMClassifier(boosting_type='dart', objective='binary', num_leaves=70,
                                learning_rate=0.1, n_estimators=30, max_depth=60,
                                bagging_fraction=0.9, feature_fraction=0.8, reg_lambda=0.10,random_state=33)
]
pred_result= np.zeros((x_test.shape[0], len(clfs)))
for j,clf in enumerate(clfs):
    clf.fit(x_train,y_train)
    y_pred = clf.predict(x_test)
    pred_result[:,j]=y_pred
result=[]
for i in pred_result:
    count_0=i.tolist().count(0)
    count_1=i.tolist().count(1)
    if count_1>count_0:
        result.append(1)
    else:
        result.append(0)
print(Counter(result))
res = [["id","label"]]
for i in range(len(ids)):
    res.append([ids[i], result[i]])
with open('sumbit_month.csv', 'w', newline='') as t:  # numline是来控制空的行数的
    writer = csv.writer(t)  # 这一步是创建一个csv的写入器
    writer.writerows(res)