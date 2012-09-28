from urllib2 import urlopen

from BeautifulSoup import BeautifulSoup
from HTMLParser import HTMLParser

import re

pokemon_str = u'Pok\xe9mon'

class Pokemon(object):
    '''Grabs information about the Pokemon from various databases.'''
        
    
    def __init__(self, num):
        self.num = num
        self.pokemondb_soup = BeautifulSoup(urlopen('http://pokemondb.net/pokedex/%d' % self.num))
        print 'Loaded PokemonDB'
        self.name = self.pokemondb_soup.find('div', attrs={'class' : 'navbar'}).h1.string
        

    ##############
    #            #
    # STATISTICS #
    #            #
    ##############


    def base_stats(self):
        '''Returns a dictionary of the base stats of a pokemon
        Includes the special stat if the pokemon is in gen I'''
        
        #Grab the table with class base-stats, then grab all the trs in it.
        stat_table = self.pokemondb_soup.find('table', attrs={'class':'base-stats'}).tbody.findAll('tr')
        bs = { row.th.string : int(row.td.string) for row in stat_table }
        
        #if the pokemon was part of Gen I, then it has a special stat too.
        if self.num <= 151:
            #Load psypokes especially for this, 
            psypokes_soup = BeautifulSoup(urlopen('http://www.psypokes.com/dex/psydex/%03d/stats' % self.num))
            print 'Loaded Psypokes'
            bs[u'Special'] = int(psypokes_soup.findAll('td', attrs={'class':'bigheaderstyle'})[4].nextSibling.nextSibling.string)  

        return bs
    
    def pokeathlon_stats(self):
        '''Returns a dictionary of the pokeathlon stats of the pokemon
        Each item in the tuple (the value of the dictionary) represents the min, base, and max stats, respectively.'''
        stats = {}
        star = '&#x2605;' #Unicode character for the star (used on the site)
        #Grab table with vitals wide class, and grab rows in it
        stat_table = self.pokemondb_soup.find('table', attrs={'class':'vitals wide'}).tbody.findAll('tr')
        for row in stat_table:
            #Count the stars in each tag, but the tag is empty then we replace it with the empty string so as not to break the program
            min_stat = (row.td.findAll('span', attrs={'class':'pkthln-stars min'})[0].string or "").count(star)
            base_stat = min_stat + (row.td.findAll('span', attrs={'class':'pkthln-stars base'})[0].string or "").count(star)
            max_stat = base_stat + (row.td.findAll('span', attrs={'class':'pkthln-stars max'})[0].string or "").count(star)
            stats[row.th.string] = (min_stat, base_stat, max_stat)
        return stats
    

    ##############
    #            #
    # BASIC DATA #
    #            #
    ##############

    def basic_data(self):
        '''Helper function to return the table \'Pokedex Data\''''
        return self.pokemondb_soup.find('table', attrs={'class':'vitals'}).tbody.findAll('tr')

    def height(self):
        '''Returns a tuple containing the height in feet and inches'''
        #HTML symbols are ', and " respectively; HTMLParser().unescape didn't work.
        #Could just replace both symbols and split via that
        return tuple(map(int, re.split('&#8242;|&#8243;', self.basic_data()[3].td.string)[:2]))

    def weight(self):
        return float(self.basic_data()[4].td.string.split()[0])

    def types(self):
        '''Returns a tuple of types of the Pokemon'''
        return tuple(( t.string for t in self.basic_data()[1].td.findAll('a') ))

    def species(self):
        '''Returns the species of the Pokemon'''
        #global pokemon_str
        return self.basic_data()[2].td.string #[:len(pokemon_str)]

    def abilities(self):
        '''Returns a tuple of abilities the Pokemon has:
            ( (Ability1, Ability2), HAbility)'''
        all_abilities = self.basic_data()[5]
        abilities = (( a.string for a in all_abilities.td.findAll('a')[:-1] ))
        hidden = all_abilities.td.small.a.string
        return tuple(( tuple(abilities), hidden ))
    
    
    #################
    #               #
    # BREEDING DATA #
    #               #
    #################

    def breeding_data(self):
        '''Helper function to grab the breeding table'''
        return self.pokemondb_soup.findAll('table', attrs={'class':'vitals'})[1].tbody.findAll('tr')

    def egg_group(self):
        '''Returns a tuple containing the egg groups of the pokemon'''
        return tuple(( group.string for group in self.breeding_data()[0].findAll('a') ))
    
    def gender_ratio(self):
        '''Returns the percentage chance of breeding a male pokemon'''
        return float(self.breeding_data()[1].td.span.string.split()[0][:-1])/100

    def egg_cycles(self):
        '''Returns the number of egg cycles needed to hatch a Pokemon
        1 egg cycle = 255 steps'''
        return int(self.breeding_data()[2].td.contents[0].strip())

    ######################
    #                    #
    # GAME-SPECIFIC DATA #
    #                    #
    ######################

    def dex_entry(self):
        '''Returns a dictionary containing the Pokedex entries of each game of the Pokemon'''
        #Grab the table with dex entries, which has class flavors
        dex_table = self.pokemondb_soup.find('table', attrs={'class':'flavors'}).tbody.findAll('tr')
        #For every row in the dex_table, and hen for every game in that row, set the game to the row entry.
        return { game: row.td.string for row in dex_table for game in row.th.getText(' ').split() }


if __name__ == '__main__':
    p = Pokemon(1)
    print p.name
    bs = p.base_stats()
    print bs
    dex = p.dex_entry()
    for k, v in dex.iteritems():
        print repr(k), ':', repr(v)

    print repr(p.species())
    print repr(p.types())
    print p.abilities()
    print repr(p.height())
    print repr(p.weight())

    print p.pokeathlon_stats()

    print p.egg_group()
    print p.gender_ratio()
    print p.egg_cycles()
