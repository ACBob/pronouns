# mypronoun.is clone, that lets you define custom terms
# Because a closed-off request database isn't very helpful for self-expression

import web
from web.contrib.template import render_jinja
from scss import compiler

urls = (
	'/(.*)\.css', 'stylesheet', # Preprocesses the stylesheet with sass
	'/(.*)\.svg', 'svg', # returns the svg
	'/(.*)', 'pronoun'
)
app = web.application(urls, globals())

builtin_pronouns = [
	["he", "him", "his"],
	["she", "her", "her"],
	["they", "them", "their"],

	# Commonly used neopronouns, from a list that claimed 'he' was a neopronoun
	["e", "em", "eir"],
	["per", "per", "pers"],
	["ve", "ver", "vis"],
	["ze", "hir", "hir"],
	["zie", "hir", "hir"]
]

render_page = render_jinja('pages', encoding='utf-8')

def test_pronouns(nouns):
	a = nouns[0]
	for n in builtin_pronouns:
		if a == n[0]:
			if len(nouns) > 1:
				if not nouns[1] == n[1]:
					continue
			
			return [[pronoun.capitalize() for pronoun in n]]
	
	return None

class pronoun:
	def GET(self, args):
		pronouns = args.split('/')

		if pronouns == ['']:
			# TODO: HOMEPAGE
			return render_page.index()
		elif '&&' in args:
			a = [] # The new list
			b = [] # Current List working on
			for p in pronouns:
				g = test_pronouns([p])
				if not g is None:
					a.append(g[0])
					b = []
					continue

				if p == "&&":
					if len(b) > 0:
						a.append(b)
						b = []
					continue

				b.append(p)
			if len(b) > 0:
				a.append(b)

			print(a)
			
			return render_page.pronouns(pronouns=a)
		elif len(pronouns) == 1:
			# Try a built-in pronoun
			a = test_pronouns(pronouns)
			if not a is None:
				return render_page.pronouns(pronouns=a)
			
			return render_page.error(error="We don't seem to know that one! Try specifying them all, in a nominative/possesive/oblique format.")
		elif len(pronouns) == 2:
			# Try a built-in again
			a = test_pronouns(pronouns)
			if not a is None:
				return render_page.pronouns(pronouns=a)
			
			# Two is enough to construct SOME pronouns
			pronouns = [n.capitalize() for n in pronouns]
			return render_page.pronouns(pronouns=[pronouns])
		elif len(pronouns) == 3:
			pronouns = [n.capitalize() for n in pronouns]
			return render_page.pronouns(pronouns=[pronouns])
		elif not "&&" in pronouns:
				return render_page.error(error="You have specified too many pronouns! Try 3, in a nominative/possesive/oblique format.<br>If you wish to have another set, seperate it with &&.")



class stylesheet: # TODO: is it inefficient to serve it every time? Maybe compile the scss when ran and serve that!
	def GET(self, args):
		return compiler.compile_file(args+".scss")

class svg:
	def GET(self, args):
		return open(args+".svg").read()


if __name__ == "__main__":
	app.run()