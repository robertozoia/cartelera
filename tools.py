# encoding: utf-8

OUTPUT_CODEC = 'utf-8'
def purify(s):
	return s.encode(OUTPUT_CODEC)


def mkdirp(self, d):
	if not os.path.isdir(d):
		os.makedirs(d)

def ppchains(cadenas):

	for chain in cadenas:
		print '+++++++++'
		for theater in chain.theaters:
			print '-----'
			for movie in theater.movies:
				print movie.name