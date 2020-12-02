import sh
from pythonforandroid.recipe import Recipe
from pythonforandroid.util import current_directory
from pythonforandroid.logger import shprint
from os.path import join
from multiprocessing import cpu_count


class LibDBRecipe(Recipe):
    version = '18.1.32'
    url = 'https://gentoo.osuosl.org/distfiles/db-{version}.tar.gz'
    sha256sum = 'fa1fe7de9ba91ad472c25d026f931802597c29f28ae951960685cde487c8d654'
    # built_libraries = {'libdb.so': 'build_unix/.libs'}
    depends = ['openssl']

    def install_dir(self, arch):
        return join(self.get_build_dir(arch.arch), 'install')

    def include_flags(self, arch):
        '''Returns a string with the include folders'''
        libdb_includes = join(self.install_dir(arch), 'include')
        return ' -I' + libdb_includes

    def build_arch(self, arch):
        env = self.get_recipe_env(arch)

        openssl_recipe = self.get_recipe('openssl', self.ctx)

        env['CPPFLAGS'] = env.get('CPPFLAGS', '') + '{} -I {}'.format(
            openssl_recipe.include_flags(arch),
            self.stl_include_dir
        )
        env['LDFLAGS'] = env.get('LDFLAGS', '') + ' {} -L{} -l{}'.format(
            openssl_recipe.link_dirs_flags(arch),
            self.get_stl_lib_dir(arch),
            self.stl_lib_name
        )
        env['LIBS'] = env.get('LIBS', '') + openssl_recipe.link_libs_flags()

        with current_directory(join(
            self.get_build_dir(arch.arch),
            'build_unix'
        )):
            shprint(
                sh.Command(join(
                    '..',
                    'dist',
                    'configure'
                )),
                '--host=arm-linux-androideabi',
                '--enable-shared',
                '--disable-static',
                '--enable-cxx',
                '--enable-stl',
                '--prefix={}'.format(self.install_dir(arch)),
                _env=env)
            shprint(sh.make, '-j', str(cpu_count()), _env=env)
            shprint(sh.make, 'install', _env=env)


recipe = LibDBRecipe()
