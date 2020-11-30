import sh
from pythonforandroid.recipe import Recipe
from pythonforandroid.util import current_directory
from pythonforandroid.logger import shprint
from os.path import join
from multiprocessing import cpu_count


class LibDBRecipe(Recipe):
    version = '18.1.40'
    url = 'http://download.oracle.com/otn/berkeley-db/db-{version}.tar.gz'
    sha256sum = '0cecb2ef0c67b166de93732769abdeba0555086d51de1090df325e18ee8da9c8'
    #built_libraries = {'libcurl.so': 'dist/lib'}
    #depends = ['openssl']

    def build_arch(self, arch):
        env = self.get_recipe_env(arch)

        openssl_recipe = self.get_recipe('openssl', self.ctx)
        openssl_dir = openssl_recipe.get_build_dir(arch.arch)

        env['CPPFLAGS'] = env.get('CPPFLAGS', '') + openssl_recipe.include_flags(arch)
        env['LDFLAGS'] = env.get('LDFLAGS', '') + openssl_recipe.link_dirs_flags(arch)
        env['LIBS'] = env.get('LIBS', '') + openssl_recipe.link_libs_flags()

        with current_directory(join(
            self.get_build_dir(arch.arch),
            'build_unix'
        ):
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
                '--prefix={}'.format(self.ctx.get_python_install_dir()),
                _env=env)
            shprint(sh.make, '-j', str(cpu_count()), _env=env)
            #shprint(sh.make, 'install', _env=env)


recipe = LibDBRecipe()
