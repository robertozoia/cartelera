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

from jinja2 import Environment, FileSystemLoader

import cine
from tools import purify

import multithread
import unify_names
import organize_by_movie



DEBUG = False


def do_processing(args):
	
	if DEBUG: start = time.time()

	# t, tag, cine = args
	
	if DEBUG: print "Thread Start:  %s" % args['tag'] 
	
	args['cines'] = args['class'].get_cartelera_cines_de_cadena()
	
	if DEBUG: print "Thread End: %s  - Elapsed Time: %s" % (args['tag'], (time.time() - start) )


def build_cartelera(cadenas):
	"""
		Devuelve la cartelera en el siguiente formato:
		[{ 'cadena':  'UVK Multicines', 'tag': 'UVK', 
			'locales':
				[ 	'cine': u'UVK Platino Basadre', 
				 	'cartelera': 
						[{  'pelicula': 'Sólo por dinero', 
							'horarios': [ u'9:45', '11:00' ]
						},
						[{  'pelicula': 'Los patitos feos', 
							'horarios': [ u'9:45', '11:00' ]
						},
						[{  'pelicula': 'El chanchito con alas', 
							'horarios': [ u'9:45', '11:00' ]
						},
				
					]
				], 
				[ 	'cine': u'UVK Larcomar', 
				 	'cartelera': 
						[{  'pelicula': 'Sólo por dinero', 
							'horarios': [ u'9:45', '11:00' ]
						},
						[{  'pelicula': 'Los patitos feos', 
							'horarios': [ u'9:45', '11:00' ]
						},
						[{  'pelicula': 'El chanchito con alas', 
							'horarios': [ u'9:45', '11:00' ]
						},
				
					]
				]
				
		}]
	
	
	"""
	
	result = []
	
	for cadena in cadenas:
		result.append(
			{ 'cadena': cadena.cadena, 'tag': cadena.tag, 'url': cadena.url, 'class': cadena , 'cines' : [] }
		)
		
	mt = multithread.MultiThread( do_processing, result )
	
	mt.start()
	mt.join()
		
	for c in result:
		del c['class']
	
	return result

	
def main(devmode=False):
	
	# if devmode, don't fetch data from the internet
	# use local fake data	
	if devmode == True:
		import testdata_cartelera as data
		cadenas = data.cadenas
	else:
		cadenas = build_cartelera( [cine.CineUVK(), cine.CineCMP(), cine.CineCP()])

	# Unify movie names
	cadenas = unify_names.unify_names(cadenas, unify_names.get_reference_movienames(cadenas))

	# organize by movies
	peliculas = organize_by_movie.organize_by_movie(cadenas)


	# init Jinja templates
	env = Environment(loader=FileSystemLoader([server_template_dir, development_template_dir]))
	tDate = datetime.now()

	# Render by-cine page
	template = env.get_template(bycine_template)
	doc = template.render(cadenas=cadenas, today=tDate.strftime("%Y-%m-%d"), now=tDate.strftime("%Y-%m-%d  %H:%M:%S"))

	# write page to file	
	try:		
		f = codecs.open(bycine_file, 'w', 'utf-8-sig')
		f.write(doc)
		f.close()
	except:
		# log exception
		import traceback
		f = open(logfile, 'w')
		traceback.print_exc(file = f)

	#  Render by-movie page
	template = env.get_template(bymovie_template)
	doc = template.render(peliculas=peliculas, today=tDate.strftime("%Y-%m-%d"), now=tDate.strftime("%Y-%m-%d  %H:%M:%S"))

	# write page to file
	try:		
		f = codecs.open(bymovie_file, 'w', 'utf-8-sig')
		f.write(doc)
		f.close()
	except:
		import traceback
		f = open(logfile, 'w')
		traceback.print_exc(file = f)



if __name__ == '__main__':

	
	# deployment dependent settings
	basedir = "/home/pajarraco/carteleraperu.com"

	if not os.path.exists(basedir):
		# local development
		basedir = "./www"

	server_template_dir = '/home/pajarraco/bin/cines/templates'
	development_template_dir = './templates'

	# non deployment dependent settings
	bycine_file =  "%s/index.html" % basedir
	bymovie_file = "%s/bymovie.html" % basedir

	bycine_template = "cines.html"
	bymovie_template = "movies.html"

	logfile = "traceback.log"

	devmode = False
	if len(sys.argv) > 1:
		if sys.argv[1] == "--nofetch":
			devmode = True

	main(devmode)

