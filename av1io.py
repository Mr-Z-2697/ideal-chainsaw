#av1 (all) in one
import subprocess
import os
import time
import pathlib
import vapoursynth as vs
core=vs.core

keyint=161
min_keyint=6
extension='ivf'
byte_concat=extension=='266' # huh.
parallel_processes=1 # limited to 26 due to some stupid code I wrote and was freakin super proud of (not really).

cwd=pathlib.Path.cwd()
lock=cwd/'.lock'
if lock.exists():
    input('lock file exists, this script will exit.\nhit enter to continue...')
    raise FileExistsError
else:
    lock.touch()

keyframefile=cwd/'.keyframes'
keyframefileexists=keyframefile.exists()
if keyframefileexists:
    with open(keyframefile,'r') as f:
        keyframelist=f.read()
        keyframelist=keyframelist.split('\n')
        keyframelist=[int(i) if i else i for i in keyframelist]

source=list(cwd.glob('*.mkv'))
source+=list(cwd.glob('*.mp4'))
source+=list(cwd.glob('*.m2ts'))
source+=list(cwd.glob('*.webm'))
source+=list(cwd.glob('*.mov'))
source+=list(cwd.glob('*.wmv'))
source+=list(cwd.glob('*.avi'))
if len(source)>1:
    input('unfortunately, this thing does not support multiple sources. only first one will be encoded.\nhit enter to contunue...')
source=sorted(source)[0]
cachefile=r'index'

clip=core.lsmas.LWLibavSource(source,cachefile=cachefile)
#clip=core.lsmas.LibavSMASHSource(source)
#################
# Although smashsource filter don't need an indexing process,
# it tends to get laggy after some time, so it's deprecated,
# but you are the boss. And don't forget to edit the vapoursynth
# template below.
#################
frames=clip.num_frames
if not keyframefileexists:
    clip=clip.resize.Bicubic(1280,720,format=vs.YUV420P8)
    sup=core.mv.Super(clip,pel=1)
    vec=core.mv.Analyse(sup,blksize=32,truemotion=False,isb=True)
    clip=core.mv.SCDetection(clip,vec)

products=cwd.glob(f'*.{extension}')
products=[i for i in products]
products.sort(key=lambda i:int(i.name.split('.')[0]))
prodfins=[i for i in products if not str(i).endswith(f'.tmp.{extension}')]
prodvalid=[]
for product in products:
    if str(product).endswith(f'.tmp.{extension}'):
        break
    else:
        prodvalid.append(int(product.name.split('.')[0]))
if prodvalid==[]:
    lastkf=0
else:
    prodvalid.sort()
    lastkf=prodvalid[-1]
    if byte_concat:
        concatrecreat='\n'.join([f"{i}.{extension}" for i in prodvalid[:-1]])
    else:
        concatrecreat='\n'.join([f"file '{i}.{extension}'" for i in prodvalid[:-1]])
    with open("_concat.txt","w",encoding='utf-8') as concat:
        print(concatrecreat,file=concat)
class a:
    def poll():
        return 0
    def wait():
        return 0
b=c=d=e=f=g=h=i=j=k=l=m=n=o=p=q=r=s=t=u=v=w=x=y=z=a
penabled=[a,b,c,d,e,f,g,h,i,j,k,l,m,n,o,p,q,r,s,t,u,v,w,x,y,z][:parallel_processes]
_g=len(prodvalid)+1
for _n in range(lastkf,frames):
    if keyframefileexists:
        scn=_n+1 in keyframelist
    else:
        _f=clip.get_frame(_n)
        scn=_f.props.get('_SceneChangeNext',0)
        # scp=bool(_f.props.get('_SceneChangePrev',0) and 173)
    kfd=_n-lastkf
    end=_n==frames-1
    if kfd <= min_keyint and not (kfd==min_keyint and scn):
        continue
    elif kfd >= keyint or scn or end:
        job=True
        _v=open(f"{lastkf}.vpy","w",encoding='utf-8')
        with open("_concat.txt","a",encoding='utf-8') as concat:
            if byte_concat:
                print(f"{lastkf}.{extension}",file=concat)
            else:
                print(f"file '{lastkf}.{extension}'",file=concat)
        print(r'''import vapoursynth as vs
core=vs.core
clip=core.lsmas.LWLibavSource(r'{s}',cachefile=r'{c}')
#clip=core.lsmas.LibavSMASHSource(r'{s}')
clip[{i}:{j}].set_output()'''.format(i=lastkf,j=_n+(scn or end),s=source,c=cachefile),file=_v)
        _v.close()
        while job:
            for _i,_x in enumerate(penabled):
                if _x.poll()==None:
                    time.sleep(0.5)
                    continue
                else:
                    # cmd=f'title piece {lastkf} to {_n+end} of {frames} (roughly {lastkf/frames*100}%) gops: {_g} & vspipe -c y4m "{lastkf}.vpy" - | vvencffapp -i - --y4m -ip 0 -rs 1024 -dr idr --preset medium -t 16 --WaveFrontSynchro 1 --CTUSize 64 --IFP 1 --CIIP 3 --POC0IDR 1 -q 24 -b "{lastkf}.tmp.{extension}" && del "{lastkf}.vpy" && move/Y "{lastkf}.tmp.{extension}" "{lastkf}.{extension}"'
                    # cmd=f'title piece {lastkf} to {_n+end} of {frames} (roughly {lastkf/frames*100}%) gops: {_g} & vspipe -c y4m "{lastkf}.vpy" - | uvg266-10 -i - --input-file-format y4m --input-bitdepth 10 --period 0 --preset fast --gop 8 --rd 3 --rdoq --mv-rdo --signhide --qp 28 -o "{lastkf}.tmp.{extension}" && del "{lastkf}.vpy" && move/Y "{lastkf}.tmp.{extension}" "{lastkf}.{extension}"'
                    # cmd=f'title piece {lastkf} to {_n+end} of {frames} (roughly {lastkf/frames*100}%) gops: {_g} & vspipe -c y4m "{lastkf}.vpy" - | ffmpeg -hide_banner -i - -c:v libaom-av1 -cpu-used 6 -crf 36 -y "{lastkf}.tmp.{extension}" && del "{lastkf}.vpy" && move/Y "{lastkf}.tmp.{extension}" "{lastkf}.{extension}"'
                    cmd=f'title piece {lastkf} to {_n+end} of {frames} (roughly {lastkf/frames*100}%) gops: {_g} & vspipe -c y4m "{lastkf}.vpy" - | sav1 -i - --preset 6 --crf 38 --tune 0 --keyint -1 -b "{lastkf}.tmp.{extension}" && del "{lastkf}.vpy" && move/Y "{lastkf}.tmp.{extension}" "{lastkf}.{extension}"'
                    penabled[_i]=subprocess.Popen(cmd,shell=True)
                    lastkf=_n+bool(scn)
                    _g+=1
                    job=False
                    break

# Such a low bitrate video don't really deserve a 96k opus.
subprocess.run(r'title encoding audio... & ffmpeg -i "{s}" -c:a libopus -b:a 96k -mapping_family 0 -ac 2 -map_metadata -1 -map_chapters -1 _audio.opus -n'.format(s=source),shell=True)
for _i in penabled:
    _i.wait()
if byte_concat:
    os.system('title byte concat')
    with open('_concat.txt','r',encoding='utf-8') as _c:
        concatlist=_c.read().split('\n')
        concatlist=[i for i in concatlist if i]
    with open('_video.266','wb') as _vid:
        for _i in concatlist:
            with open(_i,'rb') as _seg:
                for _block in iter(lambda: _seg.read(266<<20),b''):
                    _vid.write(_block)
    os.system('title all done.')
else:
    subprocess.run(rf'ffmpeg -safe 0 -f concat -i _concat.txt -c copy _video.{extension} & title all done.',shell=True)
input('enter to exit.')
