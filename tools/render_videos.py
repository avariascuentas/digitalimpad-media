import asyncio, subprocess, os, glob
src=open(__import__('os').path.join(__import__('os').path.dirname(__file__),'render_fotos.py')).read().split('async def main')[0]
exec(src)
ANIM="""body>*:not(.bg){animation:up .9s cubic-bezier(.2,.8,.2,1) both}
body>*:nth-child(2){animation-delay:.2s}body>*:nth-child(3){animation-delay:1.2s}body>*:nth-child(4){animation-delay:2.4s}body>*:nth-child(5){animation-delay:3.4s}
@keyframes up{from{opacity:0;transform:translateY(40px)}to{opacity:1;transform:none}}
.bg{animation:drift 14s ease-in-out infinite alternate}@keyframes drift{to{filter:hue-rotate(25deg) brightness(1.15)}}
.card{animation:pop .8s both}.card:nth-child(1){animation-delay:1.6s}.card:nth-child(2){animation-delay:3.0s}.card:nth-child(3){animation-delay:4.6s}
@keyframes pop{from{opacity:0;transform:scale(.85)}to{opacity:1;transform:none}}
.bar{animation:wave 1.1s ease-in-out infinite alternate}@keyframes wave{from{transform:scaleY(.25)}to{transform:scaleY(1)}}
.col{animation:pop .9s both}.col:nth-child(1){animation-delay:1.4s}.col:nth-child(2){animation-delay:3.6s}
"""
import re
V={}
V['video_residencias']=P['post2'].replace('<div style="flex:1;background:#ffffff10','<div class="card" style="flex:1;background:#ffffff10')
bars=P['post5'].replace('<div style="width:14px;','<div class="bar" style="width:14px;')
import random
cnt=[0]
def d(m):
    cnt[0]+=1; return m.group(0).replace('class="bar" style="','class="bar" style="animation-delay:-%.2fs;'%(cnt[0]*0.13))
V['video_voz']=re.sub(r'class="bar" style="',lambda m:d(m),bars)
V['video_antes_despues']=P['post6'].replace('<div style="flex:1;background:','<div class="col" style="flex:1;background:')
async def main():
  async with async_playwright() as p:
    b=await p.chromium.launch(executable_path="/usr/bin/google-chrome")
    for k,v in V.items():
      ctx=await b.new_context(viewport={"width":1200,"height":1200},record_video_dir="rec",record_video_size={"width":1200,"height":1200})
      pg=await ctx.new_page()
      await pg.set_content(f"<html><head><meta charset='utf-8'><style>{BASE}{ANIM}</style></head><body>{v}</body></html>")
      await pg.wait_for_timeout(12500)
      path=await pg.video.path(); await ctx.close()
      subprocess.run(["ffmpeg","-y","-loglevel","error","-ss","0.3","-i",path,"-t","12","-vf","scale=1080:1080,fps=30","-c:v","libx264","-preset","veryfast","-crf","20","-pix_fmt","yuv420p","-movflags","+faststart",f"{k}.mp4"],check=True)
      subprocess.run(["ffmpeg","-y","-loglevel","error","-ss","8","-i",f"{k}.mp4","-frames:v","1",f"{k}_frame.png"])
    await b.close()
asyncio.run(main())
