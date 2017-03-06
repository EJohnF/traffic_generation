
# coding: utf-8

# In[41]:

import json
import random
import numpy
import google
import time
from threading import Thread

def open_page(link):
    print 'open_page', link
random.seed(10)

def distribution_to_value(description):
    dis_type = description["type"]
    if dis_type == "uniform":
        return random.randint(int(description["low_boundary"]), int(description["up_boundary"]))
    if dis_type == "log-normal":
        return numpy.exp(numpy.random.normal(description["M"], description["D"]))
    return 0


# In[42]:

from bs4 import BeautifulSoup
import requests
import string
from lxml import etree

def correctURL(originalURL):
    goodURL = originalURL
    if (string.find(originalURL, 'http') == -1):
        goodURL = 'http://' + originalURL
    return goodURL

def get_sitemaps(siteURL):
    url = correctURL(siteURL)
    if (string.find(siteURL, 'sitemap.xml') == -1):
        if (string.rfind(siteURL,'/') < len(siteURL)-1):
            url += '/'
        url += 'sitemap.xml'
    print 'point to find sitemaps: ', url
    try:
        r = requests.get(url)
    except: 
        return []
    data = r.text
    soup = BeautifulSoup(data, 'lxml')
    result = []
    for sitemap in soup.findAll('sitemap'):
        result.append(sitemap.find('loc').text)
    return result

def get_URLs_from_sitemap(sitemapURL, number = 20, withInfo = False):
    print 'sitemap: ', sitemapURL
    r = requests.get(sitemapURL)
    data = r.text
    soup = BeautifulSoup(data, 'lxml')
    result = []
    for url in soup.findAll("url"):
        number -=1
        if (number<0):
            break
        urlNext = ''
        changefreq = ''
        priority = ''
        if (url.find('loc')):
            urlNext = url.find('loc').text
        if (url.find('changefreq')):
            changefreq = url.find('changefreq').text
        if (url.find('priority')):
            priority = url.find('priority').text
        if (withInfo):
            result.append((urlNext, changefreq, priority))
        else:
            result.append(urlNext)
#         print urlNext, changefreq, priority
    return result

def get_URLs_from_page(url):
    url = correctURL(url)
    try:
        page = requests.get(url)
    except:
        return []
    soup = BeautifulSoup(page.text, "lxml")
    result = []
    for tag in soup.body.findAll('a'):
        if (tag.attrs):
            try:
                link = tag.attrs['href']
                if (string.find(link, 'http') == -1):
                    if (string.rfind(url,'/') == len(url)-1):
                        link = url[0:len(url)-1] + link
                    else :
                        link = url + link
#                 print link
                result.append(link)
            except:
                print 'parse Error of tag: ', tag
    return result


# In[43]:

def generate_pages_google(site_link, number_pages=10):
    print 'generate_pages_google'
    result = []
    i = 0
    for url in google.search("site:" + site_link, num=number_pages):
        if i < number_pages:
            result.append(url)
            i += 1
        else:
            break
    return result

def generate_pages_sitemap(site, number_pages=10):
    print 'generate_pages_sitemap'
    sitemaps = get_sitemaps(site)
    result = []
    for sm in sitemaps:
        result = result + get_URLs_from_sitemap(sm, number_pages)
    return random.sample(result, number_pages)

def generate_pages_scraping(site, number_pages=10):
    print 'generate_pages_scraping'
    result = []
    first_lvl_pages = get_URLs_from_page(site)
    first_lvl_pages = random.sample(first_lvl_pages, min(number_pages, len(first_lvl_pages)))
    for page in first_lvl_pages:
        result = result + get_URLs_from_page(page)
    result = first_lvl_pages + result
    return random.sample(result, min(number_pages, len(result)))

def generate_page_list(site, generator, number_pages=10):
    result = []
    if (generator == 'sitemap'):
        return generate_pages_sitemap(site, number_pages)
    if (generator == 'site-scraping'):
        return generate_pages_scraping(site, number_pages)
# the default one
    return generate_pages_google(site, number_pages)


# In[44]:

def go_round_site(site, scheme):
    print 'go round site: ', site, ' scheme: ', scheme
    number_page = distribution_to_value(scheme['page_number'])
    print 'page_number ', number_page
    pages_list = generate_page_list(site, scheme['page_generator'], int(number_page))
    for page in pages_list:
        open_page(page)
        sleep_time = distribution_to_value(scheme['time_between_page'])
        print 'sleep time: ', sleep_time
#         time.sleep(sleep_time)

def parser_site_list(sites, config):
    for site in sites:
        print "site!!! :", site
        if (isinstance(site, basestring)):
            print '1'
            go_round_site(site, config['schemes']['default'])
        else:
            if (isinstance(site['scheme'], basestring)):
                go_round_site(site['link'], config['schemes'][site['scheme']])
            else:
                go_round_site(site['link'], site['scheme'])


f = open('configuration.json', 'r')
config = json.load(f)
parser_site_list(config['sites'], config)


# In[ ]:



