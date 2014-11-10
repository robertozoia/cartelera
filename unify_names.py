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
	#theater_chains_copy = copy.deepcopy(theater_chains)

	for ref_name in ref_movienames:
		for chain in theater_chains:
			for theater in chain.theaters:
				for movie in theater.movies:
					if Levenshtein.ratio(ref_name.lower(), movie.name.lower()) >= LLimit:
						movie.name = ref_name
			
	return theater_chains

		




	

	