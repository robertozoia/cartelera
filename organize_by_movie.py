# encoding: utf-8

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

from tools import purify
from operator import itemgetter


DEBUG = True

def organize_by_movie(cadenas):
	"""
		Converts a "cadenas" structure to a "movie" structure.
	"""
	return prune(restructure_by_movie(cadenas))


def restructure_by_movie(cadenas):

	result = []

	for cadena in cadenas:
		for cine in cadena['cines']:
			for pelicula in cine['cartelera']:
				data = {
					'pelicula': pelicula['pelicula'],
					'cadena': cadena['cadena'],
					'cine': cine['cine'],
					'horarios':  pelicula['horarios'],
					'isSubtitulada': pelicula['isSubtitulada'],
					'isDoblada': pelicula['isDoblada'],
					'is3D': pelicula['is3D'],
					'isHD': pelicula['isHD'],
				}


				result.append(data)

	return result


def p_attr(p):
	r = ""

	if p['isSubtitulada']:	r = r + "[SUB] "
	if p['isDoblada']: r = r + "[DOB] "
	if p['isHD']: r = r + "[HD] "
	if p['is3D']: r = r + "[3D] "
	return r.strip()

def p_horarios(p):
	return " ".join(p['horarios'])


def lineofdata(data):
	for d in data:
		yield(d)

def filter_by_key(data, key, match):
	"""
		Returns all the elements from a list of dictionaries that match the specified criteria
	"""
	result = []
	for d in data:
		if d[key] == match:
			result.append(d)
	return result

def prune(data):


	#  We need a resulting data structure like this one:
	# 	new_data.append({
	# 		'pelicula': uPel,
	# 		'cadena': uCad,
	# 		'cines' : [ { data for pelicula} ]
	# 	})
	#  
	#  Ordenamos la lista por película
	#  Esto funciona porque los nombres de las películas han sido unificados antes

	new_data = []

	data = sorted(data, key=itemgetter('pelicula'))
	
	#  build a list of unique movie names and sort it
	tmp = set()
	for p in data:
		tmp.add(p['pelicula'])

	unique_movienames = list(tmp)
	unique_movienames.sort()


	# find matches of movies for each unique movie
	for uPel in unique_movienames:
		tmp = sorted(
				filter_by_key(data, 'pelicula', uPel),
				key=itemgetter('cadena')
			)

		# build a list of unique cadenas for this movie
		unique_cadenas = set()
		for t in tmp:
			unique_cadenas.add(t['cadena'])

		# build a list of cines for each cadena
		tmpCadenas = []
		for uCad in unique_cadenas:
			# get movies for each cadena
			tmpCines = sorted(
				filter_by_key(tmp, 'cadena', uCad),
				key=itemgetter('cine')
			)

			# build a list of unique cines for this cadena
			unique_cines = set()
			for t in tmpCines:
				unique_cines.add(t['cine'])

			# build a list of salas for this movie in this cine
			tmpSalas = []
			for uCine in unique_cines:
				tmpSalas.append({
					'cine':  uCine,
					'salas': sorted(
					filter_by_key(tmpCines, 'cine', uCine),
					key=itemgetter('isSubtitulada'))
				})

			tmpCadenas.append({
				'cadena': uCad,
				'cines': tmpSalas
				})

		new_data.append({
			'pelicula': uPel,
			'cadenas': tmpCadenas,
			})

	return new_data






	


