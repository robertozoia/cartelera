#!/usr/bin/env python
# encoding: utf-8


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


if __name__=='__main__':

	import testdata_cartelera as data_cartelera
	import unify_names

	cadenas = data_cartelera.cadenas
	cadenas = unify_names.unify_names(cadenas, unify_names.get_reference_movienames(cadenas))

	data = organize_by_movie(cadenas)

	for p in data:
		print "--------------"
		print "Película: %s" % purify(p['pelicula'])

		for cadena in p['cadenas']:
			print "[%s]" % cadena['cadena']
			for cine in cadena['cines']:
				print "= %s =" % cine['cine']
				for sala in cine['salas']:
					print "%s | %s" % (p_attr(sala), p_horarios(sala))





	


