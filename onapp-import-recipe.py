#!/usr/bin/python

# Import OnApp Recipe Script
# Written by Suhail Patel <suhail@onapp.com>
# Copyright 2014 - OnApp Limited 

from __future__ import print_function

import sys, argparse
import urllib, urllib2, base64
import json
import os

def import_recipe(args):
  try:
    print("> Parsing Recipe file")
    file_response = parse_recipe_file(args.recipe_file)
  except Exception as e:
    sys.exit("! Failed to load recipe due to an error: %s" % e)

  try:
    print("> Creating Recipe with label '%s'" % file_response['label'])
    base_response = create_recipe_base(args, file_response)
    recipe_response = json.load(base_response, encoding="utf-8")
  except Exception as e:
    sys.exit("! Failed to create recipe due to an error: %s" % e)

  try:
    recipe_id = recipe_response['recipe']['id']

    count = 1
    for step in file_response['steps']:
      print("> Creating Recipe Step #%d" % count)
      create_recipe_step(recipe_id, step)
      count += 1
  except Exception as e:
    sys.exit("! Failed to create recipe step due to an error: %s" % e)

  print("""
Your recipe has been imported successfully! 
Check it out at %s/recipes/%d.json""" % (args.host, recipe_id))


def parse_recipe_file(filename):
  handler = open(filename, 'r')
  data = json.load(handler)
  handler.close()

  return data


def create_recipe_base(args, recipe):
  values = {
    'recipe': {
      'label': recipe['label'],
      'description': recipe['description'],
      'compatible_with': recipe['compatible_with'],
      'script_type': recipe['script_type']
    }
  }

  url = "%s/recipes.json" % args.host
  auth = base64.encodestring('%s:%s' % (args.user, args.password))
  # Remove new line character because it's not required
  if auth[-1] == "\n": auth = auth[:-1]

  print("> - POST request to %s" % url)
  return post_request(url, auth, values)


def create_recipe_step(recipe_id, step):
  url = "%s/recipes/%d/recipe_steps.json" % (args.host, recipe_id)
  auth = base64.encodestring('%s:%s' % (args.user, args.password))[:-1]

  print("> - POST request to %s" % url)
  return post_request(url, auth, step)


def post_request(url, auth, values):
  request = urllib2.Request(url, json.dumps(values))
  request.add_header("Authorization", "Basic %s" % auth)
  request.add_header("Accept", "application/json")
  request.add_header("Content-type", "application/json")

  return urllib2.urlopen(request)

if __name__ == '__main__':
  print("""OnApp Recipe Import Script - Version 0.1
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
  parser.add_argument('user', help='OnApp Cloud Username (or email if using API token)')
  parser.add_argument('password', help='OnApp Cloud Password (or API token)')
  parser.add_argument('recipe_file', help='Recipe file to import')

  args = parser.parse_args()
  import_recipe(args)