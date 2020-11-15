from os.path import join
from pythonforandroid.recipe import CompiledComponentsPythonRecipe

class PyZintRecipe(CompiledComponentsPythonRecipe):
    version = '33821f2e184cbb4055f799fa01745ea7750543ba'
    url = 'https://github.com/xloem/pyzint/archive/{version}.tar.gz#sha256=393fe78d9f1fad36530c403b665c4363438d5ff30635ccd89a86c65d2e1dfdd7'
    md5sum = 'c4714892dd314bf276175d263e3ab4ce'

    depends = ['setuptools']
    
    call_hostpython_via_targetpython = False

    def get_recipe_env(self, arch=None, with_flags_in_cc=True):
        env = super().get_recipe_env(arch, with_flags_in_cc)
        #env['PYTHON_ROOT'] = self.ctx.get_python_install_dir()
        #env['LIBS'] = env.get('LIBS', '') + ' -landroid'
        env['CPPFLAGS'] = env.get('CPPFLAGS', '') + ' -include stdint.h'
        return env
    
recipe = PyZintRecipe()
