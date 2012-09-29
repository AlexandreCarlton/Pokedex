from urllib2 import urlopen

from BeautifulSoup import BeautifulSoup
from HTMLParser import HTMLParser

import re

pokemon_str = u'Pok\xe9mon'

class Pokemon(object):
    '''Grabs information about the Pokemon from various databases.'''
    #FIXME: Account for different forms (see Bulbapedia for full list)
    #Luckily PokemonDB accounts for this
    
    #If a pokemon has form differences, then maybe return a dictionary where key is form, and value is the difference
        #e.g. key is origin, value is stats for origin
    #Differences include:
        #Abilities
        #Stats
        #Types
        #Body Type (ugh)
        #Height/Weight
        #Moves
    #Does not affect:
        #Color (just takes the color of its most common form; e.g. Kyurem is grey

    def __init__(self, num):
        self.num = num
        self.pokemondb_soup = BeautifulSoup(urlopen('http://pokemondb.net/pokedex/%d' % self.num))
        print 'Loaded PokemonDB'
        self.name = self.pokemondb_soup.find('div', attrs={'class' : 'navbar'}).h1.string
        
        self.psypokes_soup = BeautifulSoup(urlopen('http://psypokes.com/dex/psydex/%03d' % self.num))
        print 'Loaded Psydex'

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
            psypokes_stat_soup = BeautifulSoup(urlopen('http://www.psypokes.com/dex/psydex/%03d/stats' % self.num))
            print 'Loaded Psypokes Stats'
            bs[u'Special'] = int(psypokes_stat_soup.findAll('td', attrs={'class':'bigheaderstyle'})[4].nextSibling.nextSibling.string)  

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

    def _basic_data(self):
        '''Helper function to return the table \'Pokedex Data\''''
        return self.pokemondb_soup.find('table', attrs={'class':'vitals'}).tbody.findAll('tr')

    def height(self):
        '''Returns a tuple containing the height in feet and inches'''
        #HTML symbols are ', and " respectively; HTMLParser().unescape didn't work.
        #Could just replace both symbols and split via that
        return tuple(map(int, re.split('&#8242;|&#8243;', self._basic_data()[3].td.string)[:2]))

    def weight(self):
        return float(self._basic_data()[4].td.string.split()[0])

    def types(self):
        '''Returns a tuple of types of the Pokemon'''
        return tuple(( t.string for t in self._basic_data()[1].td.findAll('a') ))

    def abilities(self):
        '''Returns a tuple of abilities the Pokemon has:
            ( (Ability1, Ability2), HAbility)'''
        all_abilities = self._basic_data()[5]

        #found_hidden will contain either an empty list or an abilitiy enclosed within an <a/> tag
        found_hidden = all_abilities.find('small')
        hidden = found_hidden.a.string if found_hidden else None

        #Contains all abilities (including hidden if one exists)
        abilities = [ a.string for a in all_abilities.findAll('a') ]
        #If we found a hidden ability then we should exclude it from the main abilities
        if found_hidden: abilities = abilities[:-1]
        #If there is no second ability, then we set it to None
        if len(abilities) == 1: abilities = abilities + [None]

        return tuple(( tuple(abilities), hidden ))

    def _psypokes_text(self, info):
        '''Helper function to find information from psypokes page'''
        return self.psypokes_soup.find(text=info+':').parent.nextSibling.nextSibling.string

    def species(self):
        '''Returns the species of the Pokemon
        Uses Psypokes'''
        #return self._basic_data()[2].td.string #[:len(pokemon_str)]
        return self._psypokes_text('Species')

    def colour(self):
        '''Returns colour of the Pokemon
        Uses Psypokes'''
        return self._psypokes_text('Colour')

    def habitat(self):
        '''Returns the habitat of the Pokemon as dictated in FireRed/LeafGreen (Gen IV, V pokemon don't have this)
        Uses Psypokes'''
        return self._psypokes_text('Habitat') if self.num <= 386 else None
    
    #################
    #               #
    # BREEDING DATA #
    #               #
    #################

    def _breeding_data(self):
        '''Helper function to grab the breeding table'''
        return self.pokemondb_soup.findAll('table', attrs={'class':'vitals'})[1].tbody.findAll('tr')

    def egg_group(self):
        '''Returns a tuple containing the egg groups of the pokemon'''
        return tuple(( group.string for group in self._breeding_data()[0].findAll('a') ))
    
    def gender_ratio(self):
        '''Returns tuple the percentage chance of being male/female, (0,0) if pokemon is genderless'''
        #Grab second row of breeding_data, get span, then in each string split it and grab the percentage with [0] (omitting male/female), and remove the % symbol with [:-1]
        if self._breeding_data()[1].td.string == 'Genderless':
            return (0,0) #Could return 'Genderless'
        return tuple(( float(row.string.split()[0][:-1]) for row in self._breeding_data()[1].td.findAll('span') ))
        
    def egg_cycles(self):
        '''Returns the number of egg cycles needed to hatch a Pokemon
        1 egg cycle = 255 steps'''
        return int(self._breeding_data()[2].td.contents[0].strip())


    #################
    #               #
    # TRAINING DATA #
    #               #
    #################

    def _training_data(self):
        '''Helper function that gives table of relevant information for training data'''
        return self.pokemondb_soup.findAll('table', attrs={'class':'vitals'})[2].tbody.findAll('tr')

    def EV_yield(self):
        '''Returns a dictionary where each key is a stat with the value by which it increases the stat'''
        return { EV.split(' ', 1)[1] : int(EV.split(' ', 1)[0]) for EV in self._training_data()[0].td.string.split(', ') }

    def catch_rate(self):
        '''Returns the catch rate of the Pokemon (used when determining whether a pokeball thrown will catch it)'''
        return int(self._training_data()[1].td.contents[0])
    
    def base_happiness(self):
        '''Returns the base happiness of a Pokemon when it is caught'''
        return int(self._training_data()[2].td.contents[0])

    def base_exp(self):
        '''Returns the base exp of a Pokemon'''
        return int(self._training_data()[3].td.string)

    def growth_rate(self):
        '''Returns the growth rate of a pokemon- how much exp it will need to get to Lv. 100'''
        return self._training_data()[4].td.string


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

    
    #TODO
    #Movesets- dictionary for each game/generation?

if __name__ == '__main__':

    #We could always just stuff this in a __str__ method
    p = Pokemon(450)
    print p.name
    bs = p.base_stats()
    print 'Base stats:', p.base_stats()
    print 'Pokeathlon stats:', p.pokeathlon_stats()
    print 
    
    dex = p.dex_entry()
    print 'Dex entry:'
    for k, v in dex.iteritems():
        print k, ':', repr(v)
    print 
    
    print 'Species:', p.species()
    print 'Type:', ', '.join(p.types())
    print 'Colour:', p.colour()
    if p.habitat():
        print 'Habitat:', p.habitat()
    print 'Abilities:', ', '.join((a for a in p.abilities()[0] if a is not None))
    if p.abilities()[1]:
        print 'Hidden ability:', p.abilities()[1]
    print 'Height: %d\'%d"' % (p.height()[0], p.height()[1])
    print 'Weight: %.1f kg' % p.weight()
    print
    
    print 'Egg group(s):', ', '.join(p.egg_group())

    print 'Gender ratio: %.1f%% Male, %.1f%% Female' % (p.gender_ratio()[0], p.gender_ratio()[1])
    print 'Egg cycles:', p.egg_cycles(), '(%d steps)' % (p.egg_cycles()*255)
    print

    print 'EV Yield:', p.EV_yield()
    print 'Catch rate:', p.catch_rate()
    print 'Base happiness:', p.base_happiness()
    print 'Base exp:', p.base_exp()
    print 'Growth rate:', p.growth_rate()
