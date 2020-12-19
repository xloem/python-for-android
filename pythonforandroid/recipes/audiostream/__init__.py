
from pythonforandroid.recipe import CythonRecipe
from pythonforandroid.toolchain import shprint, current_directory, info
import sh
from os.path import join


class AudiostreamRecipe(CythonRecipe):
    version = 'b32e3a4b30ef4bb529ae0f3b2bb0a35350ce5aca'
    url = 'https://github.com/kivy/audiostream/archive/{version}.zip'
    name = 'audiostream'
    depends = ['python3', 'sdl2', 'pyjnius']

    def get_recipe_env(self, arch):
        env = super().get_recipe_env(arch)
        sdl_include = 'SDL2'
        sdl_mixer_include = 'SDL2_mixer'
        env['USE_SDL2'] = 'True'
        env['SDL2_INCLUDE_DIR'] = join(self.ctx.bootstrap.build_dir, 'jni', 'SDL', 'include')

        env['CFLAGS'] += ' -I{jni_path}/{sdl_include}/include -I{jni_path}/{sdl_mixer_include}'.format(
                              jni_path=join(self.ctx.bootstrap.build_dir, 'jni'),
                              sdl_include=sdl_include,
                              sdl_mixer_include=sdl_mixer_include)
        env['NDKPLATFORM'] = self.ctx.ndk_platform
        env['LIBLINK'] = 'NOTNONE'  # Hacky fix. Needed by audiostream setup.py
        return env

    def postbuild_arch(self, arch):
        # TODO: It looks like this happened automatically in the past.
        #       Given the goal of migrating off of recipes, it would
        #       be good to repair or build infrastructure for doing this
        #       automatically.
        super().postbuild_arch(arch)
        info('Copying audiostream java files to classes build dir')
        with current_directory(self.get_build_dir(arch.arch)):
            shprint(sh.cp, '-a', join('audiostream', 'platform', 'android'), self.ctx.javaclass_dir)


recipe = AudiostreamRecipe()
