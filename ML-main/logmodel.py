import pandas as pd
import pickle
df = pd.read_csv('sample_data.csv')



# Transform ARR_DELAY into a 1/0 format for Delay/No Delay
df['ARR_DELAY'] = df['ARR_DELAY'].apply(lambda x:1 if x>=5 else 0)

df = pd.concat([df,pd.get_dummies(df['UNIQUE_CARRIER'],drop_first=True,prefix="UNIQUE_CARRIER")],axis=1)
df = pd.concat([df,pd.get_dummies(df['ORIGIN'],drop_first=True,prefix="ORIGIN")],axis=1)
df = pd.concat([df,pd.get_dummies(df['DEST'],drop_first=True,prefix="DEST")],axis=1)
df = pd.concat([df,pd.get_dummies(df['DAY_OF_WEEK'],drop_first=True,prefix="DAY_OF_WEEK")],axis=1)
df = pd.concat([df,pd.get_dummies(df['DEP_HOUR'],drop_first=True,prefix="DEP_HOUR")],axis=1)
df.drop(['ORIGIN','DEST','UNIQUE_CARRIER','DAY_OF_WEEK','DEP_HOUR'],axis=1,inplace=True)

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(df.drop('ARR_DELAY',axis=1),df['ARR_DELAY'], test_size=0.30)

from sklearn.linear_model import LogisticRegression
#Train the model
logmodel = LogisticRegression()
logmodel.fit(X_train,y_train)

#Predicting on the Test Set
predictions = logmodel.predict(X_test)



with open('logmodel.pkl', 'wb') as fid:
    pickle.dump(logmodel, fid,2)

#Create a Dataframe with only the dummy variables
cat = df.drop('ARR_DELAY',axis=1)
index_dict = dict(zip(cat.columns,range(cat.shape[1])))

with open('cat', 'wb') as fid:
    pickle.dump(index_dict, fid,2) 