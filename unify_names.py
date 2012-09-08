#!/usr/bin/env python
# encoding: utf-8

import copy
import Levenshtein
from tools import purify

DEBUG = True

def get_unique_movienames(cadena):
	"""
		Given a 'cadena' data structure, returns a set of (unique) movie names. 
	"""

	data = set()
	# We just need unique movie names, in no particular order
	for cine in cadena['cines']:
		for pelicula in cine['cartelera']:
			data.add(pelicula['pelicula'])

	return data

def get_reference_movienames(cadenas, reference_tag="UVK Multicines"):
	"""
		Uses the 'cadena de cines' as indicated by reference_tag to build a set of unique movie names,
		which other movies's names can be compared to be unified.
	"""
	result = None
	for cadena in cadenas:
		if cadena['cadena'] == reference_tag:
			result = get_unique_movienames(cadena)
			break
	return result

def unify_names(cadenas, ref_movienames):
	"""
		Checks each movie name in data structure against movie names in ref_movienames.
		Uses Levenshtein for name comparison
	"""
	
	# Two movienames with Levenshtein.ratio above this number are considered equal
	# 0.8 is an empirical value based on sampled data for movie names in Perú
	LLimit = 0.8

	# Don't modify original data
	data = copy.deepcopy(cadenas)

	for ref_movie in ref_movienames:
		for iCadena, cadena in enumerate(data):
			for iCine, cine in enumerate(cadena['cines']):
				for iPelicula, pelicula in enumerate(cine['cartelera']):
					# l = Levenshtein.ratio(ref_movie.lower(), pelicula['pelicula'].lower())
					# f.write("[%s] to %s:  %f\n" % ( purify(ref_movie), purify(pelicula['pelicula']), l ))
					if Levenshtein.ratio(ref_movie.lower(), pelicula['pelicula'].lower()) >= LLimit:
						data[iCadena]['cines'][iCine]['cartelera'][iPelicula]['pelicula'] = ref_movie
	# f.close()
	return data


if __name__ == '__main__':


	import testdata_cartelera as data_cartelera

	cadenas = data_cartelera.cadenas
	data = unify_names(cadenas, get_reference_movienames(cadenas))

	print data

	