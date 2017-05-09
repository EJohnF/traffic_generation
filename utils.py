import numpy
import google
import time
from bs4 import BeautifulSoup
import requests
from SiteList import SiteList
from Surfing import Surfing
from UsualSite import UsualSite
from Opener import *
from process_python_api import Logger, LError, LInfo
from distributions import Uniform, NormalPositive, DualNormal, Fix
random.seed(10)

def create_distribution(scheme):
    dis_type = scheme["type"]
    if dis_type == "uniform":
        return Uniform.Uniform(scheme)
    if dis_type == "positive-normal":
        return NormalPositive.NormalPositive(scheme)
    if dis_type == "fix":
        return Fix.Fix(scheme)
    if dis_type == "dual-normal":
        return DualNormal.DualNormal(scheme)

    Logger.log(LError, 'receive 0 unknow distribution type {}'.format(dis_type))
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
    Logger.log(LInfo, 'sitemaps_url 0 {}'.format(url))
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
    Logger.log(LInfo, 'sitemap 0 {}'.format(sitemapURL))
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
                result.append(link)
            except:
                pass
    Logger.log(LInfo, 'links_on_page {}'.format(len(result)))
    return result


def generate_pages_google(site_link, number_pages=10):
    Logger.log(LInfo, 'generator 0 google')
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
    Logger.log(LInfo, 'generator 0 sitemap')
    sitemaps = get_sitemaps(site)
    result = []
    for sm in sitemaps:
        result += get_URLs_from_sitemap(sm, number_pages)
    return random.sample(result, number_pages)


def generate_pages_scraping(site, number_pages=10):
    Logger.log(LInfo, 'generator 0 page-scraping')
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
    return generate_pages_google(site, number_pages)


def go_round_site(site, distr_count, distr_time, page_generator):
    number_page = distr_count.next()
    Logger.log(LInfo, 'number_page {}'.format(number_page))
    pages_list = generate_page_list(site, page_generator, int(number_page))
    for page in pages_list:
        open_page(page)
        sleep_time = distr_time.next()
        Logger.log(LInfo, 'sleep {}'.format(sleep_time))
        # time.sleep(sleep_time)


def parse_scheme(scheme, config):
    if isinstance(scheme, str):
        return config['schemes'][scheme]
    else:
        return scheme


def process_specific_type(site_scheme, config):
    typ = site_scheme['type']
    obj = ''
    if typ == "loaded_list":
        obj = SiteList(site_scheme, config)
    if typ == "infinity_surfing":
        obj = Surfing(site_scheme['link'], parse_scheme(site_scheme['scheme'], config))
    if typ == "usual_site":
        obj = UsualSite(site_scheme, config)
    obj.start()
    return obj


def parse_site_scheme(site, config):
    try:
        # check is there 'type' field in site object
        t = site['type']
    except:
        # work with given link and given scheme
        site['type'] = "usual_site"

    return process_specific_type(site, config)