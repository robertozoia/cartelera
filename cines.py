#!/home/pajarraco/.pythonbrew/pythons/Python-2.7.3/bin/python
# encoding: utf-8


#
#  2012-05-2:  first release
#  (c) 2012 by Roberto Zoia


#
# Printing functions
#
import sys, os
import re
import string
import codecs
from datetime import datetime
import time
from pprint import pprint as pp

from jinja2 import Environment, FileSystemLoader

import moviecrawler

from tools import purify, ppchains

import multithread
import unify_names
import organize_by_movie




DEBUG = False


def do_processing(args):
    
    if DEBUG: start = time.time()   
    if DEBUG: print "Thread Start:  %s" % args['tag'] 
    
    args['theater_chain_movies'] = args['class'].getTheaterChainMovies()

    if DEBUG: print "Thread End: %s  - Elapsed Time: %s" % (args['tag'], (time.time() - start) )


def build_cartelera(theater_chains):

    result = []
    
    for chain in theater_chains:
        result.append(
            { 'tag': chain.tag, 'class': chain }
        )
        
    mt = multithread.MultiThread( do_processing, result )
    
    mt.start()
    mt.join()
        
    r = []

    for t in result:
        if 'theater_chain_movies' in t: r.append(t['theater_chain_movies'])
    
    return r

    
def main():
    

    cadenas = build_cartelera([moviecrawler.MovieCrawlerUVK(), 
        moviecrawler.MovieCrawlerCMP(), moviecrawler.MovieCrawlerCP()])

    # Unify movie names
    cadenas = unify_names.unify_names(cadenas, unify_names.get_reference_movienames(cadenas))
    

    # init Jinja templates
    env = Environment(loader=FileSystemLoader(template_dir))
    tDate = datetime.now()

    render_list = [
        (bycine_template, bycine_file),
        (settings_template, settings_file),
        (about_template, about_file),
    ]
    
    for tfile, ofile in render_list:
        template = env.get_template(tfile)
        doc = template.render(chains=cadenas, today=tDate.strftime("%Y-%m-%d"), now=tDate.strftime("%Y-%m-%d  %H:%M:%S"))
    
        try:        
            f = codecs.open(ofile, 'w', 'utf-8-sig')
            f.write(doc)
            f.close()
        except:
            # log exception
            import traceback
            f = open(logfile, 'w')
            traceback.print_exc(file = f)
            f.close()
           
        

if __name__ == '__main__':

    if len(sys.argv) > 1:
        if sys.argv[1] == "--dev":
            from settings.local import *
    else:
        from settings.production import * 


    main()

