import asyncio
from playwright.async_api import async_playwright
BASE="""*{margin:0;box-sizing:border-box}body{width:1200px;height:1200px;font-family:Poppins,Inter,sans-serif;color:#fff;overflow:hidden;position:relative}
.bg{position:absolute;inset:0;z-index:-1}
.tag{display:inline-block;font-size:24px;font-weight:700;letter-spacing:3px;text-transform:uppercase;border-radius:40px;padding:10px 26px}
h1{font-weight:800;line-height:1.05}em{font-style:normal}
.brand{position:absolute;left:80px;bottom:60px;font-weight:800;font-size:36px}.brand b{color:#6f84ff}
.url{position:absolute;right:80px;bottom:66px;font-size:28px;color:#aab4ff}
.phone{position:absolute;width:470px;height:900px;border-radius:64px;background:#0b0f1f;border:12px solid #1d2340;box-shadow:0 40px 120px rgba(0,0,0,.55),0 0 80px rgba(93,116,255,.35);overflow:hidden}
.wa-top{background:#1f2c34;height:120px;display:flex;align-items:flex-end;padding:0 26px 18px;gap:16px;font-size:24px}
.av{width:52px;height:52px;border-radius:50%;background:linear-gradient(135deg,#3C51D7,#7ee8ff);display:flex;align-items:center;justify-content:center;font-weight:800;font-size:22px}
.wa-body{background:#0b141a;height:100%;padding:24px 20px;display:flex;flex-direction:column;gap:14px}
.b{max-width:82%;padding:14px 18px;border-radius:18px;font-size:22px;line-height:1.35}
.in{background:#202c33;border-top-left-radius:4px}.out{background:#005c4b;margin-left:auto;border-top-right-radius:4px}
.t{font-size:15px;color:#9fb3bf;text-align:right;margin-top:4px}
.day{align-self:center;background:#182229;color:#9fb3bf;font-size:17px;padding:6px 14px;border-radius:8px}
.chip{display:inline-block;background:#ffffff14;border:1px solid #ffffff2a;border-radius:14px;padding:10px 16px;font-size:20px;margin-top:8px}
"""
FOOT='<div class="brand">Digital <b>ImPad</b></div><div class="url">digitalimpad.com</div>'
NAVY='<div class="bg" style="background:radial-gradient(circle at 80% 15%,#3C51D7aa,transparent 45%),radial-gradient(circle at 10% 90%,#00dcff40,transparent 40%),linear-gradient(160deg,#141a4d,#070a24)"></div>'
P={}
# 1 Clínicas
P['post1']=NAVY+'''<div style="position:absolute;left:80px;top:90px;width:560px">
<span class="tag" style="color:#7ee8ff;border:2px solid #7ee8ff66">🦷 Clínicas</span>
<h1 style="font-size:78px;margin-top:40px">Son las<br><em style="color:#7ee8ff">23:47.</em></h1>
<p style="font-size:34px;line-height:1.4;color:#c9d0ff;margin-top:30px">Vuestra recepción está cerrada.<br>Vuestra agenda, <b style="color:#fff">no.</b></p>
<div style="margin-top:44px;display:flex;flex-direction:column;gap:16px;font-size:28px">
<div>✅ Ofrece huecos libres</div><div>✅ Reserva la cita</div><div>✅ Envía el recordatorio</div></div></div>
<div class="phone" style="right:70px;top:110px;transform:rotate(4deg)"><div class="wa-top"><div class="av">CD</div><div>Clínica Dental<br><span style="font-size:17px;color:#7ee8ff">en línea · asistente IA</span></div></div>
<div class="wa-body"><div class="day">HOY</div>
<div class="b in">Hola, me duele una muela 😣 ¿Tenéis algo para mañana?<div class="t">23:47</div></div>
<div class="b out">¡Hola! Siento lo de la muela. Mañana tengo hueco a las 9:30 o a las 16:15. ¿Cuál te va mejor?<div class="t">23:47 ✓✓</div></div>
<div class="b in">9:30 perfecto<div class="t">23:48</div></div>
<div class="b out">¡Hecho! ✅ Cita mañana a las 9:30 con la Dra. Pérez. Te mando un recordatorio a las 8:00.<div class="t">23:48 ✓✓</div></div>
</div></div>'''+FOOT
# 2 Residencias
P['post2']='<div class="bg" style="background:radial-gradient(circle at 15% 20%,#ff9f6b55,transparent 40%),radial-gradient(circle at 90% 85%,#3C51D7aa,transparent 45%),linear-gradient(160deg,#1c1640,#0a0a24)"></div>'+'''
<div style="position:absolute;left:80px;top:90px;right:80px">
<span class="tag" style="color:#ffc59e;border:2px solid #ffc59e66">🏡 Residencias de mayores</span>
<h1 style="font-size:84px;margin-top:40px">Las familias<br>no esperan<br><em style="color:#ffc59e">al lunes.</em></h1></div>
<div style="position:absolute;left:80px;right:80px;top:600px;display:flex;gap:22px">
''' + ''.join(f'''<div style="flex:1;background:#ffffff10;border:1px solid #ffffff22;border-radius:28px;padding:26px;{'box-shadow:0 0 60px #ffc59e55;border-color:#ffc59e' if w else 'opacity:.55'}">
<div style="font-size:22px;color:#c9c3ff">Residencia {n}</div><div style="font-size:30px;font-weight:700;margin-top:10px">{s}</div><div style="font-size:20px;color:#c9c3ff;margin-top:8px">{d}</div></div>''' for n,s,d,w in [('A','Sin respuesta','Domingo 21:30',0),('B','“Os llamamos el lunes”','Lunes 10:00',0),('C','Visita reservada ✅','Domingo 21:31',1)]) + '''</div>
<p style="position:absolute;left:80px;right:80px;top:880px;font-size:32px;color:#d8d3ff;line-height:1.4">La residencia C tiene un asistente con IA. Informa de plazas, precios y reserva la visita en un minuto.</p>'''+FOOT
# 3 Qué hace el agente
icons=[('💬','WhatsApp',0),('📸','Instagram',60),('🌐','Web',120),('📞','Teléfono',180),('✉️','Email',240),('📅','Agenda',300)]
import math
nodes=''.join(f'<div style="position:absolute;left:{600+330*math.cos(math.radians(a-90))-95}px;top:{640+330*math.sin(math.radians(a-90))-95}px;width:190px;height:190px;border-radius:50%;background:#111a4a;border:2px solid #5d74ff;display:flex;flex-direction:column;align-items:center;justify-content:center;box-shadow:0 0 40px #3C51D766"><div style="font-size:54px">{i}</div><div style="font-size:22px;font-weight:600;margin-top:4px">{t}</div></div>' for i,t,a in icons)
lines=''.join(f'<line x1="600" y1="640" x2="{600+330*math.cos(math.radians(a-90))}" y2="{640+330*math.sin(math.radians(a-90))}" stroke="#5d74ff" stroke-width="3" stroke-dasharray="8 10"/>' for i,t,a in icons)
P['post3']=NAVY+f'''<div style="position:absolute;left:0;right:0;top:70px;text-align:center"><span class="tag" style="color:#7ee8ff;border:2px solid #7ee8ff66">🤖 Qué hace un agente de IA</span>
<h1 style="font-size:60px;margin-top:26px">Un asistente. <em style="color:#7ee8ff">Todos vuestros canales.</em></h1></div>
<svg width="1200" height="1200" style="position:absolute;inset:0">{lines}</svg>{nodes}
<div style="position:absolute;left:470px;top:510px;width:260px;height:260px;border-radius:50%;background:radial-gradient(circle,#7ee8ff,#3C51D7);display:flex;flex-direction:column;align-items:center;justify-content:center;box-shadow:0 0 90px #7ee8ffaa;text-align:center"><div style="font-size:70px">🤖</div><div style="font-size:26px;font-weight:800;color:#0a0d2b">Agente IA<br>24/7</div></div>'''+FOOT
# 4 Farmacias
qs=[('¿Tenéis ibuprofeno de 600?',90,330,-3),('¿A qué hora abrís el sábado?',520,400,2),('¿Está lista mi fórmula magistral?',140,520,1),('¿Hacéis test de antígenos?',560,620,-2),('¿Cuál es la farmacia de guardia?',100,720,2)]
bub=''.join(f'<div style="position:absolute;left:{x}px;top:{y}px;transform:rotate({r}deg);background:#ffffff;color:#10203a;border-radius:26px;padding:20px 28px;font-size:28px;font-weight:600;box-shadow:0 20px 50px rgba(0,0,0,.35)">{q}</div>' for q,x,y,r in qs)
P['post4']='<div class="bg" style="background:radial-gradient(circle at 85% 10%,#22d39a66,transparent 45%),radial-gradient(circle at 5% 95%,#3C51D799,transparent 40%),linear-gradient(160deg,#0c2a3a,#06121f)"></div>'+f'''
<div style="position:absolute;left:80px;top:80px"><span class="tag" style="color:#7ff0c4;border:2px solid #7ff0c466">💊 Farmacias</span>
<h1 style="font-size:66px;margin-top:30px">Las mismas preguntas,<br><em style="color:#7ff0c4">todos los días.</em></h1></div>{bub}
<div style="position:absolute;left:80px;right:80px;top:870px;font-size:34px;line-height:1.35;color:#d4fff0">Que las responda la IA, al momento.<br><b style="color:#fff">Vuestro equipo, a atender en el mostrador.</b></div>'''+FOOT
# 5 Agente de voz
bars=''.join(f'<div style="width:14px;border-radius:8px;background:linear-gradient(#7ee8ff,#3C51D7);height:{h}px"></div>' for h in [40,90,150,220,120,260,180,300,140,240,90,200,280,160,110,230,70,180,120,60,40])
P['post5']=NAVY+f'''<div style="position:absolute;left:80px;top:90px;right:80px"><span class="tag" style="color:#7ee8ff;border:2px solid #7ee8ff66">📞 Agente de voz con IA</span>
<h1 style="font-size:80px;margin-top:40px">También coge<br><em style="color:#7ee8ff">el teléfono.</em></h1></div>
<div style="position:absolute;left:80px;top:430px;background:#ffffff12;border:1px solid #ffffff2a;border-radius:24px;padding:18px 28px;font-size:26px">📲 Llamada entrante · <b>Sáb 21:15</b> · <span style="color:#7ee8ff">atendida por IA</span></div><div style="position:absolute;left:80px;right:80px;top:540px;display:flex;align-items:center;justify-content:center;gap:12px;height:320px">{bars}</div>
<div style="position:absolute;left:80px;right:80px;top:880px;display:flex;gap:18px;font-size:26px;flex-wrap:wrap">
<span class="chip">🗣️ Voz natural</span><span class="chip">🌍 Varios idiomas</span><span class="chip">📅 Reserva citas</span><span class="chip">🔀 Pasa a tu equipo si hace falta</span></div>'''+FOOT
# 6 Antes / después
def col(t,c,items,bg): return f'<div style="flex:1;background:{bg};border-radius:32px;padding:40px 36px"><div style="font-size:42px;font-weight:800;color:{c}">{t}</div>'+''.join(f'<div style="font-size:33px;margin-top:34px;line-height:1.3">{i}</div>' for i in items)+'</div>'
P['post6']=NAVY+'''<div style="position:absolute;left:80px;top:80px;right:80px"><h1 style="font-size:72px;margin-top:20px">Vuestra atención,<br><em style="color:#7ee8ff">antes y después.</em></h1></div>
<div style="position:absolute;left:80px;right:80px;top:430px;display:flex;gap:28px">'''+col('Sin asistente','#ff8a8a',['📵 Llamadas perdidas','⏳ Respuestas en horas','😩 El equipo, saturado','🌙 Fuera de horario: nada'],'#ffffff0d')+col('Con asistente IA','#7ee8ff',['✅ Cada mensaje, respondido','⚡ Respuesta en segundos','🙌 El equipo, a lo importante','🌙 24/7, también festivos'],'linear-gradient(160deg,#3C51D7,#1d2a8a)')+'</div>'+FOOT
async def main():
  async with async_playwright() as p:
    b=await p.chromium.launch(executable_path="/usr/bin/google-chrome")
    pg=await b.new_page(viewport={"width":1200,"height":1200})
    for k,v in P.items():
      await pg.set_content(f"<html><head><meta charset='utf-8'><style>{BASE}</style></head><body>{v}</body></html>"); await pg.wait_for_timeout(400)
      await pg.screenshot(path=f"{k}.png")
    await b.close()
asyncio.run(main())
