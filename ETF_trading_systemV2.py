# -*- coding: utf-8 -*-
import re
import requests
import os
import time
import json
import operator
from pprint import pprint
from bs4 import BeautifulSoup

if not os.path.exists("output"):
    os.mkdir("output")

header = {
    'cookie': '__utmt=1; _hjUserId=616c6415-761e-30fa-b733-1652b38ca9b2; csrftoken=yyhYiazr254BNO8XYYB166LtfZePf2kc; __utma=94914500.1425706763.1448673958.1448673958.1448673958.1; __utmb=94914500.2.10.1448673958; __utmc=94914500; __utmz=94914500.1448673958.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36'}

urls = ["http://www.ibillionaire.me/funds/1/warren-buffett/berkshire-hathaway",
        "http://www.ibillionaire.me/funds/4/carl-icahn/carl-icahn",
        "http://www.ibillionaire.me/funds/17/george-soros/soros-fund-management",
        "http://www.ibillionaire.me/funds/29/ray-dalio/bridgewater-associates",
        "http://www.ibillionaire.me/funds/5/john-paulson/paulson-co",
        "http://www.ibillionaire.me/funds/3/david-tepper/appaloosa-management-lp",
        "http://www.ibillionaire.me/funds/14/leon-cooperman/omega-advisors",
        "http://www.ibillionaire.me/funds/19/julian-robertson/tiger-management",
        "http://www.ibillionaire.me/funds/10/daniel-loeb/third-point-capita",
        "http://www.ibillionaire.me/funds/21/steve-mandel/lone-pine-capit",
        "http://www.ibillionaire.me/funds/31/nelson-peltz/trian-fund-management",
        "http://www.ibillionaire.me/funds/30/larry-robbins/glenview-capital-management",
        "http://www.ibillionaire.me/funds/13/bill-ackman/pershing-squar",
        "http://www.ibillionaire.me/funds/9/david-einhorn/greenlight-capital",
        "http://www.ibillionaire.me/funds/11/chase-coleman/tiger-global",
        "http://www.ibillionaire.me/funds/23/richard-chilton/chilton-investment-co"
        ]

# Portfolio
ConsumerStaples = 0
Financials = 0
Technology = 0
ConsumerDiscretionary = 0
Energy = 0
Industrials = 0
Health = 0
Telecommunications = 0
Materials = 0
Utilities = 0
Portfolio = [ConsumerStaples, Financials, Technology, ConsumerDiscretionary, Energy, Industrials, Health,
             Telecommunications, Materials, Utilities
             ]

# use bs4 to extract date
try:
    res = requests.get(urls[0], verify=False, headers=header)
except Exception as e:
    print "Check Portfolio Date occurs Exception: " + str(e)
    quit()
soup = BeautifulSoup(res.content, "html.parser")

spans = []
for span in soup.find_all('span'):
    spans.append(span.text)
date = spans[4][10:]

print "Portfolio Date: " + date
print "Continue? (y = yes, empty or others will exit)"
go = raw_input("")
if go != 'y':
    print "you input " + str(go)
    print "bye bye!"
    quit()
print "Roger that! This will take some minutes..."
print ""

for i in range(0, len(urls)):
    # sometimes connection will be rejected, need error handle
    try:
        res = requests.get(urls[i], verify=False, headers=header)
    except Exception as e:
        print "Get data occurs Exception: " + str(e)
        print res.url
        quit()

    # user re to retract Portfolio Value
    match = re.search('\<h2\>([0-9]*.)', res.text)
    if match:
        value_str = match.group(0)
        if value_str[-1] == 'M':
            p_value = float(value_str[4:-1]) / 1000
        elif value_str[-1] == 'B':
            p_value = float(value_str[4:-1])
        else:
            print "not get Portfolio Value"
            p_value = 0
    else:
        print "not get Portfolio Value"
        p_value = 0

    # use re to extract types and percentages
    m = re.search("data: eval\('\[(.*)\]'", res.text)
    # clean space and remove []
    m2 = m.group(1).replace(" ", "").replace("[", "").replace("]", "")
    # split string by "," and transform to list
    m3 = m2.split(",")

    for i in range(int(len(m3) / 2)):
        type = m3[2 * i][1:-1]
        percentage = round(float(m3[2 * i + 1]), 2)

        if type == u'ConsumerStaples':
            ConsumerStaples += p_value * percentage
            # print "ConsumerStaples: " + str(ConsumerStaples)
        elif type == u'Financials':
            Financials += p_value * percentage
            # print "Financials: " + str(Financials)
        elif type == u'Technology':
            Technology += p_value * percentage
            # print "Technology: " + str(Technology)
        elif type == u'ConsumerDiscretionary':
            ConsumerDiscretionary += p_value * percentage
            # print "ConsumerDiscretionary: " + str(ConsumerDiscretionary)
        elif type == u'Energy':
            Energy += p_value * percentage
            # print "Energy: " + str(Energy)
        elif type == u'Industrials':
            Industrials += p_value * percentage
            # print "Industrials: " + str(Industrials)
        elif type == u'Health':
            Health += p_value * percentage
            # print "Health: " + str(Health)
        elif type == u'Telecommunications':
            Telecommunications += p_value * percentage
            # print "Telecommunications: " + str(Telecommunications)
        elif type == u'Materials':
            Materials += p_value * percentage
            # print "Materials: " + str(Materials)
        elif type == u'Utilities':
            Utilities += p_value * percentage
            # print "Utilities: " + str(Utilities)
    time.sleep(1)

# save to dict
dic = {"ConsumerStaples": ConsumerStaples / 100, "Financials": Financials / 100, "Technology": Technology / 100,
       "ConsumerDiscretionary": ConsumerDiscretionary / 100, "Energy": Energy / 100, "Industrials": Industrials / 100,
       "Health": Health / 100, "Telecommunications": Telecommunications / 100, "Materials": Materials / 100,
       "Utilities": Utilities / 100
       }
sorted_dic = sorted(dic.items(), key=operator.itemgetter(1), reverse=True)
pprint(sorted_dic)

# save to json , name by date
with open("output/" + date + ".json", "w") as js:
    json.dump(sorted_dic, js)
print ""
print "Tango Down."
