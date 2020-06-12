from billsnap import Scrape
import re
import utils

bill = Scrape('house', 5430, 116)
print(bill.get_sponsor())
print(bill._get_house_vote('http://clerk.house.gov/evs/2019/roll701.xml')[0])


#print(utils.get_member_IDs())
