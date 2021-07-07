# mypronoun.is clone, that lets you define custom terms
# Because a closed-off request database isn't very helpful for self-expression

import web

urls = (
	'/(.*)', 'pronoun'
)
app = web.application(urls, globals())

builtin_pronouns = [
	["he", "him", "his"],
	["she", "her", "hers"],
	["they", "them", "theirs"],
	["it", "that", "its"] # Neo
]

class pronoun:
	def GET(self, name):
		pronouns = name.split('/')

		if len(pronouns) == 0:
			# TODO: HOMEPAGE
			return "Welcome to pronounisland"
		elif len(pronouns) == 1:
			# Try a built-in pronoun
			a = pronouns[0]
			for n in builtin_pronouns:
				if a == n[0]:
					return ', '.join(n)
			
			return "Pronoun not found, qualify more!"
		elif len(pronouns) == 2:
			# Try a built-in again
			a = pronouns[0]
			for n in builtin_pronouns:
				if a == n[0]:
					return ', '.join(n)
			
			# Two is enough to construct pronouns
			return TODO
		elif len(pronouns) == 3:
			return ', '.join(pronouns)
		
		return "Too many qualifiers."

if __name__ == "__main__":
	app.run()