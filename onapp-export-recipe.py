#!/usr/bin/python

# Export OnApp Recipe Script
# Written by Suhail Patel <suhail@onapp.com>
# Copyright 2014 - OnApp Limited 

from __future__ import print_function

import sys, argparse
import urllib2, base64
import json
import os

def export_recipe(args):
  try:
    print("> Attempting to grab recipe")
    response = request_recipe(args)
  except Exception as e:
    sys.exit("! Failed to grab recipe from server due to an error: %s" % e)

  try:
    print("> Parsing Recipe JSON")
    recipe = json.load(response, encoding="utf-8")
  except Exception as e:
    sys.exit("! Could not load JSON recipe due to an error: %s" % e)

  try:
    recipe_export = parse_recipe(recipe)

    filename = '%s.recipe.json' % args.recipe
    if os.path.isfile(filename):
      raise Exception("File '%s' already exists" % filename)

    print("> Saving Recipe to file '%s'" % filename)
    save_recipe(recipe_export, filename)
  except Exception as e:
    sys.exit("! Could not export recipe due to an error: %s" % e)

  print("""
Your recipe has been exported to '%s'! 
Share your recipe on the OnApp forums (http://forum.onapp.com)""" % filename)

def parse_recipe(recipe):
  recipe = recipe['recipe']
  print("> Processing Recipe '%s'" % recipe['label'])

  info = {
    'label': recipe['label'],
    'description': recipe['description'],
    'compatible_with': recipe['compatible_with'],
    'script_type': recipe['script_type'],
    'steps': recipe['recipe_steps']
  }

  for element in info['steps']:
    step = element['recipe_step']
    step.pop("recipe_id", None)
    step.pop("id", None)
    step.pop("created_at", None)
    step.pop("updated_at", None)

  return info

def save_recipe(recipe_export, filename):
  with open(filename, 'w') as out:
    json.dump(recipe_export, out, encoding="utf-8")

def request_recipe(args):
  url = "%s/recipes/%d.json" % (args.host, args.recipe)
  print("> - Connecting to %s" % url)

  auth = base64.encodestring('%s:%s' % (args.user, args.password))
  # Remove new line character because it's not required
  if auth[-1] == "\n": auth = auth[:-1]

  request = urllib2.Request(url)
  request.add_header("Authorization", "Basic %s" % auth)   
  return urllib2.urlopen(request)


if __name__ == '__main__':
  print("""OnApp Recipe Export Script - Version 0.1
Developed by Suhail Patel <suhail@onapp.com>
Copyright OnApp Limited 2014

IN NO EVENT UNLESS REQUIRED BY APPLICABLE LAW OR AGREED TO IN 
WRITING WILL ANY COPYRIGHT HOLDER, OR ANY OTHER PARTY WHO 
MODIFIES AND/OR CONVEYS THE PROGRAM AS PERMITTED ABOVE, BE 
LIABLE TO YOU FOR DAMAGES, INCLUDING ANY GENERAL, SPECIAL, 
INCIDENTAL OR CONSEQUENTIAL DAMAGES ARISING OUT OF THE USE OR 
INABILITY TO USE THE PROGRAM (INCLUDING BUT NOT LIMITED TO LOSS 
OF DATA OR DATA BEING RENDERED INACCURATE OR LOSSES SUSTAINED 
BY YOU OR THIRD PARTIES OR A FAILURE OF THE PROGRAM TO OPERATE 
WITH ANY OTHER PROGRAMS), EVEN IF SUCH HOLDER OR OTHER PARTY 
HAS BEEN ADVISED OF THE POSSIBILITY OF SUCH DAMAGES.
""")

  parser = argparse.ArgumentParser(description='Export your OnApp Recipes quickly and easily to use with the OnApp Import Recipe Script.')
  parser.add_argument('host', help='Hostname of the cloud (eg. http://myonappcloud.test.com)')
  parser.add_argument('user', help='OnApp Cloud Username (or email if using API token')
  parser.add_argument('password', help='OnApp Cloud Password (or API token)')
  parser.add_argument('recipe', type=int, help='Recipe ID in the URL bar of the recipe you want to export (eg. http://myonappcloud.test.com/recipes/9 means an ID of 9)')

  args = parser.parse_args()
  export_recipe(args)