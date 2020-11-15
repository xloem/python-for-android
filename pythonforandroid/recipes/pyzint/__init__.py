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
        shprint(sh.git, 'clone', self.git, build_dir)
        shprint(sh.git, 'checkout', self.version, _cwd=build_dir)
        shprint(sh.git, 'submodule', 'update', '--init', '--recursive', _cwd=build_dir)

    def get_recipe_env(self, arch=None, with_flags_in_cc=True):
        env = super().get_recipe_env(arch, with_flags_in_cc)
        #env['PYTHON_ROOT'] = self.ctx.get_python_install_dir()
        #env['LIBS'] = env.get('LIBS', '') + ' -landroid'
        env['CPPFLAGS'] = env.get('CPPFLAGS', '') + ' -include stdint.h'
        return env
    
recipe = PyZintRecipe()
