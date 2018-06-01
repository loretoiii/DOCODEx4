import nltk
from nltk import bigrams
#from nltk.tokenize import word_tokenize
from nltk.util import ngrams


class ngramas(object):
    def __new__(cls,input_list,n):
        #print(str(texto))
        lista_engrama = list()

        #enegrams = ngrams(texto.split(), n)
        #for grams in enegrams:
         #   lista_engrama.append(grams)


        #n_grams = ngrams(word_tokenize(texto), n)
        #return[' '.join(grams) for grams in n_grams]

        #input_list = ['all', 'this', 'happened', 'more', 'or', 'less']

        #print("zip ngramas-->")
        #print(str(zip(*[input_list[i:] for i in range(n)])))
        #lista_engrama=(zip(input_list, input_list[1:]))
        return zip(*[input_list[i:] for i in range(n)])
