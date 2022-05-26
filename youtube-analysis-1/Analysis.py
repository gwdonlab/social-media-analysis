import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

data=pd.read_csv('data.csv')

#Top 10 videos based on views
data_sort=data.sort_values(by='Number_of_views',ascending=False).head(10)
plt.figure(figsize=(20,10))
sns.barplot(x='Number_of_views',y='Title',data=data_sort)
plt.title('Top 10 videos based on view count')
plt.tight_layout()
plt.show()

#Top 10 videos based on likes
data_sort=data.sort_values(by='Number_of_Likes',ascending=False).head(10)
plt.figure(figsize=(20,10))
sns.barplot(x='Number_of_Likes',y='Title',data=data_sort)
plt.title('Top 10 videos based on number of Likes')
plt.tight_layout()
plt.show()

#Top 10 videos based on comments
data_sort=data.sort_values(by='Number_of_Comments',ascending=False).head(10)
plt.figure(figsize=(20,10))
sns.barplot(x='Number_of_Comments',y='Title',data=data_sort)
plt.title('Top 10 videos based on number of Comments')
plt.tight_layout()
plt.show()