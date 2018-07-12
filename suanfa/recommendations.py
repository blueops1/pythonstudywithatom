#coding:utf-8
from math import sqrt

#一个涉及影评者及其对几部影片评分情况的字典
critics={'Lisa Rose':{'Lady in the Water':2.5,'Snakes on a Plane':3.5,'Just My Luck':3.0,
'Superman Returns':3.5,'You, Me and Dupree':2.5,'The Night Listener':3.0},
'Gene Seymour':{'Lady in the Water':3.0,'Snakes on a Plane':3.5,'Just My Luck':1.5,
'Superman Returns':5.0,'You, Me and Dupree':3.5,'The Night Listener':3.0},
'Michael Phillips':{'Lady in the Water':2.5,'Snakes on a Plane':3.0,'Superman Returns':3.5,
'The Night Listener':4.0},
'Claudia Puig':{'Snakes on a Plane':3.5,'Just My Luck':3.0,'Superman Returns':4.0,
'You, Me and Dupree':2.5,'The Night Listener':4.5},
'Mick LaSalle':{'Lady in the Water':3.0,'Snakes on a Plane':4.0,'Just My Luck':2.0,
'Superman Returns':3.0,'The Night Listener':3.0,'You, Me and Dupree':2.0},
'Jack Matthews':{'Lady in the Water':3.0,'Snakes on a Plane':4.0,'Superman Returns':5.0,
'The Night Listener':3.0,'You, Me and Dupree':3.5},
'Toby':{'Snakes on a Plane':4.5,'Superman Returns':4.0,'You, Me and Dupree':1.0}}

#返回一个有关person1 与 person2 的基于距离的相似度评价--欧几里德距离相关度评价
def sim_distance(prefs,person1,person2):
    #得到shared_item 的列表
    si = {}
    for item in prefs[person1]:
        if item in prefs[person2]:
            si[item] = 1

    # 如果两者没有共同之处，则返回 0
    if len(item) == 0: return 0

    #计算所有差值的平方和
    sum_of_squares = sum([pow(prefs[person1][item]-prefs[person2][item],2)
                            for item in prefs[person1] if item in prefs[person2]])

    return 1/(1+sqrt(sum_of_squares))

# 返回p1 和 p2 的皮尔逊相关系数
def sim_pearson(prefs,p1,p2):
    #得到双方都曾评价过的物品列表
    si = {}
    for item in prefs[p1]:
        if item in prefs[p2]:si[item] = 1

    #得到列表元素的个数
    n = len(si)

    # 如果两者没有共同之处，则返回 1
    if n == 0: return 1

    #对所有偏好求和
    sum1 = sum([prefs[p1][it] for it in si])
    sum2 = sum([prefs[p2][it] for it in si])

    #求平方和
    sum1Sq = sum([pow(prefs[p1][it],2) for it in si])
    sum2Sq = sum([pow(prefs[p2][it],2) for it in si])

    #求乘积之和
    pSum = sum([prefs[p1][it]*prefs[p2][it] for it in si])

    # 计算皮尔逊评价值
    num = pSum - (sum1 * sum2 / n)
    den = sqrt((sum1Sq -pow(sum1,2)/n)*(sum2Sq-pow(sum2,2)/n))
    if den == 0 : return 0

    r = num/den

    return r

# 从反映偏好的字典中返回最为匹配者
# 返回结果的个数和相似度函数均为可选参数
def topMatches(prefs,person,n=5,similarity=sim_pearson):
    scores = [(similarity(prefs,person,other),other)
                for other in prefs if other != person]
# 对列表进行排序，评价值最高者排在最前面
    scores.sort()
    scores.reverse()
    return scores[0:n]



# 返回所有人中相似度最高的人员名单
def simest_person(prefs,similarity=sim_distance):
    #相似度值
    bigest_sim_score = 0.0
    new_sim_score = 0.0
    simest_person = {}
    old_name = []

    persons = list(prefs.keys())
    for name1 in persons:
        old_name.append(name1)
        for name2 in persons:
            if (name1 == name2) or (name2 in old_name ):
                pass
            else:
                new_sim_score = similarity(prefs,name1,name2)
                #print(bigest_sim_score)
                #print(new_sim_score)
                #print(name1,name2)
                if new_sim_score > bigest_sim_score:
                    bigest_sim_score = new_sim_score
                    simest_person = {name1 + '|' + name2:bigest_sim_score}

    return simest_person

if __name__ == '__main__':
    print(simest_person(critics))
    print(simest_person(critics,sim_pearson))
    print(topMatches(critics,'Toby',n=3))
