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

class pronoun:
	def GET(self, args):
		pronouns = args.split('/')

		print(pronouns)

		if pronouns == ['']:
			# TODO: HOMEPAGE
			return render_page.index()
		elif len(pronouns) == 1:
			# Try a built-in pronoun
			a = pronouns[0]
			for n in builtin_pronouns:
				if a == n[0]:
					pronouns = [pronoun.capitalize() for pronoun in n]
					return render_page.pronouns(pronouns=pronouns)
			
			return render_page.error(error="We don't seem to know that one! Try specifying them all, in a nominative/possesive/oblique format.")
		elif len(pronouns) == 2:
			# Try a built-in again
			a = pronouns[0]
			for n in builtin_pronouns:
				# Test the next one so that he/she works (OOPS)
				if a == n[0] and pronouns[1] == n[1]:
					pronouns = [pronoun.capitalize() for pronoun in n]
					return render_page.pronouns(pronouns=pronouns)
			
			# Two is enough to construct SOME pronouns
			pronouns = [n.capitalize() for n in pronouns]
			return render_page.pronouns(pronouns=pronouns)
		elif len(pronouns) == 3:
			pronouns = [n.capitalize() for n in pronouns]
			return render_page.pronouns(pronouns=pronouns)
		
		return render_page.error(error="You have specified too many pronouns! Try 3, in a nominative/possesive/oblique format.")

class stylesheet: # TODO: is it inefficient to serve it every time? Maybe compile the scss when ran and serve that!
	def GET(self, args):
		return compiler.compile_file(args+".scss")

class svg:
	def GET(self, args):
		return open(args+".svg").read()


if __name__ == "__main__":
	app.run()