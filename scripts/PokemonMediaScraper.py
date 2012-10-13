from urllib2 import urlopen, HTTPError
from BeautifulSoup import BeautifulSoup


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
            # We've found a Pokemon without female differences.
            pass

    def cry(self):
        '''Saves Pokemon's cry in an .ogg file to ../media/cries/
        Uses Veekun'''

        cry_url = 'http://veekun.com/dex/media/pokemon/cries/%d.ogg' % self.num
        cry_name = '../media/cries/%03d.ogg' % self.num
        self._save_file(cry_url, cry_name)


    def black_and_white_animated(self):
        '''Saves the B&W animated sprites
            both normal and shiny
            both male and (if exists) female 
        to ../media/sprites/black_white/{normal,shiny}
        Female pokemon have a 'f' suffix
        Uses Pokecheck'''
        url_genders = ['', 'f']
        url_colours = ['i', 's']
        
        base_url = 'http://sprites.pokecheck.org/%s/%03d%s.gif'
        base_file_name = '../media/sprites/black_white/%s/%03d%s.gif' # FIXME
        
        for g in url_genders:
            for c in url_colours:
                file_name = base_file_name % ('normal' if c == 'i' else 'shiny', self.num, g)
                url = base_url % (c, self.num, g)
                
                self._save_file(url, file_name)

if __name__ == '__main__':
    bulbasaur = PokemonMediaScraper(1)
    bulbasaur.cry()
    rattata = PokemonMediaScraper(19)
    rattata.black_and_white_animated()
    bulbasaur.black_and_white_animated()
