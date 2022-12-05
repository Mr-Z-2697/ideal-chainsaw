import sys,os
import pathlib
from importlib.machinery import SourceFileLoader
import subprocess
import vapoursynth as vs
core=vs.core
sys.dont_write_bytecode=True
wd=pathlib.Path(__file__).parent.absolute()
os.chdir(wd)
vpys=wd.glob('*.vpy')
for i in vpys:
    _i=str(i)
    i_=_i.replace('.vpy','_fin.hevc')
    i__=f'{i.stem}-ssim.txt'
    script=SourceFileLoader('script',_i).load_module()
    run=subprocess.Popen(f'ffmpeg -r 24 -i - -r 24 -i "{i_}" -lavfi ssim="{i__}" -f null -',stdin=subprocess.PIPE,cwd=wd)
    script.src.output(run.stdin,y4m=True)
    run.communicate()
input('done.')