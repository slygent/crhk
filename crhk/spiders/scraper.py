# coding=utf-8

import scrapy
from crhk.items import CompanyRecord

import datetime

class CrhkSpider(scrapy.Spider):
    name = "crhk"
    allowed_domains = ["mobile-cr.gov.hk"]
    numberofcompanies = 3000000 # more than current number of companies, use CLOSESPIDER_ERRORCOUNT to stop after reaching maximum

    baseurl = "https://www.mobile-cr.gov.hk/mob/cps_criteria.do?queryCRNO="
    start_urls = map(lambda x: "".join(("https://www.mobile-cr.gov.hk/mob/cps_criteria.do?queryCRNO=", format(x, '07'))), range(1,3) + range(4,numberofcompanies+1))

    def parse(self, response):    
        item = CompanyRecord()
        item['crno'] = response.css(".info tr:nth-child(1) td:nth-child(2)::text").extract_first()
        item['companynames'] = map(unicode.strip, response.css("td tr:nth-child(2) td::text").extract())
        item['companytype'] = map(unicode.strip, response.css("tr:nth-child(3) td:nth-child(2)::text").extract())[0]
        item['dateofincorporation'] = response.css("tr:nth-child(4) td:nth-child(2)::text").extract_first().replace(u'\u6708', "")
        item['activestatus'] = map(unicode.strip, response.css("tr:nth-child(5) td:nth-child(2)::text").extract())[0]
        item['remarks'] = map(unicode.strip, response.css(".sameasbody::text").extract())
        item['windingup'] = map(unicode.strip, response.css("tr:nth-child(7) td:nth-child(2)::text").extract())[0]
        item['dateofdissolution'] = response.css("tr:nth-child(8) td:nth-child(2)::text").extract_first().replace(u'\u6708', "")
        item['registerofcharges'] = map(unicode.strip, response.css("tr:nth-child(9) td:nth-child(2)::text").extract())[0]
        item['note'] = map(unicode.strip, response.css("tr:nth-child(10) td::text").extract())

        namehistorydict = {}
        namestds = response.css("td.data")   # historical dates of different names
        for idx, namestd in enumerate(namestds):
            namestdtext = namestd.css("::text").extract()
            if len(namestdtext) == 2:
                namehistorydict[namestdtext[0]] = {"English" : namestdtext[1]}
            else:
                namehistorydict[namestdtext[0]] = {"English" : namestdtext[1], "Chinese" : namestdtext[2]}

        item['namehistory'] = namehistorydict
        item['scrapetime'] = datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S")
        yield(item)
    
