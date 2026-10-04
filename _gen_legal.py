# -*- coding: utf-8 -*-
# Impressum und Datenschutz als eigene Seiten (Go-live-Blocker, 4.10.2026).
# Impressum: 1:1 von www.ad.boutique/impressum (Stand 4.10.2026).
# Datenschutz: Text von www.ad.boutique/datenschutz als Basis, angepasst an die neue Seite
# (Verantwortlicher laut Impressum, Hosting Vercel statt Webflow, Einwilligung vor Tracking,
# Adobe Fonts, Formularversand ueber Resend; veraltete Teile wie Privacy Shield, Google Fonts,
# YouTube und Newsletter entfernt). ENTWURF: vor dem Live-Schalter rechtlich pruefen lassen.
import importlib.util

spec = importlib.util.spec_from_file_location("g", "_gen.py")
g = importlib.util.module_from_spec(spec)
spec.loader.exec_module(g)

FIRMA = dict(name="Ad Boutique Agency GmbH", gf="Florian Hörmann, Daniel Hayden",
             sitz="Tuchlauben 13/OG 4, 1010 Wien, Österreich", rechnung="Döblerhofstraße 10/317, 1030 Wien, Österreich",
             fn="FN633351z", uid="ATU81022714", mail="hello@ad.boutique", web="www.ad.boutique")


def link(url, text=None):
    return '<a href="%s" target="_blank" rel="noopener">%s</a>' % (url, text or url.replace("https://", ""))


IMPRESSUM = [
    (None, ['<b>%(name)s</b><br>Geschäftsführung: %(gf)s<br>Firmensitz: %(sitz)s<br>Rechnungsanschrift: %(rechnung)s' % FIRMA,
            'Rechtsform: Gesellschaft mit beschränkter Haftung (GmbH)<br>Unternehmensgegenstand: Betrieb einer Werbeagentur<br>'
            'Registergericht: Wien, Österreich<br>Firmenbuch: %(fn)s<br>Steuernummer: %(uid)s' % FIRMA,
            'E-Mail: <a href="mailto:%(mail)s">%(mail)s</a><br>Website: %(web)s' % FIRMA,
            'Mitglied der WKÖ der Fachgruppe Werbung und Marktkommunikation<br>Zugang zu den Rechtsvorschriften: ' + link("https://www.ris.bka.gv.at")]),
    ("Nutzungsbedingungen", ["Der Inhalt dieser Website ist urheberrechtlich geschützt. Die Nutzung, Vervielfältigung oder Verbreitung dieser Inhalte sind nur mit ausdrücklicher schriftlicher Genehmigung gestattet. Eine Ausnahme gilt für den nicht-kommerziellen, persönlichen Gebrauch."]),
    ("Haftungsausschluss", ["Der Inhalt dieser Website dient nur zu allgemeinen Informationszwecken. Wir übernehmen keine Gewähr für die Vollständigkeit, Richtigkeit und Aktualität der bereitgestellten Informationen und lehnen jede Haftung in diesem Zusammenhang ab.",
                            "Die Website enthält Links zu externen Websites. Wir sind nicht verantwortlich für den Inhalt der Websites, auf die wir verlinken, und übernehmen keine Haftung oder Verantwortung für den Inhalt dieser Websites. Insbesondere können wir nicht garantieren, dass die Websites, auf die wir verlinken, die persönlichen Daten des Nutzers schützen."]),
    ("Streitschlichtung", ["Die Europäische Kommission stellt eine Plattform zur Online-Streitbeilegung (OS) bereit: " + link("https://ec.europa.eu/consumers/odr") + ".",
                           "Unsere E-Mail-Adresse finden Sie oben im Impressum.",
                           "Wir sind nicht bereit oder verpflichtet, an Streitbeilegungsverfahren vor einer Verbraucherschlichtungsstelle teilzunehmen."]),
]

DATENSCHUTZ = [
    ("1. Allgemeines", ["Mit dieser Datenschutzerklärung möchten wir Sie über den Umgang mit Ihren persönlichen Daten beim Besuch dieser Website informieren. ad.boutique legt großen Wert auf den Schutz, die Richtigkeit und die Integrität Ihrer persönlichen Daten. Die Nutzung dieser Website ist freiwillig. Sollten Sie mit der Verwendung Ihrer Daten nicht einverstanden sein, können Sie diese Website jederzeit verlassen. Die hier vorliegende Datenschutzerklärung kann jederzeit geändert oder aktualisiert werden."]),
    ("2. Verantwortliche Organisation", ["Verantwortlich für die Verarbeitung ist:",
                                         '<b>%(name)s</b><br>%(sitz)s<br><a href="mailto:%(mail)s">%(mail)s</a>' % FIRMA]),
    ("3. Sicherheitsvorkehrungen", ["Wir setzen organisatorische, vertragliche und technische Sicherheitsvorkehrungen nach dem Stand der Technik ein, um die Einhaltung der datenschutzrechtlichen Bestimmungen sowie den Schutz der von uns verwendeten Daten gegen zufällige oder vorsätzliche Manipulationen, Verlust, Zerstörung oder den Zugriff unberechtigter Personen zu gewährleisten. Zu den Sicherheitsmaßnahmen gehört insbesondere die verschlüsselte Übertragung aller Daten zwischen Ihrem Browser und unserem Server."]),
    ("4. Weitergabe von Informationen an Dritte", ["Personenbezogene Daten werden nur dann an Dritte weitergegeben, wenn dies erforderlich ist, etwa zu Vertragszwecken gemäß Art. 6 Abs. 1 lit. b DSGVO oder auf Grundlage der berechtigten Interessen eines wirtschaftlichen und effizienten Geschäftsbetriebs gemäß Art. 6 Abs. 1 lit. f DSGVO.",
                                                   "Bei der Beauftragung von Auftragsverarbeitern treffen wir rechtliche Vorkehrungen sowie technische und organisatorische Maßnahmen, um die Sicherheit personenbezogener Daten gemäß den datenschutzrechtlichen Bestimmungen zu gewährleisten."]),
    ("5. Kontakt und Anfrageformular", ["Wenn Sie uns per E-Mail oder über das Anfrageformular kontaktieren, verarbeiten wir Ihre Angaben (Auswahl, Projekt, Ziel, Budget, Zeitpunkt, Name, E-Mail-Adresse, Telefonnummer, Seite, von der Sie kommen) zur Bearbeitung Ihrer Anfrage gemäß Art. 6 Abs. 1 lit. b DSGVO. Die Daten können in unserem Customer-Relationship-Management-System gespeichert werden. Zum Schutz vor Missbrauch des Formulars (massenhaftes Absenden) halten wir die IP-Adresse des absendenden Geräts höchstens 10 Minuten im Arbeitsspeicher des Servers und löschen sie danach (Art. 6 Abs. 1 lit. f DSGVO).",
                                        "Für den Versand der Formular-Anfragen per E-Mail nutzen wir Resend (Resend, Inc., USA) als Auftragsverarbeiter. Dabei werden die Formularinhalte an Resend übermittelt und an unser Postfach zugestellt. Die Übermittlung in die USA erfolgt auf Grundlage der Standardvertragsklauseln der EU-Kommission bzw. des EU-US Data Privacy Framework."]),
    ("6. Hosting", ["Diese Website wird von Vercel Inc., 440 N Barranca Ave #4133, Covina, CA 91723, USA, gehostet. Beim Besuch der Website verarbeitet Vercel technisch notwendige Daten einschließlich Ihrer IP-Adresse, um die Seiten auszuliefern und den sicheren Betrieb zu gewährleisten. Die Verarbeitung erfolgt auf Grundlage von Art. 6 Abs. 1 lit. f DSGVO; unser berechtigtes Interesse liegt in einer zuverlässigen und sicheren Darstellung der Website.",
                    "Mit Vercel besteht ein Vertrag über die Auftragsverarbeitung. Die Übermittlung in die USA erfolgt auf Grundlage der Standardvertragsklauseln der EU-Kommission bzw. des EU-US Data Privacy Framework."]),
    ("7. Erhebung von Daten und Logfiles", ["Wir erheben Daten auf Grundlage berechtigter Interessen gemäß Art. 6 Abs. 1 lit. f DSGVO über jeden Zugriff auf den Server des Dienstes (sogenannte Serverlogfiles). Zu den Zugriffsdaten gehören Name der abgerufenen Webseite, Datei, Datum und Uhrzeit des Abrufs, übertragene Datenmenge, Meldung über erfolgreichen Abruf, Browsertyp und Version, das Betriebssystem, Referrer-URL (die zuvor besuchte Seite), IP-Adresse sowie der anfragende Provider.",
                                            "Aus Sicherheitsgründen (z. B. zur Aufklärung von Missbrauch oder Betrug) werden Logfile-Informationen für maximal sieben Tage gespeichert und danach gelöscht. Daten, für die eine Beweissicherung erforderlich ist, sind bis zur Klärung des Vorfalls von der Löschung ausgeschlossen."]),
    ("8. Cookies, lokale Speicherung und Einwilligung", ["Ohne Ihre Einwilligung setzt diese Website keine Cookies für Statistik oder Werbung. Technisch notwendig speichern wir im Speicher Ihres Browsers (Local Storage, Session Storage) nur Ihre Auswahl im Einwilligungs-Hinweis samt Datum der Wahl, ob die Einführung zum Menü schon gezeigt wurde, und für die Dauer des Besuchs Angaben für die Seitenübergänge (z. B. welche Kachel Sie angeklickt haben, damit der Übergang an der richtigen Stelle beginnt). Diese Werte verlassen Ihr Gerät nicht. Rechtsgrundlage ist Art. 6 Abs. 1 lit. f DSGVO in Verbindung mit § 165 Abs. 3 TKG 2021.",
                                                        "Erst wenn Sie im Hinweis \"Alle akzeptieren\" wählen, laden wir Google Tag Manager, Google Analytics und das Meta-Pixel (Abschnitte 9 bis 11). Rechtsgrundlage ist dann Ihre Einwilligung gemäß Art. 6 Abs. 1 lit. a DSGVO und § 165 Abs. 3 TKG 2021. Sie können Ihre Einwilligung jederzeit mit Wirkung für die Zukunft widerrufen: über den Link \"Cookie-Einstellungen\" im Fußbereich jeder Seite. Beim Widerruf löschen wir die gesetzten Cookies von Google und Meta und laden die Seite ohne diese Dienste neu.",
                                                        "Nach Ihrer Einwilligung werden insbesondere folgende Cookies gesetzt:",
                                                        "<b>_ga</b>: Statistik, dient zur Unterscheidung zwischen Nutzern, gesetzt von Google, Speicherdauer 2 Jahre.<br><b>_fbp</b>: Statistik und Werbung, dient zur Unterscheidung zwischen Nutzern und ermöglicht die Auslieferung gezielter Werbung, gesetzt von Meta, Speicherdauer 3 Monate.",
                                                        "Sie können Cookies außerdem jederzeit in den Einstellungen Ihres Browsers löschen oder blockieren. Der Ausschluss von Cookies kann zu Funktionseinschränkungen führen."]),
    ("9. Google Tag Manager und Google Analytics", ["Mit Ihrer Einwilligung setzen wir den Google Tag Manager und Google Analytics ein, Dienste der Google Ireland Limited, Gordon House, Barrow Street, Dublin 4, Irland (\"Google\"). Der Tag Manager verwaltet die Einbindung der Analyse- und Marketingdienste; Google Analytics wertet die Nutzung unserer Website aus und erstellt Berichte über die Aktivitäten auf der Website. Dabei können pseudonyme Nutzungsprofile erstellt werden. Die IP-Adresse wird gekürzt.",
                                                   "Eine Übermittlung an Google LLC in den USA ist möglich; sie erfolgt auf Grundlage des EU-US Data Privacy Framework bzw. der Standardvertragsklauseln der EU-Kommission. Weitere Informationen: " + link("https://policies.google.com/technologies/partner-sites?hl=de") + ", " + link("https://policies.google.com/technologies/ads?hl=de") + "."]),
    ("10. Google-Marketing-Services", ["Mit Ihrer Einwilligung nutzen wir Marketing- und Remarketing-Dienste von Google (z. B. Google Ads Conversion-Tracking und Remarketing). Damit können wir messen, ob eine Anzeige zu einer Anfrage geführt hat, und Anzeigen Nutzern zeigen, die sich für unser Angebot interessiert haben. Dazu werden Cookies auf Ihrem Gerät gespeichert, die pseudonyme Informationen über Ihre Nutzung enthalten (aufgerufene Seiten, technische Informationen über Browser und Betriebssystem, verweisende Seiten, Zeitpunkt des Zugriffs). Google speichert dabei nicht Ihren Namen oder Ihre E-Mail-Adresse.",
                                       "Wenn Sie der interessenbezogenen Werbung durch Google widersprechen möchten, können Sie die Einstellungen von Google nutzen: " + link("https://adssettings.google.com") + "."]),
    ("11. Meta-Pixel", ["Mit Ihrer Einwilligung verwenden wir das Meta-Pixel der Meta Platforms Ireland Limited, Merrion Road, Dublin 4, D04 X2K5, Irland (\"Meta\"). Damit können wir Besucher unserer Website als Zielgruppe für Anzeigen auf Facebook und Instagram bestimmen (\"Custom Audiences\") und die Wirksamkeit dieser Anzeigen messen (\"Conversion\"). Dabei kann ein Cookie auf Ihrem Gerät gespeichert werden. Sind Sie bei Facebook oder Instagram angemeldet, kann Meta den Besuch Ihrem Konto zuordnen.",
                        "Eine Übermittlung an Meta Platforms, Inc. in den USA ist möglich; sie erfolgt auf Grundlage des EU-US Data Privacy Framework bzw. der Standardvertragsklauseln der EU-Kommission. Weitere Informationen: " + link("https://www.facebook.com/privacy/policy/") + ". Einstellungen zu Werbeanzeigen: " + link("https://www.facebook.com/settings?tab=ads") + "."]),
    ("12. Schriftarten", ["Für die Schriftart Amandine nutzen wir Adobe Fonts der Adobe Systems Software Ireland Limited, 4-6 Riverwalk, Citywest Business Campus, Dublin 24, Irland. Beim Aufruf einer Seite lädt Ihr Browser die Schriftdateien von Servern von Adobe; dabei wird Ihre IP-Adresse an Adobe übermittelt. Rechtsgrundlage ist Art. 6 Abs. 1 lit. f DSGVO; unser berechtigtes Interesse liegt in einer einheitlichen Darstellung der Website. Weitere Informationen: " + link("https://www.adobe.com/de/privacy/policies/adobe-fonts.html") + ".",
                          "Alle anderen Schriften, Bilder und Videos liefern wir von unserem eigenen Server aus."]),
    ("13. Rechte von Nutzer*innen", ["Sie haben das Recht, auf Antrag unentgeltlich Auskunft über die über Sie gespeicherten personenbezogenen Daten zu erhalten, sowie das Recht auf Berichtigung unrichtiger Daten, Einschränkung der Verarbeitung, Löschung, Datenübertragbarkeit und Widerruf einer Einwilligung mit Wirkung für die Zukunft.",
                                     "Wenn Sie glauben, dass die Verarbeitung Ihrer Daten gegen das Datenschutzrecht verstößt, können Sie sich bei der Aufsichtsbehörde beschweren. In Österreich ist das die Datenschutzbehörde: " + link("https://www.dsb.gv.at") + "."]),
    ("14. Löschung von Daten", ["Die Löschung der bei uns gespeicherten Daten erfolgt, wenn sie für die Erfüllung des Zwecks nicht mehr erforderlich sind und sofern der Löschung keine gesetzlichen Aufbewahrungspflichten entgegenstehen. Sollten Daten nicht gelöscht werden, weil sie für andere gesetzliche Zwecke benötigt werden, wird die Verarbeitung eingeschränkt. Das gilt etwa für Daten, die aus unternehmens- oder steuerrechtlichen Gründen aufbewahrt werden müssen. Grundsätzlich erfolgt die Speicherung für bis zu 10 Jahre."]),
    ("15. Widerspruchsrecht", ["Sie haben das Recht, der künftigen Verarbeitung Ihrer personenbezogenen Daten nach Maßgabe der gesetzlichen Bestimmungen jederzeit zu widersprechen, insbesondere der Verarbeitung für Zwecke der Direktwerbung."]),
    ("16. Änderungen der Datenschutzerklärung", ["Wir behalten uns vor, die Datenschutzerklärung an geänderte Rechtslagen oder an Änderungen des Dienstes und der Datenverarbeitung anzupassen. Bitte informieren Sie sich regelmäßig über den Inhalt dieser Datenschutzerklärung.",
                                                 "Stand: Oktober 2026"]),
]


def page(slug, title, lines, blocks):
    parts = []
    for head, paras in blocks:
        h = ('        <h2 class="lgh">%s</h2>\n' % head) if head else ""
        ps = "".join('        <p>%s</p>\n' % p for p in paras)
        parts.append('      <div class="lgblock">\n' + h + ps + '      </div>\n')
    body = '''<main class="lgmain">

  <!-- RECHTLICHES -->
  <section class="sec fg-light bg-paper lgsec" data-bg="#F4F3EB" data-fg="dark">
    <div class="wrap">
      <a class="svc-back" href="index.html">← Zur Startseite</a>
      <div class="lghead">
        <h1 class="dispn" data-lines>
          <span class="rl"><span>%s</span></span>
          <span class="rl"><span>%s</span></span>
        </h1>
      </div>
      <div class="lgbody">
%s      </div>
    </div>
  </section>
''' % (lines[0], lines[1], "".join(parts))
    return {slug + ".html": g.HEAD.format(title=title, bodybg="#F4F3EB") + g.menu("index.html") + body + g.FOOTER}


# fertig(): die Nachlauf-Regeln (_nachlauf.py) laufen gleich beim Erzeugen, wie bei den anderen Generatoren
import _nachlauf
seiten = page("impressum", "Impressum", ("Impressum,", "wer hinter ad.boutique steht."), IMPRESSUM)
seiten.update(page("datenschutz", "Datenschutz", ("Datenschutz,", "was mit Ihren Daten passiert."), DATENSCHUTZ))
_nachlauf.fertig(seiten)
print("Rechtliches: impressum.html, datenschutz.html geschrieben")
