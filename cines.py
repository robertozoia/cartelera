# encoding: utf-8

# cines.py

#
#  First release: 2012-05-02  
#
# The MIT License (MIT)
#
# Copyright (c) 2012 Roberto Zoia
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
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
    

    cadenas = build_cartelera([
        moviecrawler.MovieCrawlerUVK(), 
        moviecrawler.MovieCrawlerCMP(),
        moviecrawler.MovieCrawlerCP(),
        moviecrawler.MovieCrawlerCinepolis(),
        moviecrawler.MovieCrawlerCinerama(),
    ])

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
        doc = template.render(
            running_local=RUNNING_LOCAL, 
            compress_css_js = COMPRESS_CSS_JS,
            chains=cadenas, 
            today=tDate.strftime("%Y-%m-%d"), 
            now=tDate.strftime("%Y-%m-%d  %H:%M:%S")
        )
    
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
           

RUNNING_LOCAL = False
COMPRESS_CSS_JS = True 

if __name__ == '__main__':

    if len(sys.argv) > 1:
        if sys.argv[1] == "--dev":
            from settings.local import *
            RUNNING_LOCAL = True
            COMPRESS_CSS_JS = False
        elif sys.argv[1] == "--dev-compress":
            from settings.local import *
            RUNNING_LOCAL = True
        else:
            print("The only recognized option is --dev (runs program in development mode.)")
            sys.exit(1)
    else:
        from settings.production import * 


    main()

