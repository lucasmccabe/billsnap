from bs4 import BeautifulSoup
import requests
import re
from typing import List


class SnapScrape():
    '''Scrapes US legislative data. Is very handsome.'''

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
            LookupError: if summary cannot be found on congress.gov page

        Example Usage:
            >>> bill = SnapScrape('house', 183, 113)
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

        Example usage:
            >>> bill = SnapScrape('house', 183, 113)
            >>> print(bill.get_title())
            Veterans Dog Training Therapy Act
        '''
        page_content = BeautifulSoup(
                requests.get(self.url).content, 'html.parser'
            )

        for line in page_content.find_all('h1'):
            if 'legDetail' in str(line):
                line = line.text
                congress_label = re.findall(str(self.congress)+'\w+ Congress', line)[0]

                if self.chamber == 'house':
                    chamber_label = 'H.R.%s' %str(self.bill)
                if self.chamber == 'senate':
                    chamber_label = 'S.%s' %str(self.bill)

                title = line[len(chamber_label)+3:line.index(congress_label)]

                return title
        return None

    def get_summary(self) -> str:
        '''
        Gets bill summary from congress.gov page.

        Example usage:
            >>> bill = SnapScrape('house', 183, 113)
            >>> print(bill.get_summary())
            Veterans Dog Training Therapy Act - Directs the Secretary of
            Veterans Affairs to carry out a pilot program for assessing the
            effectiveness of addressing post-deployment mental health and
            post-traumatic stress disorder symptoms [...]
        '''
        url_summary = self.url + '/summary'
        page_content = BeautifulSoup(
                requests.get(url_summary).content, 'html.parser'
            )

        paras = page_content.find_all('p')

        for i in range(len(paras)):
            if 'summary' in paras[i].text:
                return paras[i+1].text
        return None

    def get_policy_areas(self) -> List:
        '''
        Gets the bill's corresponding policy area term(s). Returns a list of
        policy terms.

        Example usage:
            >>> bill = SnapScrape('house', 183, 113)
            >>> print(bill.get_policy_areas())
            ['Armed Forces and National Security']
        '''
        policy_vocab = ['Agriculture and Food',
                        'Animals',
                        'Armed Forces and National Security',
                        'Arts, Culture, Religion',
                        'Civil Rights and Liberties, Minority Issues',
                        'Commerce',
                        'Congress',
                        'Crime and Law Enforcement',
                        'Economics and Public Finance',
                        'Education',
                        'Emergency Management',
                        'Energy',
                        'Environmental Protection',
                        'Families',
                        'Finance and Financial Sector',
                        'Foreign Trade and International Finance',
                        'Government Operations and Politics',
                        'Health',
                        'Housing and Community Development',
                        'Immigration',
                        'International Affairs',
                        'Labor and Employment',
                        'Law',
                        'Native Americans',
                        'Public Lands and Natural Resources',
                        'Science, Technology, Communications',
                        'Social Sciences and History',
                        'Social Welfare',
                        'Sports and Recreation',
                        'Taxation',
                        'Transportation and Public Works',
                        'Water Resources Development']

        url_policy = self.url + '/subjects'
        page_content = BeautifulSoup(
                requests.get(url_policy).content, 'html.parser'
            )

        policy_areas = [] #TODO: identify if a bill can have more than one policy term.
        for link in page_content.find_all('li'):
            if any(policy==link.text for policy in policy_vocab):
                policy_areas.append(link.text)
        if policy_areas:
            return policy_areas
        else:
            return [None]

    def get_text_url(self) -> str:
        '''
        Gets url for congress.gov link to full bill text.
        '''
        url_text = self.url + '/text'
        page_content = BeautifulSoup(
                requests.get(url_text).content, 'html.parser'
            )

        for link in page_content.find_all(href=True):
            if 'XML/HTML (new window)' in link.text:
                return 'https://www.congress.gov' + link['href']
        return None

    def get_text(self) -> str:
        '''
        Gets full text of a bill. Format is readable, but not guaranteed to
        be pretty.

        Returns:
            Full bill text, if available. Returns None if there is no XML/HTML
            link available.
        '''
        if self.get_text_url():
            page_content = BeautifulSoup(
                    requests.get(self.get_text_url()).content, 'html.parser'
                )

            bill_text = ''
            for item in page_content.find_all([
                'section', 'subsection', 'paragraph', 'subparagraph'
                ]):
                bill_text += item.text.replace('\n\t\t\t', '')
            return bill_text
        #TODO: consider earhing the TXT or PDF if no XML/HTML is available
        return None

    def get_sponsor(self) -> str:
        '''
        Gets the name of a bill's sponsor.

        Example usage:
            >>> bill = SnapScrape('house', 183, 113)
            >>> print(bill.get_sponsor())
            Rep. Grimm, Michael G. [R-NY-11]
        '''
        page_content = BeautifulSoup(
                requests.get(self.url).content, 'html.parser'
            )

        for link in page_content.find_all('a', href=True):
            if '/member/' in link['href'] or \
                    'Sen.' in link.text or 'Rep.' in link.text:
                return link.text
        return None

    def get_cosponsors(self) -> List:
        '''
        Gets the names of a bill's cosponsors (does not include the sponsor).
        '''
        cosponsors_url = self.url + '/cosponsors'
        page_content = BeautifulSoup(
                requests.get(cosponsors_url).content, 'html.parser'
            )

        sponsor = self.get_sponsor()
        cosponsors = []
        for link in page_content.find_all('a', href=True):
            if ('/member/' in link['href'] or \
                    'Sen.' in link.text or 'Rep.' in link.text) and \
                    link.text != sponsor:
                cosponsors.append(link.text)
        if cosponsors:
            return cosponsors
        else:
            return [None]

    def get_rollcall(self) -> List:

        actions_url = self.url + '/actions'
        page_content = BeautifulSoup(
                requests.get(actions_url).content, 'html.parser'
            )
        for link in page_content.find_all('a', href=True):
            if 'Roll no' in link.text:
                #reading House votes involves scraping XML
                print('House Vote')
            if 'Record Vote' in link.text:
                print('Senate Vote')
