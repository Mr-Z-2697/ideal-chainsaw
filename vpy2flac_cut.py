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

    framedur=1001/24000
    lines=c.split('\n')
    for j in lines:
        ml=rex.findall(j)
        if ml:
            _i=f'-i "{ml[0]}"'
            slice=re.findall('\[([0-9]*:[0-9]*)\]',j)
            startframe,endframe=slice[0].split(':')
            startframe=int(startframe) if startframe else 0
            endframe=int(endframe) if endframe else 0
            if startframe:
                _i+=f' -ss {startframe*framedur}'
            if endframe:
                _i+=f' -to {endframe*framedur}'
            break
    if ml:
        _n=1
    else:
        print('no valid file name found, skip')

    _label=''.join([f'[{i}:a:0]' for i in range(_n)])
    _f=f'-filter_complex {_label}concat=v=0:a=1:n={_n}[a]' if _n>1 else ''
    _s='0:a:0' if _n==1 else '[a]'
    cmd=f'ffmpeg -hide_banner {_i} {_f} -map {_s} -vn -f wav -c pcm_s{_b}le - | flac -8 -V -P0 --ignore-chunk-sizes -o "{_o}" -'
    subprocess.run(cmd,shell=True)
input('over.')