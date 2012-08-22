# -*- coding:utf-8 -*-
from haystack.backends.elasticsearch_backend import ElasticsearchSearchEngine as BaseEngine
from haystack.backends.elasticsearch_backend import ElasticsearchSearchBackend as BaseBackend

# Il faut qu'il soit dans la config pour pouvoir le tester
# mais pour le moment (31/07) il lui manque le franch stemmer


class ElasticsearchSearchBackend(BaseBackend):
    """
      A essayer aussi une config avec un stemmer snowball. De la forme
      {
        "index" : {
            "analysis" : {
                "analyzer" : {
                    "my_analyzer" : {
                        "tokenizer" : "standard",
                        "filter" : ["standard", "lowercase", "my_snow"]
                    }
                },
                "filter" : {
                    "my_snow" : {
                        "type" : "snowball",
                        "language" : "Lovins"
                    }
                }
            }
        }
    }

    et aussi

     {"index":{
      "analysis":{
         "analyzer":{
            "francais":{
               "type":"custom",
               "tokenizer":"standard",
               "filter":[
                  "lowercase",
                  "stop_francais",
                  "fr_stemmer",
                  "asciifolding",
                  "elision"
               ]
            },
          },
         "filter":{
            "stop_francais":{
               "type":"stop",
               "stopwords":[
                  "_french_"
               ]
            },
            "fr_stemmer":{
               "type":"stemmer",
               "name":"french"
            },
            "elision":{
               "type":"elision",
               "articles":[
                  "l",
                  "m",
                  "t",
                  "qu",
                  "n",
                  "s",
                  "j",
                  "d"
               ]
            }
         }
      }
   }
} 



   Une autre config pour autocomplete : qui surement plu adaptée au francais aussi que celle 
   par defaulft de HayStack. Et oui.... car autocomplete sur"vet" ne marche pas alors qu'il
   marche sur "vêt"... Il faut aumoins ajouter asciifolding et lower
    {
   "index":{
      "analysis":{
         "analyzer":{
            "autocomplete":{
               "tokenizer":"whitespace",
               "filter":[
                  "asciifolding",
                  "lowercase",
                  "autocomplete"
               ]
            }
         },
         "filter":{
            "autocomplete":{
               "type":"edgeNGram",
               "min_gram":"2",
               "max_gram":"15",
               "side":"front"
            }
         }
      }
   }
} 

    """



    FR_ANALYZER_SNOW = {
        "type": "snowball",
        "language": "French",
        'stopwords': ['_french_', 'voiture']
    }

    FR_ANALYZER = {
        'type': 'custom',
        'tokenizer': 'standard',
        'filter': ["lowercase", "stop_francais", "fr_stemmer", "asciifolding", "elision"],
        # 'stopwords': ["mais", "des", "elle", "d"]  # ne sert à rien avec un analyser de type custom
    }

    FR_STEMMER = {
        "type": "stemmer",
        "name": "french"
    }

    FR_STOP = {
        'type': 'stop',
        'stopwords': ['_french_', 'voiture']   # les defaults, mais on doit pouvoir mixer les deux
     }

    ELISION = {
        "type": "elision",
        "articles": ["l", "m", "t", "qu", "n", "s", "j", "d"]
    }


    # TODO: on pourra en simplifier un peu, je me suis servie de ce code pour 
    # tester diverses analyzer de ES. Celui qui me semble le mieux correspondre a mon cas
    # et celui de "fr"
    def __init__(self, connection_alias, **connection_options):
        # self.DEFAULT_SETTINGS['settings']['analysis']['analyzer']['snow_fr'] = self.FR_ANALYZER_SNOW
        self.DEFAULT_SETTINGS['settings']['analysis']['analyzer']['fr'] = self.FR_ANALYZER
        self.DEFAULT_SETTINGS['settings']['analysis']['filter']['fr_stemmer'] = self.FR_STEMMER
        self.DEFAULT_SETTINGS['settings']['analysis']['filter']['stop_francais'] = self.FR_STOP
        self.DEFAULT_SETTINGS['settings']['analysis']['filter']['elision'] = self.ELISION

        # autocomplete or french
        self.DEFAULT_SETTINGS['settings']['analysis']['analyzer']['ngram_analyzer']['filter'] = \
            self.DEFAULT_SETTINGS['settings']['analysis']['analyzer']['edgengram_analyzer']['filter'].append('asciifolding')

        super(ElasticsearchSearchBackend, self).__init__(connection_alias, **connection_options)


    # def setup(self, **kwargs):
    #     print "ENTER MY setUp %s" % self.DEFAULT_SETTINGS
    #     super(ElasticsearchSearchBackend, self).setup(**kwargs)


    def build_schema(self, fields):
        content_field_name, mapping = super(ElasticsearchSearchBackend, self).build_schema(fields)
 
        # change 'snowball' with 'fr'
        for field, params in mapping.items():
            if 'analyzer' in params and params['analyzer'] == 'snowball':
                params['analyzer'] = 'fr'
        return (content_field_name, mapping)




class ElasticsearchSearchEngine(BaseEngine):
    backend = ElasticsearchSearchBackend
