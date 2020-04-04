import subprocess
import random
import sys

#csv file https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv
def getHttpTextResp(url):
    p = subprocess.Popen(['curl','-X','GET',url], stdout=subprocess.PIPE)
    out, err = p.communicate()
    return str(out).split('\\n')
    
#obtains time vector from csv file list x 
def getVect(x):
    vect = []
    for i in range(1,len(x)):
        q = []
        lim = len(x[i].split(','))
        if(x[i].split(',')[0] == ''):
            q.append(x[i].split(',')[1])
        else:
            q.append(x[i].split(',')[0])
        for j in range(4,lim):
            q.append(x[i].split(',')[j].replace('\n',''))
        vect.append(q)
    vect.pop()
    return vect
    
#get projection montecarlo values
def getProjectionSeeds(timevector,iterations):
    seeds = []
    for i in timevector:
        iter = 0
        ms = 0
        interval = []
        for j in range(1,len(i)):
            if(i[j] != '0'):
                for k in range(0,iterations):
                     iter = iter + float(i[j]) * random.random()
                ms = iter/iterations
            interval.append(str(ms))
        interval.append(i[0])
        seeds.append(interval)
    return seeds
        
#generate Tomorrow's projection
def getTomorrowProjection(timevector):
    projection = []
    for i in timevector:
        interval = 0
        for j in range (0,2):
            interval = interval + float(i[len(i)-2-j])
        projection.append(str(i[len(i)-1]) + "," + str(interval/3))
    return projection
    
def main(argv):
    url = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv'
    res = getHttpTextResp(url)
    timevector = getVect(res)
    timemcseeds = getProjectionSeeds(timevector,100)
    projection = getTomorrowProjection(timemcseeds)
    for i in projection:
        print(i)

if __name__ == '__main__':
    main(sys.argv)
        
    