import pandas as pd   
import pymysql
import numpy as np

db = pymysql.connect(host='localhost', user='root', password='hexin123', port=3306, db='quanzhigaoshou')
cursor = db.cursor()
sql = "SELECT * FROM quanzhigaoshou"
data = pd.read_sql(sql,db)
db.close()

print(data.head(3))
print('一共获得评论数据{}条'.format(len(data)))

import matplotlib.pyplot as plt #绘图
import matplotlib as mpl #配置字体
import seaborn as sns
from matplotlib.font_manager import FontProperties
myfont=FontProperties(fname=r'C:\Windows\Fonts\simhei.ttf',size=16)
sns.set(font=myfont.get_name())
#sns.set(font='SimHei')  # 解决Seaborn中文显示问题
mpl.rcParams['font.sans-serif'] = ['SimHei']
sns.set_style("white")
sns.set_context('notebook')

#按时间作图
data['time'] = data['ctime'].apply(lambda x: x[:10])

time = data[['time']].copy()
time['time_comment'] = 1
time = time.groupby(by=['time']).count()
print(time)

plt.figure(figsize=(50,10))
sns.pointplot(time.index,time['time_comment'],alpha=0.5)
plt.ylabel('评论数量', fontsize=25)
plt.xlabel('评论日期', fontsize=25)
plt.xticks(rotation='vertical')
plt.title('日期和数量', fontsize=30)
plt.show

#截取前一个月的数据
plt.figure(figsize=(15,10))
sns.pointplot(time.index[:30],time['time_comment'][:30],alpha=0.5,color="orange")
plt.ylabel('The number of comments', fontsize=15)
plt.xlabel('The time about comments', fontsize=15)
plt.xticks(rotation='vertical')
plt.show

#性别分布
plt.figure(figsize=(10,10))
sns.countplot(x="usersex",data=data,palette="pastel")  #上图
plt.show

#等级分布
plt.figure(figsize=(10,10))
sns.countplot(x="userlevel",data=data,palette="Set3")  #上图
plt.show

#前一个月等级和性别的关系
plt.figure(figsize=(15,10))
sns.countplot(x="userlevel",data=data,hue = 'usersex',palette="husl")  #上图
plt.show

time_sex = data[['floor','time','usersex']].copy()
time_sex = time_sex['floor'].groupby(by=[time_sex['time'],time_sex['usersex']]).count()

#plt.figure(figsize=(30,10))
#sns.countplot(data['floor'][:62822], hue=data.usersex, palette="husl")
#plt.xticks(rotation='vertical')
#plt.show


#提取用户观看时间段
data['clock'] = data['ctime'].apply(lambda x: x[11:13])
clock = data[['clock']].copy()
clock['comment'] = 1
clock = clock.groupby(by=['clock']).count()
print(clock)

plt.figure(figsize=(15,10))
sns.pointplot(clock.index,clock['comment'],alpha=0.5,color = 'hotpink')
plt.ylabel('The number of comments', fontsize=15)
plt.xlabel('The clock', fontsize=15)
plt.show

#用户观看时段和等级的关系
plt.figure(figsize=(20,10))
sns.countplot(data['clock'], hue=data.userlevel, palette="Set2")
plt.show


plt.figure(figsize=(15,10))
level = [0,2,3,4,5,6]
secret = [82,1409,5173,20117,21264,289]
male =[1,261,1737,7392,9462,192]
female =[0,519,2592,10669,14078,525]
plt.stackplot(level, secret, male, female, colors=['coral','skyblue','palegreen'])
plt.xlabel('x')
plt.ylabel('y')
plt.legend()
plt.show()



#评论情感分析
from snownlp import SnowNLP
data["semiscore"] = data['comment'].apply(lambda x: SnowNLP(x).sentiments)
data['semilabel'] = data["semiscore"].apply(lambda x: 1 if x>0.5 else -1)

plt.hist(data["semiscore"], bins = np.arange(0, 1.01, 0.01),label="semisocre", color="pink")
plt.xlabel("semiscore")
plt.ylabel("number")
plt.title("The semi-score of comment")
plt.show()


semilabel = data["semilabel"].value_counts()
plt.bar(semilabel.index,semilabel.values,tick_label=semilabel.index,color='lightsage')
plt.xlabel("semislabel")
plt.ylabel("number")
plt.title("The semi-label of comment")
plt.show()

#词云图

import jieba
comment=''.join(data['comment'])
wordlist = jieba.cut(comment, cut_all=False)
stopwords_chinese = [line.strip() for line in open('stopwords_chinese.txt',encoding='UTF-8').readlines()]
#过滤点单个字
word_list=[]
for seg in wordlist:
    if seg not in stopwords_chinese:
        word_list.append(seg)
       
word_list=pd.DataFrame({'comment':word_list})
word_rank = word_list["comment"].value_counts()


from pyecharts import WordCloud
wordcloud_chinese = WordCloud(width=1500, height=820)
wordcloud_chinese.add("", word_rank.index[0:100], word_rank.values[0:100], word_size_range=[20, 200], is_more_utils=True)
wordcloud_chinese.render("comment.html")
