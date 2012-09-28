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
        self.name = self.pokemondb_soup.find('div', attrs={'class' : 'navbar'}).h1.string

        self.bulbapedia_soup = BeautifulSoup(urlopen('http://bulbapedia.bulbagarden.net/wiki/%s_(Pokemon)' % self.name))

    def base_stats(self):
        '''Returns a dictionary of the base stats of a pokemon
        Includes the special stat if the pokemon is in gen I'''
        
        #Grab the table with class base-stats, then grab all the trs in it.
        stat_table = self.pokemondb_soup.find('table', attrs={'class':'base-stats'}).tbody.findAll('tr')
        bs = { row.th.string : int(row.td.string) for row in stat_table }
        
        #if the pokemon was part of Gen I, then it has a special stat too.
        if self.num <= 151:
            #Find text with ' base stat in ', and then grab the bold sibling.
            bs['Special'] = int(self.bulbapedia_soup.find(text=' base stat in ').parent.b.string)
        
        return bs
        
    def dex_entry(self):
        '''Returns a dictionary containing the Pokedex entries of each game of the Pokemon'''
        #Grab the table with dex entries, which has class flavors
        dex_table = self.pokemondb_soup.find('table', attrs={'class':'flavors'}).tbody.findAll('tr')
        #For every row in the dex_table, and hen for every game in that row, set the game to the row entry.
        return { game: row.td.string for row in dex_table for game in row.th.getText(' ').split() }


    def basic_data(self):
        '''Helper function to return the table \'Pokedex Data\''''
        return self.pokemondb_soup.find('table', attrs={'class':'vitals'}).tbody.findAll('tr')

    def height(self):
        '''Returns a tuple containing the height in feet and inches'''
        #HTML symbols are ', and " respectively; HTMLParser().unescape didn't work.
        #Could just replace both symbols and split via that
        return tuple(map(int, re.split('&#8242;|&#8243;', self.basic_data()[3].td.string)[:2]))

    def weight(self):
        return self.basic_data()[4].td.string


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
        return tuple( (( tuple(abilities), hidden )) )
    
    

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
