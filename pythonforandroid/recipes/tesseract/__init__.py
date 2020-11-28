from pythonforandroid.recipe import Recipe
from pythonforandroid.logger import shprint
from pythonforandroid.util import current_directory
from multiprocessing import cpu_count
import os
import sh


class TesseractRecipe(Recipe):
    version = '3.05.02'
    url = 'https://github.com/tesseract-ocr/tesseract/archive/{version}.tar.gz'
    md5sum = 'd3b8661f878aed931cf3a7595e69b989'
    sha256sum = '494d64ffa7069498a97b909a0e65a35a213989e0184f1ea15332933a90d43445'

    depends = ['libleptonica']
    built_libraries = {'libtesseract.so': os.path.join('api', '.libs')}

    def get_recipe_env(self, arch, with_flags_in_cc=True):
        env = super().get_recipe_env(arch, with_flags_in_cc)
        env['PKG_CONFIG_PATH'] = os.path.join(
            self.get_recipe('libleptonica', self.ctx).get_build_dir(arch.arch),
            'install', 'lib', 'pkgconfig'
        )
        return env

    def build_arch(self, arch):
        env = self.get_recipe_env(arch)

        source_dir = self.get_build_dir(arch.arch)

        with current_directory(source_dir):
            shprint(sh.Command('./autogen.sh'))
            shprint(
                sh.Command('./configure'),
                '--host=' + arch.command_prefix,
                '--target=' + arch.toolchain_prefix,
                '--prefix=' + self.ctx.get_python_install_dir(),
                '--enable-embedded',
                '--enable-shared=yes',
                '--enable-static=no',
                _env=env)
            shprint(sh.make, '-j' + str(cpu_count() + 1), _env=env)

            # make the install so the headers are collected in the right subfolder
            shprint(sh.make, 'installl', _env=env)


recipe = TesseractRecipe()
