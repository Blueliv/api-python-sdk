# -*- coding: utf8 -*-

import logging
import sys
import os
import json
from optparse import OptionParser
from datetime import datetime

try:
    import pygal
    from pygal.style import *
    from sdk.blueliv_api import BluelivAPI
except:
    print 'You don\'t have the required libraries:'
    print 'Blueliv sdk and pygal'
    sys.exit()

serv_type = ['MALWARE', 'C_AND_C', 'BACKDOOR', 'EXPLOIT_KIT']

custom_style = Style(
  background='transparent',
  plot_background='#FFFFFF',
  foreground='#AAAAAA',
  foreground_light='#000000',
  foreground_dark='#072720',
  opacity='.8',
  opacity_hover='1',
  transition='200ms ease-in',
  colors=( '#00b388','#0093b2','#072720','#ff585d','#ffd100'))


def getData():
    print 'Downloading data...'
    proxy = None
    # Write your api token here
    token_api = ""
    if token_api == '':
        print 'In order to get the data from our api, you need a valid token! Remember to change the variable token_api (line 39) in the script.'
        sys.exit(0)
    api = BluelivAPI(base_url='https://freeapi.blueliv.com',
                     token=token_api,
                     log_level=logging.INFO,
                     proxy=proxy)

    response = api.crime_servers.online()
    if not response.updated_at:
        print "Last updated date could not be retrieved. Maybe rate limit exceeded?"
        sys.exit()

    return response.items

def getStatistics(crimeservers):
    print 'Getting statistics...'
    stats = dict()
    stats['country'] = count('country',crimeservers)
    for x in serv_type:
        stats['top_ip_'+x] = count_by_date(get_types(crimeservers, x))

    return stats

def paint(stats, seed_name):

    print 'Printing graphs...'

    country_dict = dict()

    try:
        for key in stats['country']:
            country_dict[key.lower()] = stats['country'][key]

        world_chart = pygal.Worldmap(width=1080, style=custom_style)
        world_chart.title = 'Malicious server by country'
        world_chart.add('Infected countries', country_dict)
        world_chart.render_to_file('{}_wm.svg'.format(seed_name))
    except Exception as err:
        print "An error ocurred: {}".format(err)
        sys.exit()
    print 'Worldmap generated at: {}'.format('{}_wm.svg'.format(seed_name))

    try:
        bar_chart = pygal.Bar(style=custom_style)
        bar_chart.title = 'Crimeserver endurance (in hours)'
        for x in serv_type:
            bar_chart.add(x,stats['top_ip_'+x])
        bar_chart.render_to_file('{}_bar.svg'.format(seed_name))
    except Exception as err:
        print "An error ocurred: {}".format(err)
        sys.exit()
    print 'Bar graph generated at: {}'.format('{}_bar.svg'.format(seed_name))

def count(field, crimeservers):
    t_count = dict()
    for cs in crimeservers:
        if field in cs:
            if cs[field] in t_count:
                t_count[cs[field]] += 1
            else:
                t_count[cs[field]] = 1
    return t_count

def count_by_date(crimeservers):
    t_count = dict()
    for cs in crimeservers:
        first = datetime.strptime(cs['firstSeenAt'],"%Y-%m-%dT%H:%M:%S+0000")
        last = datetime.strptime(cs['lastSeenAt'],"%Y-%m-%dT%H:%M:%S+0000")
        uptime = last - first
        if 'ip' in cs:
            t_count[cs['ip']] = int(uptime.total_seconds()/3600)
    tmp_list = sorted(t_count, key=t_count.get)[-10:]
    sorted_list = list()
    for x in tmp_list:
        sorted_list.append({'label':x,'value':t_count[x]})
    return sorted_list

def get_types(crimeservers, type_cs):
    tmp_list = list()
    for cs in crimeservers:
        if cs['type']==type_cs:
            tmp_list.append(cs)
    return tmp_list

if __name__ == "__main__":
    
    logging.basicConfig(filename='blueliv.log')
    logger = logging.getLogger('main')

    date_string = datetime.now().strftime("%Y%m%d_%H.%M")

    usage = 'usage: %prog -u [-d] or %prog -i filename [-d]'
    parser = OptionParser(usage=usage)
    parser.add_option("-u", "--update",dest="update",help="Download new information on crimeservers. Remember that you can only do this once a day.", action='store_true',default=False)
    parser.add_option("-d", "--dir",dest="dir",help="Output directory to store the downloaded crimeservers data and the generated graphs.", metavar="DIRECTORY", default="blueliv_reports")
    parser.add_option("-i", "--input",dest="filename",help="File to read the crimeserver information used to draw the graphs.", metavar="FILE")
    (options, args) = parser.parse_args()
    
    if not os.path.isdir(options.dir):
        try:
            os.makedirs(options.dir)
        except Exception as err:
            print "An error ocurred creating output directory: {}".format(options.dir)
            print "Error message: {}".format(err)
            sys.exit()
    elif not os.access(options.dir, os.W_OK):
        print "An error ocurred, I don't have permissions to write in {}".format(options.dir)
        sys.exit()
   
    file_graphs = os.path.join(options.dir,date_string)
   
    if options.filename:
        filename = options.filename
        if not os.path.isfile(filename) or not os.access(filename, os.W_OK):
            print "An error ocurred, file '{}' does not exist or I don't have permissions to write it".format(filename)
            sys.exit()
        print "Reading from: {}".format(filename)
        file_graphs = os.path.join(options.dir,(filename.split(os.sep)[-1].split('-')[0]))
        try:
            with open(filename,'r') as crime_file:
                crimeservers = json.loads(crime_file.read())
        except Exception as err:
            print "An error ocurred: {}".format(err)
            sys.exit()  
        
    elif options.update:
        # Do update 
        print "Updating"
        filename= "{}-csdata.blv".format(date_string)
        filename=os.path.join(options.dir,filename)
        if os.path.isfile(filename) and os.access(filename, os.W_OK):
            print "The file '{}' already exists or I don't have permissions to write it".format(filename)
            sys.exit()

        try:
            crimeservers = getData()
            with open(filename,'w') as crime_file:
                json.dump(crimeservers,crime_file)
        except Exception as err:
            print "An error ocurred: {}".format(err)
            sys.exit()
        print 'Created crimeserver file: {}'.format(filename)

    else:
        print "Error on argument, use '-h' to get help"
        sys.exit()
    stats = getStatistics(crimeservers)
    paint(stats,file_graphs)
