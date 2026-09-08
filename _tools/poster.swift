import AVFoundation
import AppKit
// Posterbild aus einem Video ziehen und Masse ausgeben: poster <video> <out.jpg> [sekunde]
let a = CommandLine.arguments
let url = URL(fileURLWithPath: a[1]); let out = a[2]
let sec = a.count > 3 ? Double(a[3]) ?? 0.5 : 0.5
let asset = AVURLAsset(url: url)
let gen = AVAssetImageGenerator(asset: asset)
gen.appliesPreferredTrackTransform = true
gen.requestedTimeToleranceBefore = .zero; gen.requestedTimeToleranceAfter = CMTime(seconds: 0.5, preferredTimescale: 600)
var actual = CMTime.zero
let cg = try gen.copyCGImage(at: CMTime(seconds: sec, preferredTimescale: 600), actualTime: &actual)
let rep = NSBitmapImageRep(cgImage: cg)
let data = rep.representation(using: .jpeg, properties: [.compressionFactor: 0.78])!
try data.write(to: URL(fileURLWithPath: out))
print("poster \(out) \(cg.width)x\(cg.height)")
