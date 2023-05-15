# ideal-chainsaw
python scripts for my stupid encoding workflow, the repo name is just randomly suggested by github

# explanations
## vpy2ssim.py
~read the code it's short~\
calculates ssim with ffmpeg. assuming you have one output file per vapoursynth script and the output name is (vpy name)+\_fin.hevc and your vs script has a video node object named src which is your reference for ssim calculation but you can modify the code anyway.
## find_smallest_ssim.py
drag n drop ffmpeg generated ssim log. uses and displays **dB** form of ssim because it's easier to compare for human eyes ;p
## vpy2flac.py
encodes audio from source file strings find in vpy, with concat support. and you need to manually edit this script to choose stream index.
## av1io.py
av1 (all) in one. moved from [gist](https://gist.github.com/Mr-Z-2697/3d8776f4c3e9a9b569b09cc99643fe19).\
uses mvtools to detect scene change then encode in fragments with multi-process parallel work. ([i know how to use pool](https://github.com/Mr-Z-2697/makeheic.py/blob/main/makeheic.py#L8), i use my stupid implementation just because i thought pool was too complicated)\
aomenc not doing good in mt, svtav1 refuses to use scenecut like a(n) \_\_\_\_\_, so either should benefit from this script.
