"""Carrusel IG 1080x1350 (estilo azul neón). Uso: python3 tools/ig_carrusel.py <prefijo_salida>
Genera <prefijo>-01.jpg ... según la lista S. Base: render_fotos.py."""
import asyncio, sys
from playwright.async_api import async_playwright
W,H=1080,1350
BASE=f"""*{{margin:0;box-sizing:border-box}}body{{width:{W}px;height:{H}px;font-family:Poppins,sans-serif;color:#fff;overflow:hidden;position:relative;background:#070a24}}
.bg{{position:absolute;inset:0;z-index:-1;background:radial-gradient(circle at 85% 12%,#3C51D7aa,transparent 45%),radial-gradient(circle at 8% 92%,#00dcff40,transparent 40%),linear-gradient(160deg,#141a4d,#070a24)}}
.tag{{display:inline-block;font-size:24px;font-weight:700;letter-spacing:3px;text-transform:uppercase;border-radius:40px;padding:10px 26px;color:#7ee8ff;border:2px solid #7ee8ff66}}
h1{{font-weight:800;line-height:1.08}}em{{font-style:normal;color:#7ee8ff}}
.brand{{position:absolute;left:70px;bottom:56px;font-weight:800;font-size:34px}}.brand b{{color:#6f84ff}}
.url{{position:absolute;right:70px;bottom:62px;font-size:26px;color:#aab4ff}}
.pg{{position:absolute;right:70px;top:70px;font-size:22px;color:#aab4ff;font-weight:600}}
.phone{{position:absolute;left:50%;transform:translateX(-50%);width:760px;border-radius:52px;background:#0b141a;border:12px solid #1d2340;box-shadow:0 40px 120px rgba(0,0,0,.55),0 0 80px rgba(93,116,255,.35);overflow:hidden}}
.wa-top{{background:#1f2c34;height:104px;display:flex;align-items:center;padding:0 26px;gap:16px;font-size:26px}}
.av{{width:58px;height:58px;border-radius:50%;background:linear-gradient(135deg,#3C51D7,#7ee8ff);display:flex;align-items:center;justify-content:center;font-weight:800;font-size:22px}}
.wa-body{{padding:26px 22px;display:flex;flex-direction:column;gap:16px}}
.b{{max-width:84%;padding:16px 20px;border-radius:20px;font-size:26px;line-height:1.38}}
.in{{background:#005c4b;margin-left:auto;border-top-right-radius:4px}}.out{{background:#202c33;border-top-left-radius:4px}}
.t{{font-size:16px;color:#9fb3bf;text-align:right;margin-top:4px}}
.row{{display:flex;align-items:center;border-bottom:1px solid #ffffff1e;padding:24px 0;font-size:29px}}
.row div:first-child{{flex:1}}.row .c{{width:170px;text-align:center;font-size:38px}}
"""
FOOT='<div class="brand">Digital <b>ImPad</b></div><div class="url">digitalimpad.com</div>'
S=[]
# 1 Gancho
S.append('''<div style="position:absolute;left:70px;top:110px;right:70px"><span class="tag">🏠 Inmobiliarias</span>
<h1 style="font-size:86px;margin-top:50px">“Pulsa 1<br>para comprar.<br>Pulsa 2<br>para alquilar.”</h1>
<p style="font-size:40px;line-height:1.4;color:#c9d0ff;margin-top:50px">Si tu bot todavía habla así,<br><b style="color:#fff">estás perdiendo compradores.</b></p>
<div style="margin-top:70px;font-size:30px;color:#7ee8ff;font-weight:600">Bot de menús vs. agente con IA →</div></div>''')
# 2 Bot de menús
S.append('''<div style="position:absolute;left:70px;top:90px;right:70px"><span class="tag" style="color:#ff9a9a;border-color:#ff9a9a66">❌ Bot de menús</span>
<h1 style="font-size:58px;margin-top:30px">Solo entiende botones.</h1></div>
<div class="phone" style="top:340px"><div class="wa-top"><div class="av">IN</div><div>Inmobiliaria<br><span style="font-size:18px;color:#9fb3bf">bot automático</span></div></div>
<div class="wa-body">
<div class="b out">Bienvenido. Elige una opción:<br>1️⃣ Comprar<br>2️⃣ Alquilar<br>3️⃣ Hablar con un asesor<div class="t">21:10</div></div>
<div class="b in">Busco una vivienda de 3 dormitorios cerca del centro, con garaje<div class="t">21:11 ✓✓</div></div>
<div class="b out">Opción no válida. Pulsa 1, 2 o 3.<div class="t">21:11</div></div>
<div class="b in">3<div class="t">21:12 ✓✓</div></div>
<div class="b out">Un asesor te responderá en horario de oficina. 🕘<div class="t">21:12</div></div>
</div></div>''')
# 3 Agente IA
S.append('''<div style="position:absolute;left:70px;top:90px;right:70px"><span class="tag">✅ Agente de ventas con IA</span>
<h1 style="font-size:58px;margin-top:30px">Entiende lo que buscas.</h1></div>
<div class="phone" style="top:340px"><div class="wa-top"><div class="av">IN</div><div>Inmobiliaria<br><span style="font-size:18px;color:#7ee8ff">en línea · asistente IA</span></div></div>
<div class="wa-body">
<div class="b in">Busco una vivienda de 3 dormitorios cerca del centro, con garaje<div class="t">21:11 ✓✓</div></div>
<div class="b out">¡Hola! Tengo 3 opciones así en la zona centro 🏡 ¿Es para comprar o alquilar, y qué presupuesto manejas?<div class="t">21:11</div></div>
<div class="b in">Comprar, hasta 150.000<div class="t">21:12 ✓✓</div></div>
<div class="b out">Te paso fotos y ficha de las 2 que encajan 📎 ¿Quieres visitarlas el sábado a las 10:00 o a las 12:00?<div class="t">21:12</div></div>
</div></div>''')
# 4 Comparativa
rows=[('Entiende mensajes escritos con tus palabras','❌','✅'),('Recomienda propiedades según lo que buscas','❌','✅'),('Pregunta presupuesto, zona y plazos','❌','✅'),('Agenda la visita al momento','❌','✅'),('Responde 24/7, también fines de semana','⚠️','✅'),('Pasa a un asesor con todo el contexto','❌','✅')]
S.append('<div style="position:absolute;left:70px;top:110px;right:70px"><h1 style="font-size:66px">Frente a frente</h1>'
 '<div class="row" style="font-size:24px;color:#aab4ff;font-weight:700;margin-top:40px;border-bottom:2px solid #5d74ff"><div></div><div class="c" style="font-size:22px">Bot de<br>menús</div><div class="c" style="font-size:22px;color:#7ee8ff">Agente<br>con IA</div></div>'
 +''.join(f'<div class="row"><div>{a}</div><div class="c">{b}</div><div class="c">{c}</div></div>' for a,b,c in rows)+'</div>')
# 5 Qué hace
items=[('🔎','Recomienda propiedades','según zona, precio y necesidades'),('🎯','Califica cada contacto','presupuesto, plazos, compra o alquiler'),('📎','Envía fotos y fichas','sin que nadie las busque'),('📅','Reserva la visita','y manda el recordatorio'),('🤝','Avisa a tu asesor','con un resumen de la conversación')]
S.append('<div style="position:absolute;left:70px;top:110px;right:70px"><span class="tag">🤖 Tu agente de ventas</span><h1 style="font-size:62px;margin-top:30px">Mientras tu equipo<br><em>descansa</em>, él:</h1>'
 +''.join(f'<div style="display:flex;gap:28px;align-items:center;margin-top:34px"><div style="width:100px;height:100px;flex:none;border-radius:28px;background:#111a4a;border:2px solid #5d74ff;display:flex;align-items:center;justify-content:center;font-size:48px;box-shadow:0 0 40px #3C51D766">{i}</div><div><div style="font-size:34px;font-weight:700">{t}</div><div style="font-size:26px;color:#c9d0ff">{d}</div></div></div>' for i,t,d in items)+'</div>')
# 6 CTA
S.append('''<div style="position:absolute;left:70px;right:70px;top:250px;text-align:center">
<div style="width:200px;height:200px;margin:0 auto;border-radius:50%;background:radial-gradient(circle,#7ee8ff,#3C51D7);display:flex;align-items:center;justify-content:center;font-size:100px;box-shadow:0 0 100px #7ee8ffaa">🏡</div>
<h1 style="font-size:72px;margin-top:70px">¿Lo probamos en<br><em>tu inmobiliaria?</em></h1>
<p style="font-size:34px;color:#c9d0ff;margin-top:36px;line-height:1.4">Un agente con IA entrenado con tus propiedades, en WhatsApp, Instagram y tu web.</p>
<div style="display:inline-block;margin-top:60px;background:linear-gradient(90deg,#3C51D7,#00b8e6);border-radius:60px;padding:28px 60px;font-size:40px;font-weight:800;box-shadow:0 0 60px #3C51D7aa">📩 Escríbenos por DM</div>
<div style="margin-top:30px;font-size:30px;color:#aab4ff">@digitalimpad</div></div>''')
async def main(pref):
  async with async_playwright() as p:
    b=await p.chromium.launch(executable_path="/usr/bin/google-chrome")
    pg=await b.new_page(viewport={"width":W,"height":H})
    n=len(S)
    for i,v in enumerate(S,1):
      await pg.set_content(f"<html><head><meta charset='utf-8'><style>{BASE}</style></head><body><div class='bg'></div>{v}<div class='pg'>{i}/{n}</div>{FOOT}</body></html>"); await pg.wait_for_timeout(400)
      await pg.screenshot(path=f"{pref}-{i:02d}.jpg",type="jpeg",quality=92)
    await b.close()
asyncio.run(main(sys.argv[1]))
