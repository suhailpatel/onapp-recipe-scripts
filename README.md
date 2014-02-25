# OnApp Recipe Import/Export Scripts

## Exporting Recipes

The export script (**onapp-export-recipe.py**) can be executed as follows:

    python onapp-export-recipe.py <host> <user> <pass> <recipe-id>

An example of this command to download Recipe ID 20 from the http://mycloud.com OnApp Control Panel:

  python onapp-export-recipe.py http://mycloud.com admin password 20
    
This will create a file titled `20.recipe.json`. 

## Importing Recipes

The import script (**onapp-import-recipe.py**) can be executed as follows:

    python onapp-import-recipe.py <host> <user> <pass> <recipe-file>

An example of this command to upload a recipe file `20.recipe.json` to the  http://mycloud.com OnApp Control Panel:

  python onapp-import-recipe.py http://mycloud.com admin password 20.recipe.json
    
This will import the recipe from the file `20.recipe.json`. Please note, Recipe labels need to be unique. You may get a 422 Unprocessible Entity error if you try to import a recipe which has the same label as an existing recipe.

## Requirements

These scripts have been tested on Python 2.7.5 running on Mac OSX. They don't have any external dependencies beyond Python and should work on any system. 

## License

> IN NO EVENT UNLESS REQUIRED BY APPLICABLE LAW OR AGREED TO IN WRITING WILL ANY COPYRIGHT HOLDER, OR ANY OTHER PARTY WHO MODIFIES AND/OR CONVEYS THE PROGRAM AS PERMITTED ABOVE, BE LIABLE TO YOU FOR DAMAGES, INCLUDING ANY GENERAL, SPECIAL, INCIDENTAL OR CONSEQUENTIAL DAMAGES ARISING OUT OF THE USE OR INABILITY TO USE THE PROGRAM (INCLUDING BUT NOT LIMITED TO LOSS OF DATA OR DATA BEING RENDERED INACCURATE OR LOSSES SUSTAINED BY YOU OR THIRD PARTIES OR A FAILURE OF THE PROGRAM TO OPERATE WITH ANY OTHER PROGRAMS), EVEN IF SUCH HOLDER OR OTHER PARTY HAS BEEN ADVISED OF THE POSSIBILITY OF SUCH DAMAGES.
