// Anfrage aus dem Kontakt-Funnel (kontakt.html, master.js "Absenden") als E-Mail ueber Resend.
// Vercel Function (Node). Umgebungsvariablen in Vercel (nie ins Repo):
//   RESEND_API_KEY  API-Schluessel von resend.com
//   ANFRAGE_TO      Empfaenger, mehrere mit Komma getrennt (z. B. hello@ad.boutique)
//   ANFRAGE_FROM    optional, Absender einer bei Resend bestaetigten Domain (Standard: Anfrage <anfrage@ad.boutique>)
// Antwort immer JSON: { ok: true } oder { ok: false, error: "..." }. Fehlt etwas, faellt das Formular auf mailto zurueck.

const MAX = { text: 2000, short: 200 };

function clean(v, n) {
  return String(v == null ? "" : v).replace(/\r/g, "").trim().slice(0, n);
}

function esc(s) {
  return s.replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
}

async function readBody(req) {
  if (req.body && typeof req.body === "object") return req.body;
  if (typeof req.body === "string") return JSON.parse(req.body || "{}");
  const chunks = [];
  for await (const c of req) chunks.push(c);
  return JSON.parse(Buffer.concat(chunks).toString("utf8") || "{}");
}

module.exports = async function handler(req, res) {
  res.setHeader("Content-Type", "application/json; charset=utf-8");
  res.setHeader("Cache-Control", "no-store");
  const send = (code, obj) => { res.statusCode = code; res.end(JSON.stringify(obj)); };

  if (req.method !== "POST") return send(405, { ok: false, error: "method" });

  let b;
  try { b = await readBody(req); } catch (e) { return send(400, { ok: false, error: "json" }); }

  // Honeypot: echte Besucher sehen das Feld nicht. Gefuellt heisst Bot; still "ok" melden, nichts senden.
  if (clean(b.website, MAX.short)) return send(200, { ok: true });

  const d = {
    wahl: clean(b.wahl, MAX.text),
    projekt: clean(b.projekt, MAX.short),
    ziel: clean(b.ziel, MAX.text),
    budget: clean(b.budget, MAX.short),
    zeitpunkt: clean(b.zeitpunkt, MAX.short),
    herkunft: clean(b.herkunft, MAX.short),
    name: clean(b.name, MAX.short),
    mail: clean(b.mail, MAX.short),
    telefon: clean(b.telefon, MAX.short),
  };
  if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(d.mail)) return send(422, { ok: false, error: "mail" });
  if (!d.wahl && !d.ziel && !d.projekt) return send(422, { ok: false, error: "inhalt" });

  const key = process.env.RESEND_API_KEY;
  const to = (process.env.ANFRAGE_TO || "").split(",").map((s) => s.trim()).filter(Boolean);
  if (!key || !to.length) return send(503, { ok: false, error: "konfiguration" });

  const rows = [
    ["Womit", d.wahl], ["Unternehmen/Projekt", d.projekt], ["Was sich aendern soll", d.ziel],
    ["Monatliches Mediabudget", d.budget], ["Zeitpunkt", d.zeitpunkt], ["Gekommen ueber", d.herkunft],
    ["Name", d.name], ["E-Mail", d.mail], ["Telefon", d.telefon],
  ].filter((r) => r[1]);
  const text = rows.map((r) => r[0] + ": " + r[1]).join("\n");
  const html = "<table>" + rows.map((r) => "<tr><td style=\"padding:4px 12px 4px 0;vertical-align:top\"><b>" + esc(r[0]) +
    "</b></td><td style=\"padding:4px 0\">" + esc(r[1]).replace(/\n/g, "<br>") + "</td></tr>").join("") + "</table>";

  try {
    const r = await fetch("https://api.resend.com/emails", {
      method: "POST",
      headers: { Authorization: "Bearer " + key, "Content-Type": "application/json" },
      body: JSON.stringify({
        from: process.env.ANFRAGE_FROM || "Anfrage <anfrage@ad.boutique>",
        to,
        reply_to: d.mail,
        subject: "Anfrage: " + (d.wahl || d.projekt || "Projekt").slice(0, 120),
        text,
        html,
      }),
    });
    if (!r.ok) return send(502, { ok: false, error: "versand" });
    return send(200, { ok: true });
  } catch (e) {
    return send(502, { ok: false, error: "versand" });
  }
};
