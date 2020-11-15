from os.path import join
from pythonforandroid.recipe import CompiledComponentsPythonRecipe

class PyZintRecipe(CompiledComponentsPythonRecipe):
    version = '0.1.7'
    url = 'https://files.pythonhosted.org/packages/39/42/b13d638dd53021c037544e404e18c785f4f4f9235afc7127efb95b9c5527/pyzint-0.1.7.tar.gz#sha256=f06e764780d157a1d319f83390ed67e366d215247678f189d93d24943ace1765'
    md5sum = '8f3ad6dc515bbab2fb25b207397a792f'
    blake2bsum = '84757348b619429633ba40117f1c68ddd9c932559afc664e8b156126642ce7562b20f18cbdc47ae158c00959be026ca18dc71974d785c434cc29948929799878'

    depends = ['setuptools']
    
    call_hostpython_via_targetpython = False

    def get_recipe_env(self, arch=None, with_flags_in_cc=True):
        env = super().get_recipe_env(arch, with_flags_in_cc)
        #env['PYTHON_ROOT'] = self.ctx.get_python_install_dir()
        #env['LIBS'] = env.get('LIBS', '') + ' -landroid'
        return env
    
recipe = PyZintRecipe()
