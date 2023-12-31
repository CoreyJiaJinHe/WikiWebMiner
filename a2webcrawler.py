#Name: Corey He
#ID: 217253527

# Importing Python libraries
import bs4 as BeautifulSoup
import urllib.request  
import csv
import re
import math
import statistics
import numpy as np #Not used. Could use it, but decided to do it manually. 
import os.path


countries=[]
url=[]
headers=["Country Name", "Capital", "Languages", "Total Area", "Population", "GDP (PPP)"]
linkfiledata=[]

#Get wikipedia links
path='./link.txt'
if (os.path.isfile(path)):
    f=open("link.txt","r")
    for line in f:
        linkfiledata=line
        linkfiledata=linkfiledata.rstrip("\n")
        linkfiledata=linkfiledata.split(',')
        countries.append(linkfiledata[0])
        url.append(linkfiledata[1])
else: #If the link.txt file is not there.
    countries=['Canada','China','US','Korea','UK','France','Turkey','Italy']
    url=['https://en.wikipedia.org/wiki/Canada',
         'https://en.wikipedia.org/wiki/China',
         'https://en.wikipedia.org/wiki/United_States',
         'https://en.wikipedia.org/wiki/Korea',
        'https://en.wikipedia.org/wiki/United_Kingdom',
        'https://en.wikipedia.org/wiki/France',
        'https://en.wikipedia.org/wiki/Turkey',
        'https://en.wikipedia.org/wiki/Italy']
countrydata=[]

#Scraping and Storing
for count in range (len(countries)):
    get_data = urllib.request.urlopen(url[count])

    read_page = get_data.read()
    parse_page = BeautifulSoup.BeautifulSoup(read_page,'html.parser')

    right_table=parse_page.find(class_='infobox ib-country vcard')

    rows = right_table.findAll("tr")

    b=0
    languagecounter=0
    gdpcounter=0
    data=[]
    for tr in rows:
        if ((rows[b].find('th'))):

            if (b==0):
                data.append(rows[b].find(class_='fn org country-name').text.rstrip().replace('\xa0',' '))        
            else:
                
                if ("Capital" in rows[b].find('th').text):
                    text=(rows[b].find("td").text.rstrip().replace('\xa0',''))
                    
                    data.append(text)
                elif ("language" in rows[b].find('th').text and languagecounter==0):
                    if ("language" in rows[b+1].find('th').text.rstrip()):
                        languagelist=(rows[b+1].findAll("li"))
                        singlelanguage=""
                        language=""
                        singlelanguage=(rows[b].find("td").text.rstrip())
                        secondlanguage=(rows[b+1].find("td").text.rstrip())
                        language=singlelanguage
                        if (len(languagelist) > 0):
                            for count in range (len(languagelist)):
                                language = language+ ";"+ languagelist[count].text 
                        else:
                            language = singlelanguage
                            if (len(secondlanguage)!=0):
                                language= language +";" + secondlanguage
                        languagecounter=1
                    else:
                        languagelist=(rows[b].findAll("li"))
                        singlelanguage=""
                        language=""
                        singlelanguage=(rows[b].find("td").text.rstrip())
                        if (len(languagelist) > 0):
                            for count in range (len(languagelist)):
                                language = language + languagelist[count].text + ";"
                        else:
                            language = singlelanguage
                        languagecounter=1
                    data.append(language)

                elif ("Area" in rows[b].find('th').text and "Total" in rows[b+1].find('th').text):
                    data.append(rows[b+1].find("td").text.rstrip().replace('\xa0',''))
                    
                elif ("Population" in rows[b].find('th').text):
                    
                    text=(rows[b+1].text.rstrip().replace('\xa0',''))
                    poptext=re.sub(r'[0-9]$','',text)
                    poptext=re.sub(r'^.mw-.+}$','',poptext)
                    data.append(poptext)
                elif ("GDP" in rows[b].find('th').text.rstrip()):
                    data.append(rows[b+1].find("td").text.rstrip().replace('\xa0',''))
                    gdpcounter=1
        b=b+1
    if (count==3 and gdpcounter==0): 
                    #The Korea wiki page does not have GDP. So I get the GDP data from South Korea.
                    #Because NKorea's GDP is miniscule compared to SKorea.
                    gdpcounter=1
                    get_data = urllib.request.urlopen('https://en.wikipedia.org/wiki/South_Korea')

                    read_page = get_data.read()
                    parse_page = BeautifulSoup.BeautifulSoup(read_page,'html.parser')

                    southkoreatable=parse_page.find(class_='infobox ib-country vcard')

                    skorearows = southkoreatable.findAll("tr")
                    c=0
                    for skoreadata in skorearows:
                        if ((skorearows[c].find('th'))):
                            if ("GDP" in skorearows[c].find('th').text):
                                data.append(skorearows[c+1].find("td").text.rstrip().replace('\xa0',''))
                                break
                        c=c+1
                        
    countrydata.append(data)

#Data Cleaning
for count in range (len(countrydata)):
    editcountrydata = countrydata[count]
    for secondcount in range (len(editcountrydata)):
        text=""
        text=editcountrydata[secondcount]
        
        if ("\ufeff" in editcountrydata[secondcount]):
            text=text[0:text.index("\ufeff")]
        if (secondcount==1): 
            if (re.search(r'[0-9]',text)):
                findgarbage=""
                findgarbage=re.search(r'[0-9]',text)
                text=text[0:findgarbage.start()] 
                editcountrydata[secondcount]=text
        if (re.search(r'\[.*\]',text)):
            text=re.sub(r'\[.*\]','',text)
        if (re.search(r'\(.{4}\)|\(.{3}\)',text)):
            text=re.sub(r'\(.{4}\)|\(.{3}\)','',text)   
        if (re.search(r'[0-9]{1}[a-zA-Z]|[a-zA-Z]{1}[0-9]',text)):
            text=text[0:re.search(r'[0-9]{1}[a-zA-Z]|[a-zA-Z]{1}[0-9]',text).end()-1] + " "+ text[re.search(r'[0-9]{1}[a-zA-Z]|[a-zA-Z]{1}[0-9]',text).end()-1:]
        if (secondcount==2 and ('level' in text)):
            text=text[text.index('level')+6:]
        if (secondcount==3): #US total area unit switch
            if(count==2):
                areaswitch1=text[text.index("("):]
                areaswitch1=areaswitch1.replace("(",'')
                areaswitch1=areaswitch1.replace(")",'')
                areaswitch1=areaswitch1[:re.search(r'[0-9]{1}[a-zA-Z]',areaswitch1).end()-1] + " "+ areaswitch1[re.search(r'[0-9]{1}[a-zA-Z]',areaswitch1).end()-1:]

                text=areaswitch1
            else:
                text=text[:text.index("(")]
        if (secondcount==4):
            text=text.replace(',','')
        text=text.strip(" ")
        text=text.strip("•")
        text=text.strip("\n")
        text=text.strip(";")
        editcountrydata[secondcount]=text
        if (secondcount==6):
            editcountrydata.pop()
    countrydata[count]=editcountrydata


#Output table data.
for count in range (len(countrydata)):
    displaycountrydata = countrydata[count]
    for secondcount in range (len(displaycountrydata)):
        print (displaycountrydata[secondcount])
    print ("\n")


#Output into .csv file
with open('output.csv','w', newline='') as f:
    writer=csv.writer(f)  
    writer.writerow(headers)
    for count in range (len(countrydata)):
        displaycountrydata = countrydata[count]
        writer.writerow(displaycountrydata)



#Computing Statistics
#0 is Country Name
#1 is Capital
#2 is Language
#3 is Area
#4 is Population
#5 is GDP (PPP)

#Find country with greatest population
poplist=[]
for count in range(len(countrydata)):
    loopthroughcountry=countrydata[count]
    population=str(loopthroughcountry[4])
    population=population[re.search(r'[0-9]+$',population).start():]
    poplist.append(int(population))
print ("The country with the highest population of " + str(max(poplist)) +" is the country of " + str(countries[poplist.index(max(poplist))]))

#Find country with greatest total area
arealist=[]
for count in range(len(countrydata)):
    loopthroughcountry=countrydata[count]
    area=str(loopthroughcountry[3])
    area=area.replace(',','')
    area=area.replace(" km2",'')
    arealist.append(int(area))
print ("The country with the largest area of " + str(max(arealist)) +" km2 is the country of " + str(countries[arealist.index(max(arealist))]))
GDPlist=[]

#Find country with greatest GDP
for count in range(len(countrydata)):
    loopthroughcountry=countrydata[count]
    GDP=str(loopthroughcountry[5])
    GDP=GDP.replace(',','')
    GDP=GDP.replace("$",'')
    GDP=GDP.replace(" trillion",'')
    GDPlist.append(float(GDP))
print ("The country with the largest GDP of $" + str(max(GDPlist)) +" trillion is the country of " + str(countries[GDPlist.index(max(GDPlist))]))
print ("\n")
#Write code to compute the Pearson correlation coefficient for pairs of variables, 
# uch as (area, population), (area, GDP), and (population, GDP), as defined in the documentation at "https://en.wikipedia.org/wiki/Pearson_correlation_coefficient."

#Pearson's correlation coefficient = covariance(X, Y) / (stdv(X) * stdv(Y))

#Formula for Population(Statistics) Standard Deviation 
# Vector x - mean(x)
popdeviations= [x - statistics.mean(poplist) for x in poplist]
# Sum of Vector Differences squared
sumsquaredeviation=sum([x**2 for x in popdeviations])
# Squareroot of sum/population(vector size/number of observations)
#deviation between countries' population
stdx=math.sqrt( sumsquaredeviation/(len(poplist)) )

#deviation between countries' GDP (PPP)
GDPdeviations= [x - statistics.mean(GDPlist) for x in GDPlist]
sumsquaredeviation=sum([x**2 for x in GDPdeviations])
stdy=math.sqrt( sumsquaredeviation/(len(GDPlist)) )

#deviation between countries' total area
areadeviations= [x - statistics.mean(arealist) for x in arealist]
sumsquaredeviation=sum([x**2 for x in areadeviations])
stdz=math.sqrt( sumsquaredeviation/(len(arealist)))


popdeviations= [x - statistics.mean(poplist) for x in poplist]
GDPdeviations=[x - statistics.mean(GDPlist) for x in GDPlist]
areadeviations=[x - statistics.mean(arealist) for x in arealist]

popgdpcovariance=sum([a*b for a,b in zip (popdeviations,GDPdeviations)])/(len(poplist))
popareacovariance=sum([a*b for a,b in zip (popdeviations,areadeviations)])/(len(poplist))
areagdpcovariance=sum([a*b for a,b in zip (areadeviations,GDPdeviations)])/(len(arealist))


#Formula: Covariance XY / Standard Deviation X * Standard Deviation Y
#Pearson Correlation between Population & Total Area
PearsonCorrelation=popareacovariance/(stdx*stdz)
print ("The Pearson Correlation between Population and Total Area is: " +str(PearsonCorrelation))
#Pearson Correlation between Total Area & GDP
PearsonCorrelation=areagdpcovariance/(stdz*stdy)
print ("The Pearson Correlation between GDP and Total Area is: " +str(PearsonCorrelation))
#Pearson Correlation between Population & GDP
PearsonCorrelation=popgdpcovariance/(stdx*stdy)
print ("The Pearson Correlation between Population and GDP is: " +str(PearsonCorrelation))
print ("As the Pearson Correlation coefficient between these 3 variables are greater than 0 and above 0.5, it can be concluded that these three variables are highly correlated with one another.")










