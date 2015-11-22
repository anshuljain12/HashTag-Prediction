import csv
import json
from StringIO import StringIO
import urllib2
import sys

reload(sys)
sys.setdefaultencoding('utf-8')


def get_geo_information():
    f = open('remaining_lat_lon.txt', 'r')
    fw = open('found_lat_lon.txt', 'a')
    reader=csv.reader(f,delimiter='\t')
    for lat, lon in reader:
        data = json.load(urllib2.urlopen('http://maps.googleapis.com/maps/api/geocode/json?latlng='+lat+','+lon+'&sensor=true'))
        if data['status'] == 'OK':
            print lat+'\t'+lon
            city = ''
            cityShort = ''
            state = ''
            stateShort = ''
            country = ''
            countryShort = ''
            postalcode = ''
            for address in data['results'][0]['address_components']:
                if(len(address['types'])>0):
                    if(address['types'][0]=='administrative_area_level_2'):
                        city = address['long_name']
                        cityShort = address['short_name']
                    if(address['types'][0]=='administrative_area_level_1'):
                        state = address['long_name']
                        stateShort = address['short_name']
                    if(address['types'][0]=='country'):
                        country = address['long_name']
                        countryShort = address['short_name']
                    if(address['types'][0]=='postal_code'):
                        postalcode = address['long_name']
            fw.write(lat+'\t'+lon+'\t'+city+'\t'+cityShort+'\t'+state+'\t'+stateShort+'\t'+country+'\t'+countryShort+'\t'+postalcode+'\n')
    f.close()
    fw.close()


def create_dictionary():
    dict = {}
    f = open('found_lat_lon.txt', 'r')
    reader = csv.reader(f, delimiter='\t')
    for r in reader:
        dict[r[0]+'\t'+r[1]] = r[2]+'\t'+r[3]+'\t'+r[4]+'\t'+r[5]+'\t'+r[6]+'\t'+r[7]+'\t'+r[8]
    f.close()
    return dict


def map_values(dict):
    remaining =[]
    with open('f_hashtag_prediction/data for student.txt', 'r') as f:
        reader = csv.reader(f, delimiter='\t')
        with open('geo_result.txt', 'w') as fw:
            fw.write("id\tlatitude\tlongitude\tcity\tcity_short\tstate\tstateShort\tcountry\tcountryShort\tpostalcode\n")
            for id, tweet, latitude, longitude in reader:
                if float(latitude) != 0:
                    if latitude+'\t'+longitude in dict:
                        fw.write(id+'\t'+latitude+'\t'+longitude+'\t'+dict[latitude+'\t'+longitude]+'\n')
                    else:
                        remaining.append(latitude+'\t'+longitude)
    unique = set(remaining)
    fw = open('remaining_lat_lon.txt', 'w')
    count = 0
    for x in unique:
        fw.write(x+'\n')
        count = count + 1
    print 'Remaining latitude/longitude = ' + str(count)
    fw.close()


def main():
    #get_geo_information()
    dict = create_dictionary()
    map_values(dict)


main()