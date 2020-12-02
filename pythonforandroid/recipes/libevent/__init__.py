import sh
from pythonforandroid.recipe import Recipe
from pythonforandroid.util import current_directory
from pythonforandroid.logger import shprint
from os.path import join
from multiprocessing import cpu_count


class LibEventRecipe(Recipe):
    version = '2.1.12'
    url = 'https://github.com/libevent/libevent/releases/download/release-{version}-stable/libevent-{version}-stable.tar.gz'
    sha256sum = '92e6de1be9ec176428fd2367677e61ceffc2ee1cb119035037a27d346b0403bb'

    #built_libraries = { 'libdb_stl-4.8.so': 'install/lib' }
    depends = ['openssl']

    #patches = ['config.patch', 'atomic_init.patch']

    #def install_dir(self, arch):
    #    return join(self.get_build_dir(arch.arch), 'install')

    #def include_flags(self, arch):
    #    '''Returns a string with the include folders'''
    #    libdb_includes = join(self.install_dir(arch), 'include')
    #    return ' -I' + libdb_includes

    def build_arch(self, arch):
        env = self.get_recipe_env(arch)

        openssl_recipe = self.get_recipe('openssl', self.ctx)

        env['CPPFLAGS'] = '{} {}'.format(
            env.get('CPPFLAGS', ''),
            openssl_recipe.include_flags(arch)
        )
        env['LIBS'] = '{} {}'.format(
            env.get('LIBS', ''),
            openssl_recipe.link_dirs_flags(arch),
        )

        with current_directory(join(self.get_build_dir(arch.arch))):
            shprint(
                sh.Command('./configure'),
                '--host=arm-linux-androideabi',
                '--enable-shared',
                '--disable-static',
                #'--prefix={}'.format(self.install_dir(arch)),
                #'--includedir={}/db48/include'.format(self.install_dir(arch)),
                _env=env)
            shprint(sh.make, '-j', str(cpu_count()), _env=env)
            #shprint(sh.make, 'install', _env=env)


recipe = LibEventRecipe()
