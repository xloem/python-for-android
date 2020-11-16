from os.path import join
from pythonforandroid.logger import shprint, info, debug, warning
from pythonforandroid.recipe import CompiledComponentsPythonRecipe
import sh

class PyZintRecipe(CompiledComponentsPythonRecipe):
    version = '33821f2e184cbb4055f799fa01745ea7750543ba'
    git = 'https://github.com/xloem/pyzint'

    depends = ['setuptools']
    
    call_hostpython_via_targetpython = False

    def prebuild_arch(self, arch):
        super().prebuild_arch(arch)
        build_dir = self.get_build_dir(arch.arch)
        env = self.get_recipe_env(arch)
        shprint(sh.git, 'clone', self.git, build_dir, _env=env)
        shprint(sh.git, 'checkout', self.version, _cwd=build_dir, _env=env)
        shprint(sh.git, 'submodule', 'update', '--init', '--recursive', _cwd=build_dir, _env=env)

    def get_recipe_env(self, arch=None, with_flags_in_cc=True):
        env = super().get_recipe_env(arch, with_flags_in_cc)
        env['CPPFLAGS'] = env.get('CPPFLAGS', '') + ' -include stdint.h'
        env['GIT_SSH_COMMAND'] = 'ssh -o "UserKnownHostsFile ' + join(self.get_recipe_dir(), 'known_hosts') + '"'
        return env
    
recipe = PyZintRecipe()
