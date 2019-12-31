from bs4 import BeautifulSoup
import requests
import re


class BillSnap():
    '''BillSnap is an easier way to get US legislative data.'''

    def __init__(self, chamber:str, bill:int, congress:int = 115):
        '''
        Constructor for the BillSnap class.

        Params:
            chamber: Chamber of Congress. Must be House or Senate.
            bill: The bill number, e.g. H.R.5537
            congress: Congressional session number
            url: the congress.gov url for the bill
        Raises:
            AttributeError: if chamber is invalid
            LookupError: if url does not correspond to an existing bill

        Example Usage:
            >>> bs = BillSnap('house', 183, 113)
            >>> print(bs.title)
            Veterans Dog Training Therapy Act
        '''

        self.congress = congress
        self.chamber = chamber.lower()
        self.bill = bill
        self.url = self.generate_url()

        if self.chamber not in ['house', 'senate']:
            raise AttributeError('Chamber must be House or Senate.')

        if self.congress < 93:
            raise AttributeError(
                'BillSnap is not supported for this congressional session.'
                )

        if not self.bill_exists():
            raise LookupError('Bill not found.')

        self.title = self.get_title()
        self.summary = self.get_summary()


    def generate_url(self) -> str:
        '''
        Generates a congress.gov url for a given bill. The url may or may not
        actually exist.
        '''
        url = 'https://www.congress.gov/bill/%s/%s-bill/%s' %(
                    str(self.congress),
                    self.chamber,
                    str(self.bill)
                )

        return url

    def bill_exists(self) -> bool:
        '''
        Checks if a bill exits by searching for 'Page Not Found' on corresponding
        congress.gov page.
        '''
        page_content = BeautifulSoup(
                requests.get(self.url).content, 'html.parser'
            )

        for header in page_content.find_all('h1'):
            if 'page not found' in header.text.lower():
                return False

        return True

    def get_title(self) -> str:
        '''
        Gets bill title from congress.gov page.
        '''

        page_content = BeautifulSoup(
                requests.get(self.url).content, 'html.parser'
            )

        for line in page_content.find_all('h1'):
            if 'legDetail' in str(line):
                break

        line = line.text
        congress_label = re.findall(str(self.congress)+'\w+ Congress', line)[0]

        if self.chamber == 'house':
            chamber_label = 'H.R.%s' %str(self.bill)
        if self.chamber == 'senate':
            chamber_label = 'S.%s' %str(self.bill)

        title = line[len(chamber_label)+3:line.index(congress_label)]

        return title

    def get_summary(self) -> str:
        '''
        Gets bill summary from congress.gov page.
        '''
        url_summary = self.url + '/summary'
        page_content = BeautifulSoup(
                requests.get(url_summary).content, 'html.parser'
            )

        paras = page_content.find_all('p')

        for i in range(len(paras)):
            if 'summary' in paras[i].text:
                return paras[i+1].text

        return [p.text for p in paras]
