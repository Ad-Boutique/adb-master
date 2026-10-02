import WebKit
import AppKit
// Wie probe, aber das JS laeuft als Rumpf einer async-Funktion (await erlaubt, Ergebnis per return).
// aprobe <url> <breite> <hoehe> <js-datei> [wartezeit-sek] [timeout-sek]
// Gedacht fuer Pruefungen ueber mehrere Scrollpositionen (z. B. _tools/brandaudit.js).
let a = CommandLine.arguments
let url = URL(string: a[1])!
let w = Double(a[2]) ?? 1440, h = Double(a[3]) ?? 900
let js = try! String(contentsOfFile: a[4], encoding: .utf8)
let wait = Double(a.count > 5 ? a[5] : "2.5") ?? 2.5
let tmax = Double(a.count > 6 ? a[6] : "150") ?? 150
let app = NSApplication.shared; app.setActivationPolicy(.prohibited)
let cfgW = WKWebViewConfiguration()
cfgW.websiteDataStore = WKWebsiteDataStore.nonPersistent()
// JS-Fehler ab dem ersten Byte sammeln: window.__errs
let errJS = "window.__errs=[];addEventListener('error',function(e){__errs.push(String(e.message)+' @'+(e.filename||'').split('/').pop()+':'+e.lineno)});addEventListener('unhandledrejection',function(e){__errs.push('promise: '+String(e.reason))});"
cfgW.userContentController.addUserScript(WKUserScript(source: errJS, injectionTime: .atDocumentStart, forMainFrameOnly: true))
let view = WKWebView(frame: NSRect(x: 0, y: 0, width: w, height: h), configuration: cfgW)
let win = NSWindow(contentRect: NSRect(x: 0, y: 0, width: w, height: h), styleMask: [.borderless], backing: .buffered, defer: false)
win.contentView = view; win.orderBack(nil)
final class Nav: NSObject, WKNavigationDelegate { var done = false
  func webView(_ v: WKWebView, didFinish n: WKNavigation!) { done = true }
  func webView(_ v: WKWebView, didFail n: WKNavigation!, withError e: Error) { done = true } }
let nav = Nav(); view.navigationDelegate = nav
view.load(URLRequest(url: url, cachePolicy: .reloadIgnoringLocalAndRemoteCacheData))
func pump(_ s: Double) { let t = Date(); while Date().timeIntervalSince(t) < s { RunLoop.main.run(mode: .default, before: Date(timeIntervalSinceNow: 0.03)) } }
let t0 = Date(); while !nav.done && Date().timeIntervalSince(t0) < 25 { pump(0.1) }
pump(wait)
var fin = false
view.callAsyncJavaScript(js, arguments: [:], in: nil, in: .page) { r in
  switch r {
  case .success(let v): print("\(v)")
  case .failure(let e): print("JSERR: \(e)")
  }
  fin = true }
let t1 = Date(); while !fin && Date().timeIntervalSince(t1) < tmax { pump(0.05) }
if !fin { print("TIMEOUT") }
