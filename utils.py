from bs4 import BeautifulSoup
import requests
import re
from typing import List, Dict

def get_member_IDs() -> Dict:
    '''
    Creates a dictionary of Member IDs and names by scraping Congress.gov's
    Member Bioguide.
    '''

    id_link = 'https://www.congress.gov/help/field-values/member-bioguide-ids'
    page_content = BeautifulSoup(
            requests.get(id_link).content, 'html.parser'
        ).get_text(separator=' ')

    member_content = re.findall(r'.*[A-Z][0-9]{6}', page_content)[0]

    member_IDs = re.findall(r'[A-Z][0-9]{6}', member_content)
    member_IDs_indices = [member_content.index(member_ID) for member_ID in member_IDs]

    member_dict = {}
    for i in range(len(member_IDs_indices)):
        if i==0:
            member_dict[member_IDs[i]] = member_content[:member_IDs_indices[i]-1]
        else:
            member_dict[member_IDs[i]] = member_content[member_IDs_indices[i-1]+8:member_IDs_indices[i]-1]

    return member_dict
