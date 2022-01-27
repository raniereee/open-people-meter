import pickle

def read(fname):

	'''
	f = open(fname, 'rb')

	hlist = []
	try:
		hlist = pickle.load(f)
	except EOFError:
		print "Deu EOFError - Tamanho de hlist: ", len(hlist)
		
	f.close()
	'''

	hlist = []
	try:
		with open(fname, "rb") as f:
			hlist = pickle.load(f)
	except:
		print "*** Erro ao ler hashe file %s***" % fname

	return hlist 


