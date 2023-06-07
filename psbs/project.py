import traceback
from os import path

import jinja2
from .gister import Gister
from .config import Config
from .psparser import split_ps, get_engine
from .templatebuilder import make_template
from .utils import read_file, write_file, write_yaml, make_dir, run_in_browser


class PSBSProject:
    def __init__(self, config_filename="config.yaml"):
        self.config = Config(config_filename)

    def build(self):
        # Check for target directory
        if not path.exists("bin"):
            print("bin directory does not exist, creating one")
            make_dir("bin")

        # Build the readme.txt
        print("Writing file bin/readme.txt")
        write_file("bin/readme.txt",
                   "Play this game by pasting the script in "
                   f"{self.config['engine']}editor.html")

        # Build the script.txt
        print("Building script.txt")
        jinja_env = jinja2.Environment(
            loader=jinja2.FileSystemLoader("src"),
            autoescape=False
        )
        try:
            template = jinja_env.get_template(self.config['template'])
            source = template.render()
        except jinja2.exceptions.TemplateNotFound as err:
            print(f"Error: Unable to find template '{err}'")
            raise SystemExit(1) from err
        except jinja2.exceptions.TemplateError as err:
            print(f"Error: Unable to render template\n  {err}")
            print(traceback.format_exc().split('\n')[-4])
            raise SystemExit(1) from err

        print("Writing file bin/script.txt")
        write_file("bin/script.txt", source)

    def upload(self):
        gist_id = self.config['gist_id']
        if not self.config['gist_id']:
            print("Error: Unable to upload without a gist_id in config file")
            raise SystemExit(1)

        print("Updating gist")
        gist = Gister(gist_id)
        gist.write("bin/readme.txt")
        gist.write("bin/script.txt")

    def run(self, editor=False):
        print("Opening in browser")
        if editor:
            url_string = "editor.html?hack="
        else:
            url_string = "play.html?p="
        run_in_browser(self.config['engine']+url_string+self.config['gist_id'])

    @staticmethod
    def create(project_name, gist_id=None, file=None):
        src_directory = f"{project_name}/src/"
        bin_directory = f"{project_name}/bin/"

        source = ""
        engine = "https://www.puzzlescript.net/"

        if gist_id:
            print("Downloading data from gist")
            gist = Gister(gist_id)
            source = gist.read("script.txt")
            engine = get_engine(gist.read("readme.txt"))

        if file:
            source = read_file(file)

        src_tree = split_ps(source)

        print("Building directory structure")
        make_dir(project_name)
        make_dir(src_directory)
        make_dir(bin_directory)

        print("Creating config file")
        write_yaml(f"{project_name}/config.yaml", {
            'gist_id': gist_id,
            'engine': engine,
            'template': "main.pss"})

        print("Creating template file")
        write_file(f"{src_directory}/main.pss", make_template(src_tree))

        print("Creating source files")
        for section in src_tree:
            for index, src_content in enumerate(src_tree[section]):
                if index == 0:
                    index = ""
                src_filename = f"{section}{index}.pss"
                write_file(src_directory+src_filename, src_content)
