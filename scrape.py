#!/usr/bin/env python3.5
import sys
import re
import random
import time
import requests
from bs4 import BeautifulSoup

LIB = 'lxml'
ENDPOINT = 'https://apps.hcr.ny.gov/buildingsearch/'

agent = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/51.0.2704.103 Safari/537.36"
)

AJAX_HEAD = {
    'X-MicrosoftAjax': 'Delta=true',
    'X-Requested-With': 'XMLHttpRequest'
}

def dumb_params(soup):
    try:
        return {
            '__VIEWSTATE': soup.find(attrs={'name': '__VIEWSTATE'}).attrs['value'],
            '__EVENTVALIDATION': soup.find(attrs={'name': '__EVENTVALIDATION'}).attrs['value'],
            '__VIEWSTATEGENERATOR': soup.find(attrs={'name': '__VIEWSTATEGENERATOR'}).attrs['value'],
            '__VIEWSTATEENCRYPTED': soup.find(attrs={'name': '__VIEWSTATEENCRYPTED'}).attrs['value'],
            '__EVENTARGUMENT': '',
            '__LASTFOCUS': '',
        }
    except AttributeError as err:
        # import pdb; pdb.set_trace()
        raise err


def construct_soup(text):
    fields = 'VIEWSTATE', 'EVENTVALIDATION', 'VIEWSTATEGENERATOR', 'VIEWSTATEENCRYPTED'
    vals = dict()

    for f in fields:
        match = re.search(r'__' + f + r'\|([^|]*)\|', text)
        vals[f] = match.groups()[0] if match else ''

    document = '''{} <input value="{VIEWSTATE}" name="__VIEWSTATE" />
        <input value="{EVENTVALIDATION}" name="__EVENTVALIDATION" />
        <input value="{VIEWSTATEGENERATOR}" name="__VIEWSTATEGENERATOR" />
        <input value="{VIEWSTATEENCRYPTED}" name="__VIEWSTATEENCRYPTED" />'''

    html = document.format(text, **vals)
    return BeautifulSoup(html, LIB)


def clean(text):
    text = re.sub(r'\s+', ' ', text.strip(' \r\n'))
    if ',' in text:
        return '"' + text + '"'
    else:
        return text


def writerows(f, soup):
    table = soup.find('table', attrs={'class': 'grid'})

    if table is None:
        raise RuntimeError("Missing table")

    for tr in table.find_all('tr'):
        if tr.td is None or tr.td.attrs.get('colspan') == 7:
            continue

        if 'Displaying buildings ' in str(tr):
            continue

        try:
            row = [clean(td.text) for td in tr.find_all('td')]
        except TypeError:
            import pdb
            pdb.set_trace()

        f.write(','.join(row) + '\n')


def prepare(sesh):
    sesh.headers.update({
        'User-Agent': agent,
        'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8',
        'Origin': 'https://apps.hcr.ny.gov',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Referer': 'https://apps.hcr.ny.gov/buildingsearch/default.aspx',
    })

    # request page, get session cookie
    r = sesh.get(ENDPOINT)
    soup = BeautifulSoup(r.text, LIB)
    sesh.headers.update({
        'Cookie': 'ASP.NET_SessionId=' + sesh.cookies['ASP.NET_SessionId']
    })
    time.sleep(random.uniform(0.02, 0.03))

    # poke zip code button
    param = dumb_params(soup)
    param.update({
        '__EVENTTARGET': 'ctl00$ContentPlaceHolder1$zipCodeSearchLinkButton',
        'ctl00$ContentPlaceHolder1$countyDropDown': '',
    })
    time.sleep(random.uniform(0.02, 0.03))

    r = sesh.post(ENDPOINT, data=param)
    return BeautifulSoup(r.text, LIB)


def main(county, zipcode):
    basic = {
        'ctl00$ContentPlaceHolder1$countyListDropDown': county,
        'ctl00$ContentPlaceHolder1$zipCodesDropDown': zipcode,
        '__EVENTTARGET': '',
    }

    with requests.Session() as sesh:
        print('starting', zipcode, file=sys.stderr)
        soup = prepare(sesh)

        # select county from dropdown list
        params = {
            'ctl00$ContentPlaceHolder1$countyListDropDown': county,
            'ctl00$ContentPlaceHolder1$zipCodesDropDown': '',
            '__EVENTTARGET': 'ctl00$ContentPlaceHolder1$countyListDropDown',
            '__ASYNCPOST': 'true',
            'ctl00$ContentPlaceHolder1$ScriptManager1': (
                'ctl00$ContentPlaceHolder1$ScriptManager1|'
                'ctl00$ContentPlaceHolder1$countyListDropDown'
            ),
        }
        params.update(dumb_params(soup))
        print('selecting county:', county, file=sys.stderr)
        breq = sesh.post(ENDPOINT, data=params, headers=AJAX_HEAD)
        time.sleep(random.uniform(0.02, 0.03))

        # decode parameters out of nasty nonsense
        # easiest way is to make another soup object
        soup = construct_soup(breq.text)

        params = {
            'ctl00$ContentPlaceHolder1$submitZipCodeButton': 'Submit',
        }
        params.update(basic)
        params.update(dumb_params(soup))

        req = sesh.post(ENDPOINT, data=params)

        # Sometimes page errs, sets of a chain of redirects that end nowhere interesting.
        if len(req.history) > 1:
            # import pdb; pdb.set_trace()
            raise RuntimeError("too many histories in", zipcode)

        if re.search('0 results found', req.text):
            print('0 buildings found in', zipcode, file=sys.stderr)
            return

        match = re.search(r'Displaying buildings \d+ - \d+ of (\d+)', req.text)
        print(match.groups()[0], 'buildings found in', zipcode, file=sys.stderr)

        next_button = re.search(r'value="Next"', req.text)
        soup = BeautifulSoup(req.text, LIB)

        writerows(sys.stdout, soup)

        while next_button:
            params = {
                "ctl00$ContentPlaceHolder1$ScriptManager1": (
                    "ctl00$ContentPlaceHolder1$gridUpdatePanel|"
                    'ctl00$ContentPlaceHolder1$buildingsGridView$ctl54$btnNext'
                ),
                'ctl00$ContentPlaceHolder1$buildingsGridView$ctl54$btnNext': "Next",
                '__ASYNCPOST': 'true',
            }
            params.update(basic)
            params.update(dumb_params(soup))

            req = sesh.post(ENDPOINT, data=params, headers=AJAX_HEAD)
            soup = construct_soup(req.text)

            try:
                writerows(sys.stdout, soup)

            except RuntimeError:
                print("Missing table in results for", zipcode)

            except AttributeError as e:
                raise e
                # import pdb; pdb.set_trace()

            next_button = re.search(r'value="Next"', req.text)

            time.sleep(random.uniform(0.02, 0.03))

if __name__ == '__main__':
    c, z = sys.argv[1], sys.argv[2]
    c.replace('NEWYORK', 'NEW YORK')
    main(c, z)
