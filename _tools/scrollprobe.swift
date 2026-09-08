import WebKit
import AppKit
// Seite laden, in Schritten durchscrollen, danach JavaScript auswerten:
// scrollprobe <url> <breite> <hoehe> <js-datei> [schritte] [pause-sekunden]
let a = CommandLine.arguments
let url = URL(string: a[1])!
let w = Double(a[2]) ?? 390, h = Double(a[3]) ?? 800
let js = (try? String(contentsOfFile: a[4], encoding: .utf8)) ?? "1"
let steps = a.count > 5 ? Int(a[5]) ?? 24 : 24
let pause = a.count > 6 ? Double(a[6]) ?? 0.45 : 0.45

let app = NSApplication.shared; app.setActivationPolicy(.prohibited)
let cfg = WKWebViewConfiguration()
let view = WKWebView(frame: NSRect(x: 0, y: 0, width: w, height: h), configuration: cfg)
let win = NSWindow(contentRect: NSRect(x: 0, y: 0, width: w, height: h), styleMask: [.borderless], backing: .buffered, defer: false)
win.contentView = view; win.orderBack(nil)
final class Nav: NSObject, WKNavigationDelegate {
  var done = false
  func webView(_ v: WKWebView, didFinish n: WKNavigation!) { done = true }
  func webView(_ v: WKWebView, didFail n: WKNavigation!, withError e: Error) { done = true }
  func webView(_ v: WKWebView, didFailProvisionalNavigation n: WKNavigation!, withError e: Error) { done = true }
}
let nav = Nav(); view.navigationDelegate = nav
func pump(_ s: Double) { let t = Date(); while Date().timeIntervalSince(t) < s { RunLoop.main.run(mode: .default, before: Date(timeIntervalSinceNow: 0.04)) } }
view.load(URLRequest(url: url))
let t0 = Date(); while !nav.done && Date().timeIntervalSince(t0) < 25 { pump(0.1) }
pump(2.5)

// Optional: Recorder vor dem Scrollen installieren (Umgebungsvariable PREJS)
if let pre = ProcessInfo.processInfo.environment["PREJS"], !pre.isEmpty {
  view.evaluateJavaScript(pre, completionHandler: nil)
  pump(1.0)
}

// Gesamthoehe holen
var total = h * 3
var got = false
view.evaluateJavaScript("document.documentElement.scrollHeight") { r, _ in
  if let n = r as? Double { total = n } else if let n = r as? Int { total = Double(n) }
  got = true
}
let t1 = Date(); while !got && Date().timeIntervalSince(t1) < 8 { pump(0.05) }

// in Schritten nach unten scrollen, damit alle scrollgetriebenen Effekte ausloesen
let maxY = max(0, total - h)
for i in 0...steps {
  let y = maxY * Double(i) / Double(steps)
  view.evaluateJavaScript("window.scrollTo({top: \(y), behavior:'instant'});", completionHandler: nil)
  pump(pause)
}
pump(0.6)

var out = "kein Ergebnis"
var fin = false
view.evaluateJavaScript(js) { r, e in
  if let e = e { out = "JS-FEHLER: \(e.localizedDescription)" } else if let r = r { out = "\(r)" }
  fin = true
}
let t2 = Date(); while !fin && Date().timeIntervalSince(t2) < 20 { pump(0.05) }
print(out)
