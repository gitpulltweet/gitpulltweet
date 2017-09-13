## This file imports newwf1 file functions and runs scraping for all the companies listed in here##

import newwf1

## comp is list of companies which we get from compfetch.py ##

comp = ['whiteclouds','scrap.connection.inc','the.speakeasy','bioclonetics','palmia','zipzap','fafco','rentuscom','blazntech','vodi','ridgemontoutfitters','urban.juncture','vaute','myswimpro','globechat','plantsnap','texasbeerco','kumbahealth','chicagosteakcompany','bushel','igenapps','bchi','grease.box','avuacachaca','blockchaser','lazy.tree.ranch','cigloo','chatter','retaggio','dollar.shots.club','xtractmor','nightflight','designerinc','quila.marias','asanda.air.','beachmonkey','cavu.biotherapies','oodles.corporation.2','cinemadraft']

## This function is to run scraper for multiple companies in the list above
def scrapemultiple(comp):
    for i in comp:
        print "started for comapny {}".format(i)
        prf1 = newwf1.get_investors_of_single_company(i)
        print prf1
        if (len(prf1)<=1):
            continue
        investors1 = newwf1.get_details(prf1)
        newwf1.write_investors_to_csv(investors1,i)
