import sh
from pythonforandroid.recipe import Recipe
from pythonforandroid.util import current_directory
from pythonforandroid.logger import shprint
from os.path import join
from multiprocessing import cpu_count


class LibDBRecipe(Recipe):
    version = '4.8.30'
    url = 'https://download.oracle.com/berkeley-db/db-{version}.tar.gz'
    sha256sum = 'e0491a07cdb21fb9aa82773bbbedaeb7639cbd0e7f96147ab46141e0045db72a'
    # built_libraries = {'libdb.so': 'build_unix/.libs'}
    depends = ['openssl']

    patches = ['config.patch']

    def install_dir(self, arch):
        return join(self.get_build_dir(arch.arch), 'install')

    def include_flags(self, arch):
        '''Returns a string with the include folders'''
        libdb_includes = join(self.install_dir(arch), 'include')
        return ' -I' + libdb_includes

    def build_arch(self, arch):
        env = self.get_recipe_env(arch)

        openssl_recipe = self.get_recipe('openssl', self.ctx)

        env['CPPFLAGS'] = '{} {} -I {}'.format(
            env.get('CPPFLAGS', ''),
            openssl_recipe.include_flags(arch),
            self.stl_include_dir
        )
        env['LIBS'] = '{} {} {} -L{} -l{}'.format(
            env.get('LIBS', ''),
            openssl_recipe.link_libs_flags(),
            openssl_recipe.link_dirs_flags(arch),
            self.get_stl_lib_dir(arch),
            self.stl_lib_name
        )

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
