#av1 (all) in one
import subprocess
import time
import vapoursynth as vs
from vapoursynth import core

source=r'test.mp4'
cachefile=r'ffindex'
keyint=300
min_keyint=15

clip=core.ffms2.Source(source,cachefile=cachefile)
#clip=core.lsmas.LibavSMASHSource(source)
#################
# Although smashsource filter don't need an indexing process,
# it tends to get laggy after some time, so it's deprecated,
# but you are the boss. And don't forget to edit the vapoursynth
# template below.
#################
clip=clip.resize.Bicubic(1280,720,format=vs.YUV420P8)
sup=core.mv.Super(clip,pel=1)
vec=core.mv.Analyse(sup,blksize=32,truemotion=False)
clip=core.mv.SCDetection(clip,vec)

lastkf=0
frames=clip.num_frames
class a:
    def poll():
        return 0
    def wait():
        return 0
b=c=d=e=f=g=h=i=j=k=l=m=n=o=p=q=r=s=t=u=v=w=x=y=z=a
penabled=[a,b,c,d]
_g=1
for _n in range(lastkf,frames):
    _f=clip.get_frame(_n)
    end=_n==frames-1
    if _n-lastkf <= min_keyint:
        continue
    elif _n-lastkf >= keyint or _f.props._SceneChangePrev or end:
        job=True
        _v=open(f"{lastkf}.vpy","w",encoding='utf-8')
        concat=open("_concat.txt","a",encoding='utf-8')
        print(f"file '{lastkf}.ivf'",file=concat)
        concat.close()
        print(r'''import vapoursynth as vs
from vapoursynth import core
clip=core.ffms2.Source(r'{s}',cachefile=r'{c}')
#clip=core.lsmas.LibavSMASHSource(r'{s}')
clip[{i}:{j}].set_output()'''.format(i=lastkf,j=_n+end,s=source,c=cachefile),file=_v)
        _v.close()
        while job:
            for _i,_x in enumerate(penabled):
                if _x.poll()==None:
                    time.sleep(0.5)
                    continue
                else:
                    # cmd=f'title piece {lastkf} to {_n+end} of {frames} (roughly {lastkf/frames*100}%) gops: {_g} & vspipe -c y4m "{lastkf}.vpy" - | ffmpeg -hide_banner -i - -c:v libaom-av1 -cpu-used 6 -crf 36 "{lastkf}.ivf" && del "{lastkf}.vpy"'
                    cmd=f'title piece {lastkf} to {_n+end} of {frames} (roughly {lastkf/frames*100}%) gops: {_g} & vspipe -c y4m "{lastkf}.vpy" - | sav1 -i - --preset 6 --crf 38 --tune 0 --keyint -1 -b "{lastkf}.ivf" && del "{lastkf}.vpy"'
                    penabled[_i]=subprocess.Popen(cmd,shell=True)
                    lastkf=_n
                    _g+=1
                    job=False
                    break

# Such a low bitrate video don't really deserve a 96k opus.
subprocess.run(r'title encoding audio... & ffmpeg -i "{s}" -c:a libopus -b:a 96k -mapping_family 1 -ac 2 -map_metadata -1 -map_chapters -1 _audio.opus'.format(s=source),shell=True)
for _i in penabled:
    _i.wait()
subprocess.run(r'ffmpeg -safe 0 -f concat -i _concat.txt -c copy _video.ivf & title all done.',shell=True)
input('enter to exit.')
