from scrapers.fb import facebook_scraper
from scrapers.g import google_scraper
from config import locations
import csv
import sys

if __name__ == "__main__":
    Dance_type = sys.argv[1]
    fields = ["DANCE_TYPE","EventID","Url","Title","Date","Address","Latitude","Longitude","City","Image","Description"]
    f = open(f'{Dance_type}_events.csv','w')
    csvwriter = csv.writer(f)
    csvwriter.writerow(fields)
    try:
        for c in locations:  
            print("##################################################")
            print(f"Scraping for {c}")
            print("##################################################")
            google_rows = google_scraper(Dance_type,c)
            csvwriter.writerows(google_rows)
            facebook_rows = facebook_scraper(Dance_type,c)
            csvwriter.writerows(facebook_rows)
    except KeyboardInterrupt:
        sys.exit()
    except Exception as e:
        print(e)
        print('Some error occured.')
    finally:
        f.close()

        