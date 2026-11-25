# Reel IG 1080x1920 (agente de voz, fisio/kinesio). Render fotograma a fotograma con Playwright
# (animaciones CSS "congeladas" en cada instante) + ffmpeg con pista AAC silenciosa.
# Uso: python3 tools/ig_reel_voz.py salida.mp4
import asyncio, subprocess, sys, os, tempfile, shutil
from playwright.async_api import async_playwright
OUT = sys.argv[1] if len(sys.argv) > 1 else "reel.mp4"
DUR, FPS = 16.0, 30
CSS = """*{margin:0;box-sizing:border-box}
body{width:1080px;height:1920px;font-family:Poppins,sans-serif;color:#fff;overflow:hidden;position:relative;
background:radial-gradient(circle at 85% 8%,#3C51D7bb,transparent 40%),radial-gradient(circle at 5% 70%,#00dcff33,transparent 40%),linear-gradient(170deg,#141a4d,#070a24)}
.tag{display:inline-block;font-size:30px;font-weight:700;letter-spacing:3px;text-transform:uppercase;border-radius:40px;padding:12px 30px;color:#7ee8ff;border:2px solid #7ee8ff66}
h1{font-weight:800;line-height:1.08;font-size:88px}em{font-style:normal;color:#7ee8ff}
.brand{position:absolute;left:70px;bottom:70px;font-weight:800;font-size:40px}.brand b{color:#6f84ff}
.url{position:absolute;right:70px;bottom:78px;font-size:32px;color:#aab4ff}
.card{position:absolute;left:70px;right:70px;top:600px;background:#0e1438cc;border:2px solid #5d74ff88;border-radius:44px;padding:34px 40px;box-shadow:0 0 80px #3C51D766}
.row{display:flex;align-items:center;gap:26px}
.av{width:96px;height:96px;border-radius:50%;background:linear-gradient(135deg,#3C51D7,#7ee8ff);display:flex;align-items:center;justify-content:center;font-size:48px;animation:ring 1s ease-in-out infinite alternate}
@keyframes ring{from{box-shadow:0 0 0 0 #7ee8ff88}to{box-shadow:0 0 0 22px #7ee8ff00}}
.waves{display:flex;align-items:center;justify-content:center;gap:10px;height:150px;margin-top:20px}
.bar{width:14px;border-radius:8px;background:linear-gradient(#7ee8ff,#3C51D7);animation:wave .9s ease-in-out infinite alternate}
@keyframes wave{from{transform:scaleY(.2)}to{transform:scaleY(1)}}
.msgs{position:absolute;left:70px;right:70px;top:1010px;display:flex;flex-direction:column}
.m{margin-bottom:22px;max-width:86%;padding:22px 28px;border-radius:30px;font-size:33px;line-height:1.35;opacity:0;animation:up .6s cubic-bezier(.2,.8,.2,1) both}
.m small{display:block;font-size:22px;font-weight:700;letter-spacing:1px;margin-bottom:6px;opacity:.75}
.p{background:#ffffff14;border:1px solid #ffffff2a;border-top-left-radius:8px}
.ia{background:linear-gradient(160deg,#3C51D7,#26339a);margin-left:auto;border-top-right-radius:8px}
.tp{font-size:40px;letter-spacing:8px;line-height:1;overflow:hidden;animation:tp 1.3s both}
@keyframes tp{0%{opacity:0;max-height:0;padding:0 28px;margin-bottom:0}15%,85%{opacity:1;max-height:90px;padding:18px 28px;margin-bottom:22px}100%{opacity:0;max-height:0;padding:0 28px;margin-bottom:0}}
@keyframes up{from{opacity:0;transform:translateY(40px)}to{opacity:1;transform:none}}
@keyframes blink{0%{opacity:0}10%{opacity:1}90%{opacity:1}100%{opacity:0}}
.end{position:absolute;inset:0;background:linear-gradient(170deg,#141a4d,#070a24);display:flex;flex-direction:column;justify-content:center;padding:0 80px;opacity:0;animation:fade .7s both}
@keyframes fade{from{opacity:0}to{opacity:1}}
.chip{background:#ffffff12;border:1px solid #ffffff2a;border-radius:22px;padding:20px 26px;font-size:34px;margin-top:22px;opacity:0;animation:up .6s both}
.cta{margin-top:60px;display:inline-block;background:linear-gradient(90deg,#3C51D7,#00c8ff);border-radius:60px;padding:30px 50px;font-size:46px;font-weight:800;opacity:0;animation:up .6s both;box-shadow:0 0 60px #00c8ff66}
.intro{opacity:0;animation:up .8s both}
"""
H = [40,90,150,110,60,130,80,140,70,120,50,100,145,85,55,125,95,60,110,45]
bars = ''.join(f'<div class="bar" style="height:{h}px;animation-delay:-{i*0.17:.2f}s"></div>' for i, h in enumerate(H))
# (quién, texto, aparición en s)
MS = [("p", "Hola, quería una cita con el fisio. Me molesta la espalda 😣", 3.2),
      ("ia", "¡Claro! Mañana tengo a las 10:00 o el jueves a las 18:30. ¿Cuál prefieres?", 5.4),
      ("p", "El jueves a las 18:30.", 7.4),
      ("ia", "¡Listo! ✅ Te envío la confirmación por WhatsApp y un recordatorio el día antes.", 9.0)]
msgs = ''.join(f'<div class="m {k} tp" style="animation-delay:{t-1.3:.2f}s">•••</div><div class="m {k}" style="animation-delay:{t}s"><small>{"PACIENTE" if k=="p" else "🤖 AGENTE DE VOZ IA"}</small>{x}</div>' for k, x, t in MS)
# typ = ''.join(f'<div class="typing" style="{"right:90px" if k=="ia" else "left:90px"};top:{965 + 0}px;animation:blink {1.2}s {t-1.2}s both;display:none"></div>' for k, x, t in MS)
END = 11.6
HTML = f"""<div style="position:absolute;left:70px;right:70px;top:130px" class="intro">
<span class="tag">📞 Agente de voz · Fisio / Kinesio</span>
<h1 style="margin-top:36px">Tu clínica cerró<br>a las 20:00.<br><em>El teléfono, no.</em></h1></div>
<div class="card intro" style="animation-delay:.6s"><div class="row"><div class="av">📞</div>
<div><div style="font-size:30px;color:#aab4ff">Llamada entrante · 20:41</div>
<div style="font-size:40px;font-weight:700">Atendida por IA · <span id="clk">00:00</span></div></div></div>
<div class="waves">{bars}</div></div>
<div class="msgs">{msgs}</div>
<div class="end" style="animation-delay:{END}s">
<span class="tag" style="align-self:flex-start;opacity:0;animation:up .6s {END+.2}s both">Resultado de la llamada</span>
<div class="chip" style="animation-delay:{END+.5}s">✅ Cita reservada en tu agenda</div>
<div class="chip" style="animation-delay:{END+.8}s">📝 Llamada grabada y resumida</div>
<div class="chip" style="animation-delay:{END+1.1}s">🔀 Si hace falta, pasa a tu equipo</div>
<div style="align-self:flex-start" ><div class="cta" style="animation-delay:{END+1.6}s">📩 Escríbenos por DM</div></div>
<div style="font-size:34px;color:#c9d0ff;margin-top:40px;opacity:0;animation:up .6s {END+2.0}s both">Agentes de voz con IA para tu negocio</div>
</div>
<div class="brand">Digital <b>ImPad</b></div><div class="url">digitalimpad.com</div>"""
JS = """(t)=>{document.getAnimations().forEach(a=>{a.pause();a.currentTime=t*1000});
const s=Math.min(Math.floor(Math.max(t-0.6,0)),11);document.getElementById('clk').textContent='00:'+String(s).padStart(2,'0');}"""
async def main():
    tmp = tempfile.mkdtemp()
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page(viewport={"width": 1080, "height": 1920})
        await pg.set_content(f"<html><head><meta charset='utf-8'><style>{CSS}</style></head><body>{HTML}</body></html>")
        await pg.wait_for_timeout(800)
        n = int(DUR * FPS)
        for i in range(n):
            await pg.evaluate(JS, i / FPS)
            await pg.screenshot(path=f"{tmp}/f{i:04d}.jpg", type="jpeg", quality=92)
        await b.close()
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(FPS), "-i", f"{tmp}/f%04d.jpg",
                    "-f", "lavfi", "-i", "anullsrc=r=44100:cl=stereo", "-shortest",
                    "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-pix_fmt", "yuv420p",
                    "-c:a", "aac", "-b:a", "128k", "-movflags", "+faststart", OUT], check=True)
    for t in (2, 4.5, 8, 10.8, 15):
        shutil.copy(f"{tmp}/f{int(t*FPS):04d}.jpg", os.path.splitext(OUT)[0] + f"_t{t}.jpg")
    shutil.rmtree(tmp)
asyncio.run(main())
