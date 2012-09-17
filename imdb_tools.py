# encoding: utf-8

import copy
import operator

import imdb
import tools


def pick_movie_from_imdb_results(movies):
	"""
	Expects movies to be a list of imdb movies, as returned by IMDbPY search_movie function.
	Returns a movie object
	"""

	DEBUG = False

	# Only one movie, no work to do
	if len(movies) == 1:
		return movies

	result = None
	#
	# Rule 1:  pick current year movie
	#
	import datetime
	today_year = datetime.date.today().year

	tmp = []

	# Pick this year's movies
	for m in movies:
		try:
			if m['year'] == today_year:
				tmp.append(m)
		except KeyError:
			pass

	# If no movies of this year, try last year
	if len(tmp) == 0:
		for m in movies:
			try:
				if m['year'] == today_year-1:
					tmp.append(m)
			except KeyError:
				pass

	# Check if match found
	if len(tmp) == 1:
		result = tmp[0]


	# sort movie objects by year
	# movies = sorted(movies.iteritems(), key=operator.itemgetter('year'))

	return result



def fetch_imdb_data(theater_chains):

	DEBUG = False

	movie_cache = {}
	idb = imdb.IMDb()

	chains_work_copy = copy.deepcopy(theater_chains)

	for theater_chain in chains_work_copy: 
		for theater in theater_chain.theaters:
			for movie in theater.movies:

				if DEBUG: print "Processing %s..." % tools.purify(movie.name)

				if movie.name not in movie_cache.keys():

					if DEBUG: print "-- movie not in cache"
					
					imdb_m = idb.search_movie(movie.name)

					if len(imdb_m) == 1:
						m = imdb_m[0]
					else:
						m = pick_movie_from_imdb_results(imdb_m)

					if m is not None:
						if DEBUG: print "-- hit found in imdb"
						# fetch additional data from imdb
						idb.update(m)

						# add data to movie cache
						if DEBUG:  print "Adding %s to movie cache" % tools.purify(movie.name)

						movie_cache[movie.name] = m

						if DEBUG:  print "Cache keys: %s" % movie_cache.keys()
					else:
						if DEBUG:  print "Couldn't find exact entry for %s in imdb." % tools.purify(movie.name)


				if movie.name in movie_cache.keys():
					try:
						movie.imdb_rating = movie_cache[movie.name]['rating']
						movie.imdb_canonical_title = movie_cache[movie.name]['canonical title']
					except KeyError:
						# if there is no key for this movie, then imdb does not have data (strange case)
						if DEBUG:  print "No Key for %s." % movie.name
						movie.imdb_rating = 0
				else:
					movie.imdb_rating = 0

					

	return chains_work_copy

