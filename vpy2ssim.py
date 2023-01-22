import sys,os
import pathlib
from importlib.machinery import SourceFileLoader
import subprocess
import vapoursynth as vs
import re
core=vs.core
sys.dont_write_bytecode=True
wd=pathlib.Path(__file__).parent.absolute()
os.chdir(wd)
vpys=wd.glob('*.vpy')
ren=re.compile('n:([0-9]*)')
for i in vpys:
    _i=str(i)
    i_=_i.replace('.vpy','_fin.hevc')
    i__=f'{i.stem}-ssim.txt'
    i___=i__.replace('.txt','_fin.txt')
    if os.path.exists(i___):
        continue
    script=SourceFileLoader('vsscript',_i).load_module()
    _o=script.src
    __o=_o.num_frames
    del script
    del sys.modules['vsscript']
    run=subprocess.Popen(f'ffmpeg -r 24 -i - -r 24 -i "{i_}" -lavfi ssim="{i__}" -f null -',stdin=subprocess.PIPE,cwd=wd)
    _o.output(run.stdin,y4m=True)
    run.communicate()
    with open(i__) as __i:
        l_=__i.readlines()[-1]
    l__=ren.search(l_).group(1)
    if int(l__)==__o:
        os.rename(i__,i___)
input('done.')