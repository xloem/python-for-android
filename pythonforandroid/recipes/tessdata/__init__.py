from pythonforandroid.recipe import Recipe
from pythonforandroid.logger import shprint
from pythonforandroid.util import current_directory
from multiprocessing import cpu_count
import os
import sh

class TessdataRecipe(Recipe):
    version = '3.04.00'
    url = 'https://github.com/tesseract-ocr/tessdata/archive/{version}.tar.gz'
    md5sum = 'b25e830d203af5c863081af3f684b53a'
    sha256sum = '5dcb37198336b6953843b461ee535df1401b41008d550fc9e43d0edabca7adb1'

    languages = ['eng,equ,osd']

    def postbuild_arch(self, arch):
        super().postbuild_arch(arch)

        env = self.get_recipe_env(arch)
        languages = env.get('TESSDATA_LANGS', self.languages).split(',')

        install_dir = join(self.ctx.get_python_install_dir(), 'share', 'tessdata')

        info('Copying tesseract traineddata files for ' + ', '.join(languages))
        shprint(sh.mkdir, '-p', install_dir)
        with current_directory(self.get_build_dir(arch.arch)):
            shprint(sh.cp, '-a',
                *('{}.traineddata'.format(lang) for lang in languages),
                install_dir)


recipe = TessdataRecipe()
