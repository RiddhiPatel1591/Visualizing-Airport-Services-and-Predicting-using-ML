#!/usr/bin/env python
# coding: utf-8

# In[2]:


get_ipython().system('curl https://topcs.blob.core.windows.net/public/FlightData.csv -o flightdata.csv')


# In[5]:


#read the flight data and explore it using pandas. 
import pandas as pd
import pickle
df = pd.read_csv('flightdata.csv')
df.head()


# # Clean and Prepare Data

# In[6]:


df.shape


# In[7]:


#rows 11231 and columns 26
df.columns


# In[8]:


df.isnull().values.any() #True indicates that there is at least one missing value somewhere in the dataset.


# In[9]:


df.isnull().sum() #Checking where the missing value is.


# In[10]:


#drop the column
df =df.drop('Unnamed: 25',  axis=1)
df.isnull().sum()


# In[ ]:


#The model you are building , To predict whether a flight you are booking is likely to arrive on time
#So the columns which are not in use eliminate that columns 


# In[12]:


#separate the columns which are required 
r_df = df[["MONTH" , "DAY_OF_MONTH" , "DAY_OF_WEEK" , "ORIGIN" , "DEST" ,"CRS_DEP_TIME" , "ARR_DEL15"]]
r_df.isnull().sum()


# In[14]:


r_df[r_df.isnull().values.any(axis = 1)].head()


# In[18]:


#NAN inidciated missing values in ARR_DEL15 , the reason these rows are missing is that they all were diverted or canceled  will use fillna method to replace Nan with 1
r_df = r_df.fillna({"ARR_DEL15" : 1})
r_df.iloc[177:185]


# In[20]:


# Bin the departure times of CRS_DEP_TIME bcoz it contians time in military seconds
r_df.head()


# In[35]:


import math 
for index, row in r_df.iterrows():
    r_df.loc[index, 'CRS_DEP_TIME'] = math.floor(row['CRS_DEP_TIME']/100)


# In[37]:


r_df.head()


# In[32]:


r_df=pd.get_dummies(r_df, columns=['ORIGIN' , 'DEST'])
r_df.head()#0 OR 1 REPRESENT WHETHER THE FLIGHTS WERE departed or diverted


# # Build Machine Learning Model

# In[ ]:


#To create a machine learning model you need two datasets one for training and one for testing in practice you often  have only one dataset 
#so you split in the two we have used 80-20 split ,
#Will also separate Dataframe into features columns and labels columns 
#The former will contain Flights origin , Flights destination , Scheduled departure time 
#The latter will contains the columns  that the models has to predictARR_DEL15 this indicates whether the flight arrive on time or not 


# In[38]:


from sklearn.model_selection import train_test_split
train_x, test_x, train_y, test_y  = train_test_split(r_df.drop('ARR_DEL15' , axis=1),r_df['ARR_DEL15'], test_size=0.2, random_state=42)


# In[40]:


print(train_x.shape)
print(test_x.shape)


# In[ ]:


#This is a Binary Classification Model that predicts whether a flight will arrive on time or late


# In[41]:


print(train_y.shape)
print(test_y.shape)


# In[ ]:


#Training the model


# In[42]:


from sklearn.ensemble import RandomForestClassifier

classifier = RandomForestClassifier(random_state=13)
classifier.fit(train_x , train_y)


# Saving model to disk
pickle.dump(classifier, open('FlightDelay.pkl','wb'))

# Loading model to compare the results
flightdelay = pickle.load(open('FlightDelay.pkl','rb'))
print(flightdelay.predict(test_x))































