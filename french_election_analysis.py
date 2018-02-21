
import numpy as np
import pandas as pd
pd.options.mode.chained_assignment = None  # default='warn'
import sqlite3

#get_ipython().magic('matplotlib inline')

import matplotlib
import matplotlib.pyplot as plt
plt.rcParams["figure.figsize"] = (16,10)
import seaborn as sns




list_files=["database_18_0.sqlite","database_18_1.sqlite",
            "database_18_2.sqlite","database_18_3.sqlite","database_17_1.sqlite",
            "database_17_2.sqlite","database_17_3.sqlite"]

list_df=[]
for file in list_files:
    print(file)
    connection = sqlite3.connect("/home/harshit/Videos/database/{}".format(file))
    df_tweet= pd.read_sql_query("SELECT * from data", connection)
    connection.close()
    
    
    df_tweet=df_tweet.loc[df_tweet['lang']=="fr"]
    list_df.append(df_tweet)

df_tweets=pd.concat(list_df,axis=0)
print(df_tweets.head())


# In[ ]:

# Plot the emtion of the candidates
candidates_tags={
    "Hamon":["@benoithamon","@AvecHamon2017","@partisocialiste"],
    "Le Pen":["@MLP_officiel","@FN_officiel"],
    "Macron":["@EmmanuelMacron","@enmarchefr"],
    "Mélenchon":["@JLMelenchon","@jlm_2017"],
    "Fillon":["@FrancoisFillon","@Fillon2017_fr","@lesRepublicains"]
}


# In[ ]:

count_candidate_call=[]
candidates_ticks=[]
for candidate in candidates_tags:
    candidates_ticks.append(candidate)
    count_candidate_call.append(df_tweets["mention_"+candidate].value_counts()[1])
df_mention=(pd.DataFrame(count_candidate_call,index=list(candidates_tags),columns=["Number_of_mentions"])).sort_values(["Number_of_mentions"],ascending=False)
print(df_mention)


# In[ ]:


#Make a graph for to see the repartition
fig, ax = plt.subplots(figsize=(12,12))
#Plot time (daily timestamp)
columns_namecandidate=["day","hour"]
for i,candidate in enumerate(candidates_tags):
    columns_namecandidate.append("mention_"+candidate)
print(columns_namecandidate)
ax.tick_params(axis='x', labelsize=15)
ax.tick_params(axis='y', labelsize=10)
ax.set_xlabel('Candidates', fontsize=15)
ax.set_ylabel('Number of tweets' , fontsize=15)
ax.set_title('Number of candidate mention', fontsize=15, fontweight='bold')
df_mention.plot(ax=ax, kind='bar', color='red')


# In[ ]:

#Plot time (daily timestamp)
columns_namecandidate=["day","hour"]
for i,candidate in enumerate(candidates_tags):
    columns_namecandidate.append("mention_"+candidate)
print(columns_namecandidate)


# In[ ]:



df_mentions=df_tweets[columns_namecandidate].copy()
df_mentions.head()
fig, ax = plt.subplots(figsize=(12,12))
ax.tick_params(axis='x', labelsize=15)
ax.tick_params(axis='y', labelsize=10)
ax.set_xlabel('Day', fontsize=15)
ax.set_ylabel('Number of tweets' , fontsize=15)
ax.set_title('Number of tweets by candidate by day', fontsize=15, fontweight='bold')
df_mentions_perday=df_mentions.groupby(["day"]).sum()
df_mentions_perday.plot(ax=ax, kind='bar',cmap=plt.get_cmap("gist_rainbow"))


# In[ ]:

#Use an heatmap approach to see who is mention with who
def inlist(elt,liste):
    try:
        liste.index(elt)
        return True
    except:
        return False


# In[ ]:

def test_mention(df,ref_candidate,dict_nomention):
    for candidate in dict_nomention:
        if inlist(candidate,ref_candidate):
            df=df.loc[df["mention_"+candidate]==1].copy()
        else:
            df=df.loc[df["mention_"+candidate]==0].copy()
    return df


# In[ ]:

list_mention_only_candidate=[]
for i,candidate in enumerate(candidates_tags):
    df_mentioncandidate=df_mentions.loc[df_mentions["mention_"+candidate]==1]
    nbr_mention=len(df_mentioncandidate)
    list_mention_whowho_candidate=[]
    df_onlycandidate=test_mention(df_mentioncandidate.copy(),[candidate],candidates_tags)
    
    list_mention_only_candidate.append(df_onlycandidate)
    
df_tot_onlycandidate=pd.concat(list_mention_only_candidate,axis=0)

print(df_tot_onlycandidate.head())
#Plot time


# In[ ]:

fig, ax = plt.subplots(figsize=(12,12))
ax.tick_params(axis='x', labelsize=15)
ax.tick_params(axis='y', labelsize=10)
ax.set_xlabel('Day', fontsize=15)
ax.set_ylabel('Number of tweets' , fontsize=15)
ax.set_title('Number of tweets by candidate by day', fontsize=15, fontweight='bold')
df_mentions_perday=df_tot_onlycandidate.groupby(["day"]).sum()
df_mentions_perday.plot(ax=ax, kind='bar',cmap=plt.get_cmap("gist_rainbow"))

_ = ax.set_xticklabels(df_mentions_perday.index,rotation=45)
    
    
        


# In[ ]:

df_mentions_perhour= df_tot_onlycandidate.groupby(['day','hour']).sum()
# df_counttweets=df_tot_onlycandidate.groupby(['day','hour']).size()
# df_counttweets.columns=["count_tweets"]
df_glob=pd.concat([df_mentions_perhour],axis=1)

print(df_glob.head())


# In[ ]:

fig, ax = plt.subplots(figsize=(12,12))
ax.tick_params(axis='x', labelsize=10)
ax.tick_params(axis='y', labelsize=10)
ax.set_xlabel('Date', fontsize=15)
ax.set_ylabel('Number of tweets' , fontsize=15)
ax.set_title('Number of tweets by candidate', fontsize=15, fontweight='bold')
df_rollingmean=df_glob.rolling(3,min_periods=1).mean()
print(df_rollingmean.head())
#df_glob.plot(ax=ax,colormap=plt.get_cmap("gist_rainbow"))
df_rollingmean.plot(ax=ax,colormap=plt.get_cmap("gist_rainbow"))
# _ = ax.set_xticklabels(df_rollingmean.index,rotation=45)


# In[ ]:



