#av1 (all) in one
import subprocess
import time
import pathlib
import vapoursynth as vs
core=vs.core

keyint=161
min_keyint=6

cwd=pathlib.Path.cwd()
lock=cwd/'.lock'
if lock.exists():
    input('lock file exists, this script will exit.\nhit enter to continue...')
    raise FileExistsError
else:
    lock.touch()

source=[i for i in cwd.glob('*.mkv')]
source+=[i for i in cwd.glob('*.mp4')]
source+=[i for i in cwd.glob('*.m2ts')]
source+=[i for i in cwd.glob('*.webm')]
source+=[i for i in cwd.glob('*.mov')]
source+=[i for i in cwd.glob('*.wmv')]
source+=[i for i in cwd.glob('*.avi')]
if len(source)>1:
    input('unfortunately, this thing does not support multiple sources. only first one will be encoded.\nhit enter to contunue...')
source=sorted(source)[0]
cachefile=r'index'
extension='ivf'

clip=core.lsmas.LWLibavSource(source,cachefile=cachefile)
#clip=core.lsmas.LibavSMASHSource(source)
#################
# Although smashsource filter don't need an indexing process,
# it tends to get laggy after some time, so it's deprecated,
# but you are the boss. And don't forget to edit the vapoursynth
# template below.
#################
frames=clip.num_frames
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
    concatrecreat='\n'.join([f"file '{i}.{extension}'" for i in prodvalid[:-1]])
    with open("_concat.txt","w",encoding='utf-8') as concat:
        print(concatrecreat,file=concat)
class a:
    def poll():
        return 0
    def wait():
        return 0
b=c=d=e=f=g=h=i=j=k=l=m=n=o=p=q=r=s=t=u=v=w=x=y=z=a
penabled=[a]
_g=len(prodvalid)+1
for _n in range(lastkf,frames):
    _f=clip.get_frame(_n)
    kfd=_n-lastkf
    end=_n==frames-1
    scn=_f.props.get('_SceneChangeNext',0)
    # scp=bool(_f.props.get('_SceneChangePrev',0) and 173)
    if kfd <= min_keyint and not (kfd==min_keyint and scn):
        continue
    elif kfd >= keyint or scn or end:
        job=True
        _v=open(f"{lastkf}.vpy","w",encoding='utf-8')
        with open("_concat.txt","a",encoding='utf-8') as concat:
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
                    # cmd=f'title piece {lastkf} to {_n+end} of {frames} (roughly {lastkf/frames*100}%) gops: {_g} & vspipe -c y4m "{lastkf}.vpy" - | uvg266-10 -i - --input-file-format y4m --input-bitdepth 10 --period 0 --preset fast --gop 8 --rd 3 --rdoq --mv-rdo --signhide --qp 28 -o "{lastkf}.tmp.{extension}" && del "{lastkf}.vpy" && move/Y "{lastkf}.tmp.{extension}" "{lastkf}.{extension}"'
                    # cmd=f'title piece {lastkf} to {_n+end} of {frames} (roughly {lastkf/frames*100}%) gops: {_g} & vspipe -c y4m "{lastkf}.vpy" - | ffmpeg -hide_banner -i - -c:v libaom-av1 -cpu-used 6 -crf 36 -y "{lastkf}.tmp.{extension}" && del "{lastkf}.vpy" && move/Y "{lastkf}.tmp.{extension}" "{lastkf}.{extension}"'
                    cmd=f'title piece {lastkf} to {_n+end} of {frames} (roughly {lastkf/frames*100}%) gops: {_g} & vspipe -c y4m "{lastkf}.vpy" - | sav1 -i - --preset 6 --crf 38 --tune 0 --keyint -1 -b "{lastkf}.tmp.{extension}" && del "{lastkf}.vpy" && move/Y "{lastkf}.tmp.{extension}" "{lastkf}.{extension}"'
                    penabled[_i]=subprocess.Popen(cmd,shell=True)
                    lastkf=_n+bool(scn)
                    _g+=1
                    job=False
                    break

# Such a low bitrate video don't really deserve a 96k opus.
subprocess.run(r'title encoding audio... & ffmpeg -i "{s}" -c:a libopus -b:a 96k -mapping_family 0 -ac 2 -map_metadata -1 -map_chapters -1 _audio.opus'.format(s=source),shell=True)
for _i in penabled:
    _i.wait()
subprocess.run(rf'ffmpeg -safe 0 -f concat -i _concat.txt -strict -2 -c copy _video.{extension} & title all done.',shell=True)
input('enter to exit.')
