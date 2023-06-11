# PSBS

The PuzzleScript Build System!

PSBS combines multiple files into one puzzlescript source file and uploads it to the web.

This is an early development release and changes may be made to the project structure and config file formats in the future.

## Features

 - Compile PuzzleScript games from many files using Jinja2 templates
 - Import images and spritesheets directly into your PuzzleScript game
 - Load existing PuzzleScript projects right from their gists
 - Load existing PuzzleScript projects from a source text file
 - Save PuzzleScript projects to gists
 - Launch your project from play.html or the PuzzleScript editor
 - Supports most PuzzleScript forks including [Pattern:Script](https://github.com/ClementSparrow/Pattern-Script)
 - Use your favorite version control for your PuzzleScript Projects

## Installing

If you already have Python 3.8 or greater and pip installed simply run the following command from your terminal

`pip install psbs`

If you don't have Python and pip installed: [Download Python](https://www.python.org/downloads/)

## Connecting to GitHub

PSBS will build your projects into PuzzleScript source without interacting with GitHub at all, however uploading and running your projects requires an authorization token.

By default PSBS will attempt to run `gh auth token` to recieve an authorization token from the GitHub command line tool.  If you would like to use a different token or prefer not to install the GitHub command line tool you can run the following command.

`psbs token insert_your_token_here`

## Usage

Enter `psbs` into your terminal to get a list of commands

Commands:

`psbs new` Creates a new project
`psbs build` Builds the project in the current working directory
`psbs upload` Builds project then uploads it to gist
`psbs run` Builds project, uploads it, then runs it in your web browser

For more information on these commands and to see available flags enter `psbs help `*`command`*

## CLI Example

    psbs new myProject
    cd myProject
    psbs build


---

# Getting To Know Your PSBS Project

## Project Structure

    ├── config.yaml
    ├── bin
    │   ├── script.txt    (These files are generated by build command)
    │   └── readme.txt
    └── src
        ├── collisionlayers.pss    (Default template files)
        ├── legend.pss             (you can organize your project's templates however you like)
        ├── levels.pss
        ├── main.pss
        ├── objects.pss
        ├── prelude.pss
        ├── rules.pss
        ├── sounds.pss
        └── wincondition.pss


## Config.yaml

At the root of your project you will find a file called config.yaml containing configuration variables for your project

- engine: the url of the fork you are using, by default https://www.puzzlescript.net/
- gist_id: the id of the gist the upload and run commands should use to store this project in
- template: the name of your root template file, by default main.pss

## Templates

PSBS uses Jinja2, a fast, expressive, extensible templating engine, to build your PuzzleScript project.  To learn more about all of the features available to you check out the Jinja2 [Template Designer Documentation](https://jinja.palletsprojects.com/en/3.1.x/templates/).

To avoid conflicting with valid PuzzleScript code, the Jinja2 Tags have been changed as follows:

(% blocks %) (( variables )) (# comments #)

## Images

A helper function has been added to the template environment `Image(filename)` that will import an image file directly into your game as a PuzzleScript object!

    Target
    ((image("images/target.png")))

Additionally, this helper function contains the following optional parameters (alpha=False, max_colors=10, x=0, y=0, width=None, height=None)

- alpha: (true/false) if true will include the RGBA alpha values for transparency supported by some forks
- max_colors: (int) maximum colors in output object, PuzzleScript can only handle 10 by default but some forks such as Pattern:Script support up to 36 colors
- x: (int) horizontal position in image to start importing from
- y: (int) vertical position in image to start importing from
- width: (int) width of the object to import, if None set to the width of the image file
- height: (int) height of the object to import, if None set to the height of the image file

By using the last four parameters listed one can load objects from a single image as a spritesheet.

    (% set directions = ["down","left","up","right"] %) (# Can be placed in your main template #)
    (% for dir in directions %)
    Player_((dir))
    ((image("images/player.png",x=loop.index0*5,width=5,height=5)))
    (% endfor %)