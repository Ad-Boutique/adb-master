import WebKit
import AppKit
// JavaScript gegen eine geladene Seite auswerten: probe <url> <breite> <hoehe> <js-datei> [wartezeit]
let a = CommandLine.arguments
let url = URL(string: a[1])!
let w = Double(a[2]) ?? 1440, h = Double(a[3]) ?? 900
let js = try! String(contentsOfFile: a[4], encoding: .utf8)
let wait = Double(a.count > 5 ? a[5] : "2.2") ?? 2.2
let app = NSApplication.shared; app.setActivationPolicy(.prohibited)
let view = WKWebView(frame: NSRect(x: 0, y: 0, width: w, height: h))
let win = NSWindow(contentRect: NSRect(x: 0, y: 0, width: w, height: h), styleMask: [.borderless], backing: .buffered, defer: false)
win.contentView = view; win.orderBack(nil)
final class Nav: NSObject, WKNavigationDelegate { var done = false
  func webView(_ v: WKWebView, didFinish n: WKNavigation!) { done = true }
  func webView(_ v: WKWebView, didFail n: WKNavigation!, withError e: Error) { done = true } }
let nav = Nav(); view.navigationDelegate = nav
view.load(URLRequest(url: url))
func pump(_ s: Double) { let t = Date(); while Date().timeIntervalSince(t) < s { RunLoop.main.run(mode: .default, before: Date(timeIntervalSinceNow: 0.05)) } }
let t0 = Date(); while !nav.done && Date().timeIntervalSince(t0) < 25 { pump(0.1) }
pump(wait)
var fin = false
view.evaluateJavaScript(js) { r, e in
  if let e = e { print("JSERR: \(e.localizedDescription)") } else if let r = r { print("\(r)") } else { print("null") }
  fin = true }
let t1 = Date(); while !fin && Date().timeIntervalSince(t1) < 20 { pump(0.1) }
