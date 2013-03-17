#!/usr/bin/env python
# encoding: utf-8

import copy
import Levenshtein
from tools import purify

DEBUG = True

def get_unique_movienames(theater_chain):
	"""
		Given a 'cadena' data structure, returns a set of (unique) movie names. 
	"""

	data = set()
	# We just need unique movie names, in no particular order
	
	for theater in theater_chain.theaters:
		for movie in theater.movies:
			# print '-- %s'% movie.name
			data.add(movie.name)

	return data

def get_reference_movienames(theater_chains, reference_chain_tag="UVK"):
	"""
		Uses the 'cadena de cines' as indicated by reference_tag to build a set of unique movie names,
		which other movies's names can be compared to be unified.
	"""
	result = None

	for chain in theater_chains:
		if chain.tag == reference_chain_tag:
			result = get_unique_movienames(chain)
			break

	return result

def unify_names(theater_chains, ref_movienames):
	"""
		Checks each movie name in data structure against movie names in ref_movienames.
		Uses Levenshtein for name comparison
	"""
	
	# Two movienames with Levenshtein.ratio above this number are considered equal
	# 0.8 is an empirical value based on sampled data for movie names in Perú
	LLimit = 0.8

	# Don't modify original data
	theater_chains_copy = copy.deepcopy(theater_chains)

	for ref_name in ref_movienames:
		for chain in theater_chains_copy:
			for theater in chain.theaters:
				for movie in theater.movies:
					if Levenshtein.ratio(ref_name.lower(), movie.name.lower()) >= LLimit:
						movie.name = ref_name



	# for ref_movie in ref_movienames:
	# 	for iCadena, cadena in enumerate(data):
	# 		for iCine, cine in enumerate(cadena['cines']):
	# 			for iPelicula, pelicula in enumerate(cine['cartelera']):
	# 				# l = Levenshtein.ratio(ref_movie.lower(), pelicula['pelicula'].lower())
	# 				# f.write("[%s] to %s:  %f\n" % ( purify(ref_movie), purify(pelicula['pelicula']), l ))
	# 				if Levenshtein.ratio(ref_movie.lower(), pelicula['pelicula'].lower()) >= LLimit:
	# 					data[iCadena]['cines'][iCine]['cartelera'][iPelicula]['pelicula'] = ref_movie


	return theater_chains_copy


if __name__ == '__main__':


	import testdata_cartelera as td
	from tools import purify

	chains = td.to_object()

	data = unify_names(chains, get_reference_movienames(chains))

	for chain in data:
		print "Cadena:  %s" % purify(chain.name)

		for theater in chain.theaters:
			print "-- Cine:  %s" % purify(theater.name)

			for movie in theater.movies:
				print "    * %s " % purify(movie.name)

		print "----------------------------------------\n"
		




	

	