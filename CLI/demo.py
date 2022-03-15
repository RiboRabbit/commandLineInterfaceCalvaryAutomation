from time import sleep
from main_classes import CalvarySession, NoSponsorFoundException


s = CalvarySession()

while(True):
	verify = input("Type 'yes(or)y' to contine: ")
	if not (verify == "yes" or verify == "y" or verify == 'Y' or verify == "YES"):
		break
		
	keyword = input("Type Sonsor (Number): ")

	try:
	    sponsor = s.get_sponsors_full_details(keyword=keyword)
	    print(sponsor)
	except NoSponsorFoundException as e:
	    print("has no user")
	    pass    