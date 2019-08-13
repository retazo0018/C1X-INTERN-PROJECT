import numpy as np
import pandas as pd
import psycopg2
#from ip2geotools.databases.noncommercial import DbIpCity
import pygeoip

def connection():
    try:
        conn = psycopg2.connect(user="spyfu", password="SpyfuU$3r", host="18.219.13.131", port="5432",
                                      database="spyfu")
        cursor = conn.cursor()
    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL ", error)
    else:
        print("")

    return conn, cursor


def cookiechurn():
    conn, cursor = connection()
    clist = []
    cursor.execute("select distinct (uuid) from  impression_agg_poc where date_utc = '2019-06-05'")
    res = cursor.fetchall()
    clist.append(res)
    cursor.execute("select distinct (uuid) from  impression_agg_poc where date_utc = '2019-06-06'")
    res = cursor.fetchall()
    clist.append(res)
    cursor.execute("select distinct (uuid) from  impression_agg_poc where date_utc = '2019-06-07'")
    res = cursor.fetchall()
    clist.append(res)
    cursor.execute("select distinct (uuid) from  impression_agg_poc where date_utc = '2019-06-08'")
    res = cursor.fetchall()
    clist.append(res)
    cursor.execute("select distinct (uuid) from  impression_agg_poc where date_utc = '2019-06-09'")
    res = cursor.fetchall()
    clist.append(res)
    cursor.execute("select distinct (uuid) from  impression_agg_poc where date_utc = '2019-06-10'")
    res = cursor.fetchall()
    clist.append(res)
    cursor.execute("select distinct (uuid) from  impression_agg_poc where date_utc = '2019-06-11'")
    res = cursor.fetchall()
    clist.append(res)

    cookieagetrend = []
    temp = []
    temp.append(len(clist[0]))
    temp.append(100)
    cookieagetrend.append(temp)
    c1, c2, c3, c4, c5, c6 = 0, 0, 0, 0, 0, 0
    temp = []
    for j in range(len(clist[0])):
        if (clist[1].count(clist[0][j]) > 0):
            c1 += 1
        if (clist[2].count(clist[0][j]) > 0):
            c2 += 1
        if (clist[3].count(clist[0][j]) > 0):
            c3 += 1
        if (clist[4].count(clist[0][j]) > 0):
            c4 += 1
        if (clist[5].count(clist[0][j]) > 0):
            c5 += 1
        if (clist[6].count(clist[0][j]) > 0):
            c6 += 1
    temp.append(c1)
    temp.append(round((c1 / len(clist[0])) * 100, 3))
    cookieagetrend.append(temp)
    temp = []

    temp.append(c2)
    temp.append(round((c2 / len(clist[0])) * 100, 3))
    cookieagetrend.append(temp)
    temp = []

    temp.append(c3)
    temp.append(round((c3 / len(clist[0])) * 100, 3))
    cookieagetrend.append(temp)
    temp = []

    temp.append(c4)
    temp.append(round((c4 / len(clist[0])) * 100, 3))
    cookieagetrend.append(temp)
    temp = []

    temp.append(c5)
    temp.append(round((c5 / len(clist[0])) * 100, 3))
    cookieagetrend.append(temp)
    temp = []

    temp.append(c6)
    temp.append(round((c6 / len(clist[0])) * 100, 3))
    cookieagetrend.append(temp)
    temp = []

    return cookieagetrend


def toplevelmetacategories():
    conn, cursor = connection()
    cursor.execute("select mcid, uuid from click_agg_poc")
    week = cursor.fetchall()
    week = pd.DataFrame(week)
    week.columns = ['MCID', 'UUID']
    week = week[week['UUID'] != 'undefined']
    new = week.groupby(week.MCID)
    category = new.apply(lambda x: x['UUID'].unique())
    category = pd.DataFrame(category)
    category.columns = ['UUID']
    top = {}
    count = 0
    for index, row in category.iterrows():
        top.update({index: 0})
        for i in row:
            c = len(i)
        top[index] = c
        count = count + c
    topCategory = [[k, v] for k, v in top.items()]
    topCategory.sort(key=lambda x: x[1], reverse=True)
    df = pd.DataFrame(topCategory)
    df.columns = ['MCID', 'Count']

    cat = pd.read_csv("assets/category-soka.csv")
    cat = cat[['id', 'name']]
    cat = pd.DataFrame(cat)
    cat.columns = ['MCID', 'Name']
    cat.head()

    result = pd.merge(df, cat, on='MCID')
    final = result.head(10)
    return final


def count_of_users_in_each_city(ip_s):
    gi = pygeoip.GeoIP('assets/dbip4.dat')
    citycount = {}
    for i in range(len(ip_s)):
        try:
            records = gi.record_by_addr(ip_s[i][0])
            if (records['city'] not in citycount):
                citycount[records['city']] = 1
            else:
                citycount[records['city']] += 1
        except:
            pass
    return citycount


def ip2geomapping():
    conn, cursor = connection()
    cursor.execute("select (userip) from click_agg_poc")
    ip_s = cursor.fetchall()
    citycount = count_of_users_in_each_city(ip_s)
    lat = []
    lon = []
    information = []
    gi = pygeoip.GeoIP('assets/dbip4.dat')
    for i in range(len(ip_s)):
        try:
            info = ''
            records = gi.record_by_addr(ip_s[i][0])
            lat.append(records['latitude'])
            lon.append(records['longitude'])
            info += records['city']
            info += ' | UU: '
            info += str(citycount[records['city']])
            information.append(info)
        except:
            pass
    return lat, lon, information

def channelcount():
    conn, cursor = connection()
    cursor.execute("SELECT channel, COUNT(*) FROM click_agg_poc GROUP BY channel")
    channel = cursor.fetchall()
    nchannel=[]
    for i in range(len(channel)):
        temp = []
        if(channel[i][0] == 'M'):
            temp.append('Mobile')
            temp.append(channel[i][1])
            nchannel.append(temp)
        elif (channel[i][0] == 'D'):
            temp.append('Desktop')
            temp.append(channel[i][1])
            nchannel.append(temp)
        else:
            temp.append('App')
            temp.append(channel[i][1])
            nchannel.append(temp)
    return sorted(nchannel, key = lambda x: x[1], reverse=True)

def valueboxes():
    conn, cursor = connection()
    cursor.execute("SELECT count(uuid) FROM click_agg_poc")
    tclicks = cursor.fetchall()

    cursor.execute("SELECT count(uuid) FROM impression_agg_poc")
    timpressions = cursor.fetchall()

    cursor.execute("SELECT COUNT(*) FROM (SELECT DISTINCT uuid FROM impression_agg_poc) as uniqueusers")
    tuniqueusers = cursor.fetchall()

    cursor.execute("SELECT count(uuid) FROM capacity_agg_poc")
    tcapacity = cursor.fetchall()


    return format(tclicks[0][0],',d'), format(timpressions[0][0],',d'), format(tuniqueusers[0][0], ',d'), format(tcapacity[0][0], ',d')



