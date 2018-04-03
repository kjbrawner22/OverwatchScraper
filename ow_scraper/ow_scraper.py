#regex expression
from re import search
#itemgetter for sorts
from operator import itemgetter
#request html
from urllib.request import urlopen
#url for unicode strings
from urllib.parse import quote
#html parsing
from bs4 import BeautifulSoup

class Profile(object):
	def __init__(self, battle_tag, platform='pc'):
		self.url = 'https://playoverwatch.com/en-us/career/'
		
		platforms = ['pc', 'xbl', 'psn']
		if platform not in platforms:
			raise ValueError('Invalid platform. Expected one of: %s' % platforms)
			__del__()
		else:
			self.url += platform + '/'
		
		if battle_tag is None or '#' not in battle_tag:
			raise ValueError('Battle tag expected in format: "Name#Number"')
			__del__()
		else:
			self.url += quote(battle_tag.replace(' ', '%20').replace('#', '-').encode('utf-8'))

		html = urlopen(self.url).read()
		if html.decode('utf-8').find('"code":404') != -1:
			raise ValueError("Battle tag does not exist!")
			__del__()

	def __repr__(self):
			return '<Scraper %s>' % self.battle_tag

	"""
	returns list of 2-tuples (name:string, time:string)
	for heroes sorted by time played for current competitive
	season(default) or all of quickplay
	"""
	def heroes_by_time_played(self, competitive=True):
		html = urlopen(self.url).read()
		soup = BeautifulSoup(html, "html.parser")
		
		base = ""
		if competitive:
			base = soup.find(id="competitive")
		else:
			base = soup.find(id="quickplay")

		stats_div = base.find(attrs={"data-category-id":"overwatch.guid.0x0860000000000021"})
		list = []
		for hero in stats_div.findAll(attrs={"class" : "bar-text"}):
			name = hero.find(attrs={"class":"title"}).text
			time = hero.find(attrs={"class":"description"}).text
			list.append((name, time))
		return list

	"""
	returns list of 2-tuples (name:string, wins:string)
	for heroes sorted by total wins for current competitive
	season(default) or all of quickplay
	"""
	def heroes_by_total_wins(self, competitive=True):
		html = urlopen(self.url).read()
		soup = BeautifulSoup(html, "html.parser")
		
		base = ""
		if competitive:
			base = soup.find(id="competitive")
		else:
			base = soup.find(id="quickplay")

		stats_div = base.find(attrs={"data-category-id":"overwatch.guid.0x0860000000000039"})
		list = []
		for hero in stats_div.findAll(attrs={"class" : "bar-text"}):
			name = hero.find(attrs={"class":"title"}).text
			wins = hero.find(attrs={"class":"description"}).text
			list.append((name, wins))
		return list

	"""
	returns list of 2-tuples (name:string, percent:string)
	for heroes sorted by win percentage for current competitive
	season(default) or all of quickplay
	"""
	def heroes_by_win_percentage(self, competitive=True):
		html = urlopen(self.url).read()
		soup = BeautifulSoup(html, "html.parser")
		
		base = ""
		if competitive:
			base = soup.find(id="competitive")
		else:
			base = soup.find(id="quickplay")

		stats_div = base.find(attrs={"data-category-id":"overwatch.guid.0x08600000000003D1"})
		list = []
		for hero in stats_div.findAll(attrs={"class" : "bar-text"}):
			name = hero.find(attrs={"class":"title"}).text
			percent = hero.find(attrs={"class":"description"}).text
			list.append((name, percent))
		return list

	"""
	returns list of 2-tuples (name:string, elims:string)
	for heroes sorted by average elims per life for current 
	competitive season(default) or all of quickplay
	"""
	def heroes_by_elims_per_life(self, competitive=True):
		html = urlopen(self.url).read()
		soup = BeautifulSoup(html, "html.parser")
		
		base = ""
		if competitive:
			base = soup.find(id="competitive")
		else:
			base = soup.find(id="quickplay")

		stats_div = base.find(attrs={"data-category-id":"overwatch.guid.0x08600000000003D2"})
		list = []
		for hero in stats_div.findAll(attrs={"class" : "bar-text"}):
			name = hero.find(attrs={"class":"title"}).text
			elims = hero.find(attrs={"class":"description"}).text
			list.append((name, elims))
		return list

	"""
	returns dictionary of career stats for current competitive
	season(default) or all of quickplay. when hero is not
	specified, it defaults to "ALL HEROES" option.
	NOTE: do NOT use non-ascii characters for hero names. For 
	example, "Lúcio" should be spelled "Lucio." capitalization 
	does not matter. 
	"""
	def career_stats(self, hero=None, competitive=True):
		html = urlopen(self.url).read()
		soup = BeautifulSoup(html, "html.parser")

		if hero is None:
			hero = "None"
		else:
			hero = hero.lower()
			hero.replace(" ", "")

		"""
		dict of hero names and corresponding ids
		on playoverwatch website
		"""
		heroes = {
			"None":"0x02E00000FFFFFFFF",
			"ana":"0x02E000000000013B",
			"d.va":"0x02E000000000007A",
			"genji":"0x02E0000000000029",
			"hanzo":"0x02E0000000000005",
			"lucio":"0x02E0000000000079", 
			"mercy":"0x02E0000000000004",
			"mccree":"0x02E0000000000042",
			"moira":"0x02E00000000001A2",
			"orisa":"0x02E000000000013E",
			"pharah":"0x02E0000000000008",
			"reaper":"0x02E0000000000002",
			"reinhardt":"0x02E0000000000007",
			"roadhog":"0x02E0000000000040",
			"soldier:76":"0x02E000000000006E",
			"sombra":"0x02E000000000012E",
			"symmetra":"0x02E0000000000016",
			"tracer":"0x02E0000000000003",
			"winston":"0x02E0000000000009",
			"zarya":"0x02E0000000000068",
			"zenyatta":"0x02E0000000000020"
		}

		id = ""
		if hero not in heroes.keys():
			raise ValueError("expected hero value of: %s" % heroes.keys())
		else:
			id = heroes[hero]

		base = ""
		if competitive:
			base = soup.find(id="competitive")
		else:
			base = soup.find(id="quickplay")

		stats_div = base.find(attrs={"data-category-id":id})
		list = []
		for table in stats_div.findAll("tbody"):
			for stat in table.findAll("tr"):
				row = stat.findAll("td")
				title = row[0].text
				if title.find("{") != -1:
					"""
					remove formatters(e.g.:
						{count, plural, one {game} other {games}} played)
					"""
					start = title.find("{", 1) + 1
					end = title.find("}")
					new_title = title[start:end] + "s"
					new_start = title.find("}", end+2) + 2
					new_title += title[new_start:]
					title = new_title
				description = row[1].text
				list.append((title, description))
		return list
