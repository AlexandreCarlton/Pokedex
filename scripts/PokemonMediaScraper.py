from urllib2 import urlopen, HTTPError
from BeautifulSoup import BeautifulSoup


'''
On second thought, wouldn't it be better to make a bunch of functions,
where each one takes a game's worth of sprites.
Would account for form differences.
Yep. Do that instead.
'''

#Final pokemon number in each generation
GEN_1 = 151 # Mew
GEN_2 = 251 # Celebi
GEN_3 = 386 # Deoxys
GEN_4 = 493 # Arceus
GEN_5 = 649 # Genesect


def _save_file(url, filename):
    '''Helper function to save files- write a try/catch block once'''
    try:
        url_file = urlopen(url).read()
        with open(filename, 'w') as file:
            file.write(url_file)
    except HTTPError, e:
        print 'Unable to save', filename
    else:
        print 'Successfully saved', filename


def get_icons():
    '''Saves all Pokemon icons (the tiny sprites seen in your party or in a PC)
    to /res/drawable/ (as there are no alternatives to the sprites)
    Currently saves pngs, hopefully the B&W animated ones will be found.''' 
    
    #TODO: Grab Form-specific icons?
    for i in xrange(1, GEN_5+1):
        name = '%d.png' % i
        _save_file('http://veekun.com/dex/media/pokemon/icons/%s' % name, '../res/drawable/%s' % name)

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
    
    def footprint(self):
        '''Saves Pokemon's footprint in a .png file to ../media/footprints
        Uses Veekun'''
        footprint_url = 'http://veekun.com/dex/media/pokemon/footprints/%d.png' % self.num
        footprint_name = '../media/footprints/%03d.png' % self.num
        self._save_file(footprint_url, footprint_name)

    def emerald(self):
        '''Saves animated Emerald sprite to ../media/sprites/emerald
        Uses Veekun'''
        #Remember, only gen IV and V have gender-specific sprites
        if self.num > 386: # FIXME: Take out magic nums.
            return
        url = 'http://veekun.com/dex/media/pokemon/main-sprites/emerald/animated/%s%d.gif'
        file_name = '../media/sprites/emerald/%s/%03d.gif'

        # Grab normal sprite
        self._save_file(url % ('', self.num), file_name % ('normal', self.num))
        # Grab shiny sprite
        self._save_file(url % ('shiny/', self.num), file_name % ('shiny', self.num))

        #FIXME: Castform, Unknown,

    def black_and_white_animated(self):
        #Could also use play.pokemonshowdown.com/sprites/bwani for back sprites too

        '''Saves the B&W animated sprites
            both normal and shiny
            both male and (if exists) female 
        to ../media/sprites/black_white/{normal,shiny}
        Female pokemon have a 'f' suffix
        Uses Pokecheck'''
        #FIXME: Form differences
        #Castform (351) has hyphens of -snowy, -rainy, -sunny
        #No shiny differences in these forms.
        url_genders = ['', 'f']
        url_colours = ['i', 's']
        
        base_url = 'http://sprites.pokecheck.org/%s/%03d%s.gif'
        base_file_name = '../media/sprites/black_white/%s/%03d%s.gif' 
        
        for g in url_genders:
            for c in url_colours:
                file_name = base_file_name % ('normal' if c == 'i' else 'shiny', self.num, g)
                url = base_url % (c, self.num, g)
                
                self._save_file(url, file_name)

if __name__ == '__main__':
    get_icons()
###    bulbasaur = PokemonMediaScraper(1)
###    bulbasaur.cry()
###    bulbasaur.footprint()
###    rattata = PokemonMediaScraper(19)
###    rattata.black_and_white_animated()
###    bulbasaur.black_and_white_animated()
