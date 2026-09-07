import AVFoundation
import AppKit
// Standbilder aus einem Video: dense <video> <ausgabeordner> <prefix> <schritt-sekunden>
let args = CommandLine.arguments
let asset = AVAsset(url: URL(fileURLWithPath: args[1])); let outDir = args[2]; let prefix = args[3]; let step = Double(args[4]) ?? 0.4
let dur = CMTimeGetSeconds(asset.duration); let gen = AVAssetImageGenerator(asset: asset)
gen.appliesPreferredTrackTransform = true; gen.maximumSize = CGSize(width: 1100, height: 1100)
gen.requestedTimeToleranceBefore = .zero; gen.requestedTimeToleranceAfter = CMTime(seconds: 0.1, preferredTimescale: 600)
var i = 0; var t = 0.0
while t < dur {
  if let cg = try? gen.copyCGImage(at: CMTime(seconds: t, preferredTimescale: 600), actualTime: nil) {
    let rep = NSBitmapImageRep(cgImage: cg)
    if let d = rep.representation(using: .jpeg, properties: [.compressionFactor: 0.6]) {
      try? d.write(to: URL(fileURLWithPath: String(format: "%@/%@_%04d.jpg", outDir, prefix, i))) } }
  i += 1; t += step }
print("done \(prefix) dur=\(dur)s frames=\(i)")
