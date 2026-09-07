import WebKit
import AppKit
// Screenshots an Scrollpositionen: scrollshot <url> <prefix> <breite> <hoehe> <y1> [y2 ...]
let a = CommandLine.arguments
let url = URL(string: a[1])!; let prefix = a[2]
let W = Double(a[3]) ?? 1400, H = Double(a[4]) ?? 880
let ys = a.dropFirst(5).compactMap { Double($0) }
let app = NSApplication.shared; app.setActivationPolicy(.prohibited)
let web = WKWebView(frame: NSRect(x: 0, y: 0, width: W, height: H))
let win = NSWindow(contentRect: NSRect(x: 0, y: 0, width: W, height: H), styleMask: [.borderless], backing: .buffered, defer: false)
win.contentView = web; win.orderBack(nil)
final class D: NSObject, WKNavigationDelegate { var done = false
  func webView(_ v: WKWebView, didFinish n: WKNavigation!) { done = true }
  func webView(_ v: WKWebView, didFail n: WKNavigation!, withError e: Error) { done = true } }
let d = D(); web.navigationDelegate = d
func pump(_ s: Double) { let t = Date(); while Date().timeIntervalSince(t) < s { RunLoop.main.run(mode: .default, before: Date(timeIntervalSinceNow: 0.05)) } }
web.load(URLRequest(url: url))
let t0 = Date(); while !d.done && Date().timeIntervalSince(t0) < 20 { pump(0.1) }
pump(4)
// Optional: JS vor den Screenshots ausfuehren (z. B. Cookie-Banner schliessen), via Umgebungsvariable PREJS
if let pre = ProcessInfo.processInfo.environment["PREJS"], !pre.isEmpty {
  web.evaluateJavaScript(pre, completionHandler: nil)
  pump(2)
}
for (i, y) in ys.enumerated() {
  web.evaluateJavaScript("window.scrollTo({top: \(y), behavior:'instant'});", completionHandler: nil)
  pump(2.5)
  let cfg = WKSnapshotConfiguration(); cfg.rect = CGRect(x: 0, y: 0, width: W, height: H); cfg.snapshotWidth = NSNumber(value: Double(W))
  var fin = false
  web.takeSnapshot(with: cfg) { img, _ in
    if let img = img, let tf = img.tiffRepresentation, let rep = NSBitmapImageRep(data: tf),
       let dt = rep.representation(using: .jpeg, properties: [.compressionFactor: 0.72]) {
      try? dt.write(to: URL(fileURLWithPath: "\(prefix)_\(i).jpg")); print("ok \(prefix)_\(i).jpg @\(Int(y))") }
    fin = true }
  let t = Date(); while !fin && Date().timeIntervalSince(t) < 10 { pump(0.1) }
}
