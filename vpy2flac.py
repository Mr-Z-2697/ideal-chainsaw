import os,sys
import pathlib
import subprocess
import re
_fil=pathlib.Path(__file__)
try:
    _b={'16':16,'24':24,'32':32}[str(_fil.stem)[-2:]]
except:
    if len(sys.argv)>=2:
        _b=sys.argv[1]
    else:
        _b=input('bps? ')
rex=re.compile(r'Source\((?:source=|)[r]*[\'"](.+?(?:m2ts|mkv|mp4))[\'"]',re.M)
wd=_fil.parent.absolute()
os.chdir(wd)
vpys=wd.glob('*.vpy')
for i in vpys:
    print('='*10,f'processing {i.name}','='*10)
    _o=str(i).replace('.vpy','.flac')
    if os.path.exists(_o):
        print('output exists, skip')
        continue
    with open(i,'r',encoding='utf-8') as f:
        c=f.read()
    m=rex.findall(c)
    if m:
        _i=''
        for j in m:
            _i+=f'-i "{j}" '
    else:
        print('no valid file name found, skip')
        continue
    _n=len(m)
    _label=''.join([f'[{i}:a:0]' for i in range(_n)])
    _f=f'-filter_complex {_label}concat=v=0:a=1:n={_n}[a]' if _n>1 else ''
    _s='0:a:0' if _n==1 else '[a]'
    cmd=f'ffmpeg -hide_banner {_i} {_f} -map {_s} -vn -f wav -c pcm_s{_b}le - | flac -8 -V --ignore-chunk-sizes -o "{_o}" -'
    subprocess.run(cmd,shell=True)
input('over.')