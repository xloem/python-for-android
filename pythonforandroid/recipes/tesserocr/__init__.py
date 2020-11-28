from pythonforandroid.recipe import CythonRecipe
# import os


class TesserOCRRecipe(CythonRecipe):
    version = '2.5.1'
    url = 'https://github.com/sirfz/tesserocr/archive/v{version}.tar.gz'
    name = 'tesserocr'

    md5sum = '01a4da9d957d132f449f81e3c2416d1a'
    sha256sum = 'ffcc772e76ed40b8d1da4b6f074e940865b525b6454d99253e91c3e7bff872e1'

    depends = ['tesseract', 'Pillow']
    call_hostpython_via_targetpython = False

    # def get_recipe_env(self, arch=None, with_flags_in_cc=True):
    #     env = super().get_recipe_env(arch, with_flags_in_cc)
    #     env['CPFLAGS'] = env.get('CPPFLAGS', '') + ' -I' + os.path.join(
    #         self.get_recipe('tesseract', self.ctx).get_build_dir(arch.arch),
    #     )


recipe = TesserOCRRecipe()
