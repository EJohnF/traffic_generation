import numpy
import google
import time
from bs4 import BeautifulSoup
import requests
from SiteList import SiteList
from Surfing import Surfing
from Opener import *

random.seed(10)


def distribution_to_value(description):
    dis_type = description["type"]
    if dis_type == "uniform":
        return random.randint(int(description["low_boundary"]), int(description["up_boundary"]))
    if dis_type == "log-normal":
        return numpy.exp(numpy.random.normal(description["M"], description["D"]))
    return 0


def correctURL(originalURL):
    goodURL = originalURL
    if str.find(originalURL, 'http') == -1:
        goodURL = 'http://' + originalURL
    return goodURL


def get_sitemaps(siteURL):
    url = correctURL(siteURL)
    if str.find(siteURL, 'sitemap.xml') == -1:
        if str.rfind(siteURL, '/') < len(siteURL) - 1:
            url += '/'
        url += 'sitemap.xml'
    print('point to find sitemaps: ', url)
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


def get_URLs_from_sitemap(sitemapURL, number=20, withInfo=False):
    print('sitemap: ', sitemapURL)
    r = requests.get(sitemapURL)
    data = r.text
    soup = BeautifulSoup(data, 'lxml')
    result = []
    for url in soup.findAll("url"):
        number -= 1
        if number < 0:
            break
        urlNext = ''
        changefreq = ''
        priority = ''
        if url.find('loc'):
            urlNext = url.find('loc').text
        if url.find('changefreq'):
            changefreq = url.find('changefreq').text
        if url.find('priority'):
            priority = url.find('priority').text
        if withInfo:
            result.append((urlNext, changefreq, priority))
        else:
            result.append(urlNext)
            #         print(urlNext, changefreq, priority)
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
        if tag.attrs:
            try:
                link = tag.attrs['href']
                if str.find(link, 'http') == -1:
                    if str.rfind(url, '/') == len(url) - 1:
                        link = url[0:len(url) - 1] + link
                    else:
                        link = url + link
                        #                 print(link)
                result.append(link)
            except:
                a = 1
                #                 print('parse Error of tag: ', tag)
    return result


# In[23]:

def generate_pages_google(site_link, number_pages=10):
    print('generate_pages_google')
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
    print('generate_pages_sitemap')
    sitemaps = get_sitemaps(site)
    result = []
    for sm in sitemaps:
        result += get_URLs_from_sitemap(sm, number_pages)
    return random.sample(result, number_pages)


def generate_pages_scraping(site, number_pages=10):
    print('generate_pages_scraping')
    result = []
    first_lvl_pages = get_URLs_from_page(site)
    first_lvl_pages = random.sample(first_lvl_pages, min(number_pages, len(first_lvl_pages)))
    for page in first_lvl_pages:
        result += get_URLs_from_page(page)
    result = first_lvl_pages + result
    return random.sample(result, min(number_pages, len(result)))


def generate_page_list(site, generator, number_pages=10):
    if generator == 'sitemap':
        return generate_pages_sitemap(site, number_pages)
    if generator == 'site-scraping':
        return generate_pages_scraping(site, number_pages)
    # the default one
    return generate_pages_google(site, number_pages)


# In[25]:

def go_round_site(site, scheme):
    print('go round site: ', site, ' scheme: ', scheme)
    number_page = distribution_to_value(scheme['page_number'])
    print('page_number ', number_page)
    pages_list = generate_page_list(site, scheme['page_generator'], int(number_page))
    for page in pages_list:
        open_page(page)
        sleep_time = distribution_to_value(scheme['time_between_page'])
        print('sleep time: ', sleep_time)
        time.sleep(sleep_time)


def process_specific_type(site_object, config):
    typ = site_object['type']
    if typ == "sitelist_xlsx":
        sitelist = SiteList(site_object)
        count_for_visit = site_object['count_for_visit']
        # sitelist = random.sample(sitelist, min(count_for_visit, len(sitelist)))
        scheme = parse_scheme(site_object['scheme'], config)
        for site in sitelist:
            go_round_site(site, scheme)
            count_for_visit -= 1
            if count_for_visit < 0:
                break
    if typ == "infinity_surfing":
        surfing = Surfing(site_object['link'], parse_scheme(site_object['scheme'],config))
        surfing.start()


def parse_scheme(scheme, config):
    if isinstance(scheme, str):
        return config['schemes'][scheme]
    else:
        return scheme


def parse_site(site, config):
    if isinstance(site, str):
        go_round_site(site, config['schemes']['default'])
    else:
        withtype = False
        try:
            # check is there 'type' field in site object
            t = site['type']
            withtype = True
        except:
            # work with given link and given scheme
            scheme = parse_scheme(site['scheme'], config)
            go_round_site(site['link'], scheme)
        if withtype:
            # type was given, so work with specific site object
            process_specific_type(site, config)


def parser_site_list(sites, config):
    for site in sites:
        print("site!!! :", site)
        parse_site(site, config)
        # thread.start_new_thread(parse_site, (site, config,))
