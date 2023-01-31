# ideal-chainsaw
python scripts for my stupid encoding workflow, the repo name is just randomly suggested by github

# explanations
## vpy2ssim.py
~read the code it's short~
calculates ssim with ffmpeg. assuming you have one output file per vapoursynth script and the output name is (vpy name)+\_fin.hevc and your vs script has a video node object named src which is your reference for ssim calculation but you can modify the code anyway.
## find_smallest_ssim.py
drag n drop ffmpeg generated ssim log. uses and displays **dB** form of ssim because it's easier to compare for human eyes ;p
## vpy2flac.py
encodes audio from source file strings find in vpy, with concat support. and you need to manually edit this script to choose stream index.
