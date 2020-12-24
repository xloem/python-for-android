from pythonforandroid.recipe import Recipe
from pythonforandroid.toolchain import shprint, current_directory, info
import sh
from os.path import join

class TessdataRecipe(Recipe):
    #version = '3.04.00'
    version = '4.0.0'

    url = 'https://github.com/tesseract-ocr/tessdata_fast/archive/{version}.tar.gz'
    #url = 'https://github.com/tesseract-ocr/tessdata/archive/{version}.tar.gz'
    #md5sum = 'b25e830d203af5c863081af3f684b53a'
    #sha256sum = '5dcb37198336b6953843b461ee535df1401b41008d550fc9e43d0edabca7adb1'
    md5sum = 'e7460097802be761a88f1b93e9f2349c'
    sha256sum = 'f1b71e97f27bafffb6a730ee66fd9dc021afc38f318fdc80a464a84a519227fe'

    languages = 'eng,equ,osd'

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
