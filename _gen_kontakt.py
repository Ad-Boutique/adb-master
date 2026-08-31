# Kontaktseite als kleiner Funnel: die Vorauswahl von der Leistungsseite
# kommt per URL mit, danach Projekt, danach Kontakt.
import re
import importlib.util

spec = importlib.util.spec_from_file_location("g", "_gen.py")
g = importlib.util.module_from_spec(spec)
spec.loader.exec_module(g)

STEPS = [
    ("Ihre Auswahl", "Womit sollen wir anfangen?",
     "Mehrfachauswahl ist in Ordnung. Was Sie auf der Leistungsseite gewählt haben, steht schon hier."),
    ("Das Projekt", "Worum geht es?",
     "Grob reicht. Wir brauchen keine Ausschreibung, um zu sagen, ob wir passen."),
    ("Der Kontakt", "Wer meldet sich bei wem?",
     "Ein Gründer sieht sich das an und antwortet unter 24 Stunden, auch wenn es ein Nein wird."),
]

NEEDS = ["Account-Audit", "Meta-Setup", "Google-Setup", "Lead-Kampagne",
         "Creative-Testing", "Tracking-Setup", "Shop & Conversion", "Landingpage",
         "Content-Produktion", "Website oder Relaunch", "Strategie-Session", "Zweitmeinung"]

chips = "\n          ".join(
    '<button class="kchip" data-v="%s" type="button">%s <span class="kx">+</span></button>' % (n, n)
    for n in NEEDS)

BUDGET = ["unter € 3k", "€ 3k bis 10k", "€ 10k bis 25k", "über € 25k", "weiß ich noch nicht"]
WHEN = ["sofort", "im nächsten Monat", "im nächsten Quartal", "wir sondieren"]

budget = "\n          ".join(
    '<button class="kopt" data-g="budget" data-v="%s" type="button">%s</button>' % (b, b) for b in BUDGET)
when = "\n          ".join(
    '<button class="kopt" data-g="when" data-v="%s" type="button">%s</button>' % (w, w) for w in WHEN)

body = '''<main class="kmain">

  <!-- KONTAKT-FUNNEL -->
  <section class="ksec" data-bg="#F3EDE1" data-fg="dark">
    <div class="wrap">
      <a class="svc-back" href="index.html">← Zur Startseite</a>

      <div class="khead">
        <span class="label" style="color:var(--champ-deep);display:block;margin-bottom:clamp(16px,1.8vw,24px)">Anfrage</span>
        <h1 class="dispn" data-lines>
          <span class="rl"><span>Erzählen Sie uns,</span></span>
          <span class="rl"><span>worum es geht.</span></span>
        </h1>
        <p class="klead" data-fade>Drei Schritte, keine Pflichtfelder außer Ihrer Mailadresse. Wir prüfen den Fit in beide Richtungen und sagen offen, wenn wir die Falschen sind.</p>
        <p class="kfrom" data-fade hidden>Sie kommen von <b class="kfromname"></b>. Ihre Auswahl haben wir übernommen.</p>
      </div>

      <div class="kprog" aria-hidden="true">
        <span class="kp on" data-s="1"><i>01</i> Auswahl</span>
        <span class="kp" data-s="2"><i>02</i> Projekt</span>
        <span class="kp" data-s="3"><i>03</i> Kontakt</span>
        <span class="kbar"><i></i></span>
      </div>

      <!-- Schritt 1 -->
      <div class="kstep on" data-s="1">
        <div class="kq">
          <h2 class="kh">Womit sollen wir anfangen?</h2>
          <p class="kt">Mehrfachauswahl ist in Ordnung. Was Sie auf der Leistungsseite gewählt haben, steht schon hier.</p>
        </div>
        <div class="kchips">
          ''' + chips + '''
        </div>
        <div class="kcustom">
          <label for="kfree">Etwas anderes?</label>
          <input id="kfree" class="kinput" type="text" placeholder="In einem Satz, was Sie brauchen">
        </div>
        <div class="knav">
          <span class="khint">Mindestens eine Auswahl oder ein Satz.</span>
          <button class="kbtn knext" type="button" data-to="2">Weiter <i>→</i></button>
        </div>
      </div>

      <!-- Schritt 2 -->
      <div class="kstep" data-s="2">
        <div class="kq">
          <h2 class="kh">Worum geht es?</h2>
          <p class="kt">Grob reicht. Wir brauchen keine Ausschreibung, um zu sagen, ob wir passen.</p>
        </div>
        <div class="kfields">
          <div class="kfield">
            <label for="kfirm">Unternehmen oder Projekt</label>
            <input id="kfirm" class="kinput" type="text" placeholder="Name, Branche, Website">
          </div>
          <div class="kfield">
            <label for="kgoal">Was soll sich ändern?</label>
            <textarea id="kgoal" class="kinput karea" rows="3" placeholder="Zum Beispiel: mehr qualifizierte Anfragen, bessere Marge, neuer Auftritt"></textarea>
          </div>
        </div>
        <div class="kgroup">
          <span class="kglab">Monatliches Mediabudget</span>
          <div class="kopts">
          ''' + budget + '''
          </div>
        </div>
        <div class="kgroup">
          <span class="kglab">Zeitpunkt</span>
          <div class="kopts">
          ''' + when + '''
          </div>
        </div>
        <div class="knav">
          <button class="kback" type="button" data-to="1"><i>←</i> Zurück</button>
          <button class="kbtn knext" type="button" data-to="3">Weiter <i>→</i></button>
        </div>
      </div>

      <!-- Schritt 3 -->
      <div class="kstep" data-s="3">
        <div class="kq">
          <h2 class="kh">Wer meldet sich bei wem?</h2>
          <p class="kt">Ein Gründer sieht sich das an und antwortet unter 24 Stunden, auch wenn es ein Nein wird.</p>
        </div>
        <div class="kfields">
          <div class="kfield">
            <label for="kname">Name</label>
            <input id="kname" class="kinput" type="text" placeholder="Vor- und Nachname">
          </div>
          <div class="kfield">
            <label for="kmail">E-Mail</label>
            <input id="kmail" class="kinput" type="email" placeholder="name@unternehmen.at" required>
          </div>
          <div class="kfield">
            <label for="kphone">Telefon, wenn ein Anruf schneller geht</label>
            <input id="kphone" class="kinput" type="tel" placeholder="optional">
          </div>
        </div>
        <div class="ksum">
          <span class="kslab">Das schicken Sie ab</span>
          <div class="ksumbody"></div>
        </div>
        <div class="knav">
          <button class="kback" type="button" data-to="2"><i>←</i> Zurück</button>
          <button class="kbtn ksend" type="button">Anfrage abschicken <i>→</i></button>
        </div>
        <div class="ktrust">
          <span>Kein Newsletter</span><span>Keine Weitergabe</span><span>Antwort unter 24 h</span>
        </div>
      </div>

      <!-- Bestaetigung -->
      <div class="kstep kdone" data-s="4">
        <div class="kq">
          <h2 class="kh">Ihr Mailprogramm ist offen.</h2>
          <p class="kt">Die Anfrage ist vorformuliert, Sie müssen nur noch senden. Kommt nichts an, schreiben Sie direkt an <a href="mailto:hello@ad.boutique">hello@ad.boutique</a>.</p>
        </div>
        <div class="knav">
          <a class="kbtn" href="work.html">Solange durch die Arbeit blättern <i>→</i></a>
        </div>
      </div>

    </div>
  </section>

'''

page = (g.HEAD.format(title="Anfrage", bodybg="#F3EDE1")
        + g.menu("index.html#kontakt") + body + g.FOOTER)
open("kontakt.html", "w", encoding="utf-8").write(page)
print("kontakt.html geschrieben, %d Zeichen" % len(page))
