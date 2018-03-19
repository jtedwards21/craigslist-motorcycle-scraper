import argparse
from bs4 import BeautifulSoup
import aiohttp
import asyncio
import async_timeout

async def get_list(response):
    '''
        Parse the response and collect the motorcycle
    '''

    soup = BeautifulSoup(response, "html.parser")
    motorcycles = soup.find_all("li", "result-row")

    return motorcycles

async def fetch(session, url):
    '''
    Basic request with a 30 second timeout
    '''
    with async_timeout.timeout(30):
        async with session.get(url) as response:
            return await response.text()

async def getPage():
    '''
    Returns a page from an http session
    '''
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(verify_ssl=False)) as session:
        response = await fetch(session, getUrl())

    listed = []

    listed = await get_list(response)

    return listed

async def outBike(li_stub):
    '''
    Parsing Section:
    This will parse the li stub to a
    dictionary and output it to a csv file if specified
    '''
    title = li_stub.find("a", "result-title").text
    print(title)
    if(li_stub.find("span", "result-price")):
        price = li_stub.find("span", "result-price").text
    else:
        price = "None"
    print(price)
    if(li_stub.find("span", "result-hood")):
        location = li_stub.find("span", "result-hood").text
    else:
        location = "None"
    post_time = li_stub.find("time", "result-date")["datetime"]

    output = {'title':title, 'price':price, 'location': location, 'post_time':post_time}

    print(output)



def getUrl():
    '''
        URL Decision:
        Scraper uses arguments to construct the URL for scraping

        Returns complete URL.
    '''

    url = "https://greensboro.craigslist.org/search/mca?"

    if arg.m != None:
        url += "auto_make_model%3A{0.m}".format(arg)
    if arg.ud != None:
        url += "max_engine_displacement_cc=%3A{0.ud}".format(arg)
    if arg.ld != None:
        url += "min_engine_displacement_cc=%3A{0.ld}".format(arg)
    if arg.uy != None:
        url += "max_auto_year=%3A{0.uy}".format(arg)
    if arg.ly != None:
        url += "min_auto_year=%3A{0.ly}".format(arg)
    if arg.up != None:
        url += "max_price==%3A{0.up}".format(arg)
    if arg.lp != None:
        url += "min_price==%3A{0.lp}".format(arg)

    return url


async def main():
    response = await getPage()
    for l in response:
        await outBike(l)

if __name__ == '__main__':
     ap = argparse.ArgumentParser(prog="motoscraper.py", usage="python %(prog)s [options]", description="Motoscraper - A craigslist scraper for bikes")
     ap.add_argument("-m", help="Search for a make and model")
     ap.add_argument("-ud", help="Set max engine displacement")
     ap.add_argument("-ld", help="Set min engine displacement")
     ap.add_argument("-uy", help="Set max year")
     ap.add_argument("-ly", help="Set min year")
     ap.add_argument("-up", help="Set max price")
     ap.add_argument("-lp", help="Set min price")

     arg = ap.parse_args()

     loop = asyncio.get_event_loop()
     loop.run_until_complete(main())
