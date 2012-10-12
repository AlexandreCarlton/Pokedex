from urllib2 import urlopen, HTTPError, URLError

class PokemonMediaScraper(object):
    '''Scrapes sprites and cries from the web and saves them to
        ../media'''
        
    def __init__(self, num):
        self.num = num

    def _save_file(self, url, filename):
        '''Helper function to save files- write a try/catch block once'''
        try:
            url_file = urlopen(url).read()
            with open(filename, 'w') as file:
                file.write(url_file)
        except HTTPError, e:
            print 'Unable to retrieve', url, 'due to HTTP Error', e.code 
        except URLError, e:
            print 'Unable to retrive', url, 'due to URL Error', e.code

    def cry(self):
        cry_url = 'http://veekun.com/dex/media/pokemon/cries/%d.ogg' % self.num
        cry_name = '../media/cries/%03d.ogg' % self.num
        self._save_file(cry_url, cry_name)

    def black_and_white_animated(self):
        '''Saves the B&W animated sprites 
        both male and (if exists) female'''
        # TODO

    def black_and_white_shiny_animated(self):
        '''Saves the B&W animated shiny sprites
        both male and (if exists) female'''
        # TODO


if __name__ == '__main__':
    bulbasaur = PokemonMediaScraper(2)
    bulbasaur.cry()

