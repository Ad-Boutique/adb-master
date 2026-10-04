# -*- coding: utf-8 -*-
"""Performance-Seite nach den Apple-Prinzipien als Vorschau-Seite (v3).
Ableitung aus der generierten Seite: Stat-Group statt Pillen im Hero, ein Beispiel
mit Fett-Lead im Problem, Chips ueber den Stationen, Vergleich statt Liste, Kapitel-Leiste.
Abgeleitet wird im Nachlauf (_nachlauf.py, Tabelle ABLEITUNGEN): _gen_services.py erzeugt die Leistungsseite,
nach der Regel "brand" entsteht daraus mit ableiten() diese Seite, danach laufen beide durch die restlichen Regeln.
Anker sind Struktur (Sektions-id, Klassen) und Marker-Kommentare, kein Fliesstext; fehlt einer, bricht der Build
mit einer Meldung aus _anker.py ab."""
import re
from _anker import AnkerFehlt, einmal, finde
from _brand_inplace import layout

SRC = "service-performance-marketing.html"
OUT = "service-performance-marketing-v3.html"

BEISPIEL = ('\n          <p class="cap" data-fade style="margin-top:18px"><b>Ein Beispiel.</b> Ein Finance-Kunde hatte einen Paid-Kanal '
            'laufen, den niemand messen konnte. Wir haben ihn messbar gemacht, an der Hypothese geprüft und geschlossen.</p>')


def ableiten(h):
    """HTML der Leistungsseite (Stand nach der Regel "brand") -> HTML der Vorschau-Seite."""
    h = einmal(h, "<title>", "<title>Vorschau v3, ", "Title")

    # 0. Kapitel-Leiste gibt es nicht mehr (24.9.2026); die Sektions-IDs kommen aus dem Generator

    # 1. Hero: Zahlen statt Schlagwoerter (nur noch, wenn der alte Hero da ist; seit 3.10.2026 Woerterbuch-Hero)
    if '<div class="tags" data-fade>' in h:
        h = einmal(h, '''      <div class="tags" data-fade>
        <span>Meta, Google, TikTok</span>
        <span>Lead-Generierung</span>
        <span>Creative-Testing</span>
        <span>Ehrliche Attribution</span>
      </div>''',
    '''      <div class="statg" data-stagger>
        <div class="st" data-fade><div class="sv">489</div><div class="sc">Anfragen, ein Neubauprojekt</div></div>
        <div class="st" data-fade><div class="sv">€ 11,77</div><div class="sc">je Anfrage, alle Motive gerechnet</div></div>
        <div class="st" data-fade><div class="sv">8,75</div><div class="sc">ROAS Crowdinvesting, vorher 2,14</div></div>
      </div>''', "Hero-Tags")

    # 2. Problem: die unbequeme Wahrheit als Beispiel, Fett-Lead. Eingesetzt nach dem letzten Absatz der
    # Text-Spalte in der Sektion id="problem" (Struktur, nicht der Wortlaut des Absatzes)
    a = finde(h, '<section id="problem"', "Problem-Sektion")
    b = finde(h, "</section>", "Problem-Sektion (Ende)", a)
    i = h.rfind("</p>\n        </div>", a, b)
    if i < 0:
        raise AnkerFehlt("Problem-Sektion: kein Absatz am Ende der Text-Spalte ('</p>' vor '        </div>')")
    i += len("</p>")
    h = h[:i] + BEISPIEL + h[i:]

    # 3. Stationen: Chips zum Anzeigen und Springen
    h = einmal(h, '''    <div class="wrap">
      <div class="tell">''',
    '''    <div class="wrap">
      <div class="hlxnav tellnav" role="tablist">
        <button class="hn on" type="button">Budget</button>
        <button class="hn" type="button">Anfragen</button>
        <button class="hn" type="button">Preis</button>
        <button class="hn" type="button">Erkenntnis</button>
      </div>
      <div class="tell">''', "Stationen")

    # 4. Cases: Vergleich statt Liste (zwischen den Marker-Kommentaren der Cases und der Kundenstimme)
    start = finde(h, "  <!-- 07, CASES -->", "Cases (Marker-Kommentar)")
    end = finde(h, "  <!-- WAS KUNDEN SAGEN -->", "Kundenstimme (Marker-Kommentar)")
    m = re.search(r'<p class="morecases".*?</p>', h[start:end], re.S)
    if not m:
        raise AnkerFehlt('Cases: Zeile "Auch mit dieser Leistung" (p.morecases) fehlt')
    more = m.group(0)
    compare = '''  <!-- 07, VERGLEICH: drei Wohnbau-Projekte nebeneinander -->
  <section id="vergleich" class="sec fg-light bg-cream" data-bg="#EFE7D6" data-fg="dark" style="padding-top:clamp(60px,7vw,100px)">
    <div class="wrap">
      <span class="label" style="color:var(--champ-deep);display:block;margin-bottom:16px">Drei Wohnbau-Projekte im Vergleich</span>
      <h2 class="dispn" data-lines style="font-size:clamp(28px,3.2vw,50px);max-width:20ch"><span class="rl"><span>Gleiche Stadt, gleicher Kanal,</span></span><span class="rl"><span>drei Preise je Anfrage.</span></span></h2>
      <div class="cmp" data-stagger>
        <div class="cmprow cmprow--head" data-fade>
          <div></div>
          <a href="case-premium-neubau.html">Premium-Neubau, Wien</a>
          <a href="case-bautraeger-portfolio.html">Bauträger-Portfolio, Wien</a>
          <a href="case-wohnbau-floridsdorf.html">Wohnbau, Floridsdorf</a>
        </div>
        <div class="cmprow" data-fade>
          <div class="cmpl">Anfragen</div>
          <div class="cmpv">489</div>
          <div class="cmpv">546</div>
          <div class="cmpv">460</div>
        </div>
        <div class="cmprow" data-fade>
          <div class="cmpl">Preis je Anfrage</div>
          <div class="cmpv">€ 11,77</div>
          <div class="cmpv">€ 5,93</div>
          <div class="cmpv">€ 12,77</div>
        </div>
        <div class="cmprow" data-fade>
          <div class="cmpl">Zeitraum und Strecke</div>
          <div class="cmpd">Jänner bis Mai 2026, Meta mit Instant Forms</div>
          <div class="cmpd">Zweites Quartal 2026, zwei Projekte parallel</div>
          <div class="cmpd">Erstes Quartal, dann zweites mit anderem Ziel</div>
        </div>
        <div class="cmprow" data-fade>
          <div class="cmpl">Was den Unterschied machte</div>
          <div class="cmpd">Vier Motive im Test, ein Interior-Motiv trug 54 Prozent. Später Wellen unter € 5.</div>
          <div class="cmpd">Zwei Projekte, ein Setup: Was im ersten gelernt wurde, senkte im zweiten den Preis.</div>
          <div class="cmpd">Erst Volumen, dann bewusst weniger Anfragen zu höherer Qualität: 232 im zweiten Quartal, 18 statt 8 qualifiziert.</div>
        </div>
        <div class="cmprow cmprow--go" data-fade>
          <div></div>
          <a class="zalink" href="case-premium-neubau.html">Case ansehen</a>
          <a class="zalink" href="case-bautraeger-portfolio.html">Case ansehen</a>
          <a class="zalink" href="case-wohnbau-floridsdorf.html">Case ansehen</a>
        </div>
      </div>
      <p class="cap" data-fade style="margin-top:clamp(28px,3.4vw,48px);max-width:60ch"><b>Und außerhalb vom Wohnbau.</b> Crowdinvesting-Plattform: ROAS 8,75 statt 2,14 bei gleichem Budget. Dental-Marke: 1.385 Verkäufe, Ziel-Gap offen reportet. Nordic Spirit: 23.579 Abschlüsse in zwölf Monaten zu € 11,70.</p>
      ''' + more + '''
    </div>
  </section>

'''
    h = h[:start] + compare + h[end:]

    # Sektionsabstaende und Seitenrand wie auf allen Seiten (Layout-Abteilung)
    return layout(h, OUT)


if __name__ == "__main__":
    # Einzeln: aus der fertigen Leistungsseite ableiten und die restlichen Regeln anwenden. Verbindlich ist der Build.
    import _nachlauf
    h = _nachlauf.bearbeite({OUT: ableiten(open(SRC, encoding="utf-8").read())}, ab="footer")[OUT]
    open(OUT, "w", encoding="utf-8").write(h)
    print("geschrieben:", OUT, "Sektionen:", h.count("<section"))
