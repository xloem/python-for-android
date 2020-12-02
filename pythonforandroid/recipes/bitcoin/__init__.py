import sh
from multiprocessing import cpu_count

from pythonforandroid.archs import Arch
from pythonforandroid.logger import shprint
from pythonforandroid.recipe import Recipe
from pythonforandroid.util import current_directory


class BitcoinRecipe(Recipe):

    version = '0.20.1'
    url = 'https://bitcoincore.org/bin/bitcoin-core-{version}/bitcoin-{version}.tar.gz'
    sha256sum = '4bbd62fd6acfa5e9864ebf37a24a04bc2dcfe3e3222f056056288d854c53b978'

    depends = ['libsecp256k1', 'libdb']

    def get_recipe_env(self, arch=None, with_flags_in_cc=True):
        env = super().get_recipe_env(arch, with_flags_in_cc)

        libdb_recipe = self.get_recipe('libdb', self.ctx)

        env['CPPFLAGS'] = env.get('CPPFLAGS', '') + ' -I{} {}'.format(
                self.stl_include_dir,
                libdb_recipe.include_flags(arch)
        )

        env['LDFLAGS'] = env.get('LDFLAGS', '') + ' -L{} -l{}'.format(
            self.get_stl_lib_dir(arch),
            self.stl_lib_name
        )

    def build_arch(self, arch: Arch) -> None:
        env = self.get_recipe_env(arch)
        with current_directory(self.get_build_dir(arch.arch)):
            shprint(sh.Command('./autogen.sh'), _env=env)
            shprint(
                sh.Command('./configure'),
                '--host=' + arch.toolchain_prefix,
                '--prefix=' + self.ctx.get_python_install_dir(),
                '--enable-shared',
                '--disable-static',
                _env=env)
            shprint(
                sh.make,
                "-j",
                str(cpu_count()),
                _env=env,
            )


recipe = BitcoinRecipe()
