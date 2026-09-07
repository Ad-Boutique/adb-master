import AVFoundation
import CoreMedia
import CoreImage
import AppKit
// Video-Encoder fuer die Seite: enc <in> <out> <zielbreite> <kbit> <ton:0|1>
let a = CommandLine.arguments
let inURL = URL(fileURLWithPath: a[1]); let outURL = URL(fileURLWithPath: a[2])
let targetW = Int(a[3]) ?? 720; let kbit = Int(a[4]) ?? 1200
let withAudio = (a.count > 5 ? a[5] : "0") == "1"
let asset = AVAsset(url: inURL)
guard let vTrack = asset.tracks(withMediaType: .video).first else { print("kein Videotrack"); exit(1) }
let natural = vTrack.naturalSize.applying(vTrack.preferredTransform)
let srcW = abs(natural.width), srcH = abs(natural.height)
var outW = targetW, outH = Int((Double(targetW) * srcH / srcW).rounded())
if outW % 2 != 0 { outW += 1 }; if outH % 2 != 0 { outH += 1 }
try? FileManager.default.removeItem(at: outURL)
let writer = try AVAssetWriter(outputURL: outURL, fileType: .mp4)
let vIn = AVAssetWriterInput(mediaType: .video, outputSettings: [
  AVVideoCodecKey: AVVideoCodecType.h264, AVVideoWidthKey: outW, AVVideoHeightKey: outH,
  AVVideoCompressionPropertiesKey: [AVVideoAverageBitRateKey: kbit * 1000, AVVideoMaxKeyFrameIntervalKey: 60,
    AVVideoProfileLevelKey: AVVideoProfileLevelH264HighAutoLevel, AVVideoAllowFrameReorderingKey: true]])
vIn.expectsMediaDataInRealTime = false; writer.add(vIn)
var aIn: AVAssetWriterInput?; let aTrack = asset.tracks(withMediaType: .audio).first
if withAudio, aTrack != nil {
  let x = AVAssetWriterInput(mediaType: .audio, outputSettings: [AVFormatIDKey: kAudioFormatMPEG4AAC, AVNumberOfChannelsKey: 2, AVSampleRateKey: 44100, AVEncoderBitRateKey: 96000])
  x.expectsMediaDataInRealTime = false; writer.add(x); aIn = x }
let reader = try AVAssetReader(asset: asset)
let vOut = AVAssetReaderTrackOutput(track: vTrack, outputSettings: [kCVPixelBufferPixelFormatTypeKey as String: kCVPixelFormatType_32BGRA]); reader.add(vOut)
var aOut: AVAssetReaderTrackOutput?
if withAudio, let t = aTrack { let x = AVAssetReaderTrackOutput(track: t, outputSettings: [AVFormatIDKey: kAudioFormatLinearPCM]); reader.add(x); aOut = x }
let adaptor = AVAssetWriterInputPixelBufferAdaptor(assetWriterInput: vIn, sourcePixelBufferAttributes: [
  kCVPixelBufferPixelFormatTypeKey as String: kCVPixelFormatType_32BGRA, kCVPixelBufferWidthKey as String: outW, kCVPixelBufferHeightKey as String: outH])
reader.startReading(); writer.startWriting(); writer.startSession(atSourceTime: .zero)
let ciCtx = CIContext(options: [.useSoftwareRenderer: false]); let group = DispatchGroup(); var frames = 0
group.enter()
vIn.requestMediaDataWhenReady(on: DispatchQueue(label: "v")) {
  while vIn.isReadyForMoreMediaData {
    guard let sb = vOut.copyNextSampleBuffer(), let src = CMSampleBufferGetImageBuffer(sb) else { vIn.markAsFinished(); group.leave(); return }
    let pts = CMSampleBufferGetPresentationTimeStamp(sb); var dst: CVPixelBuffer?
    CVPixelBufferPoolCreatePixelBuffer(nil, adaptor.pixelBufferPool!, &dst)
    if let dst = dst {
      var img = CIImage(cvPixelBuffer: src).transformed(by: vTrack.preferredTransform)
      let e = img.extent; img = img.transformed(by: CGAffineTransform(translationX: -e.origin.x, y: -e.origin.y))
      img = img.transformed(by: CGAffineTransform(scaleX: CGFloat(Double(outW) / Double(e.width)), y: CGFloat(Double(outH) / Double(e.height))))
      ciCtx.render(img, to: dst); adaptor.append(dst, withPresentationTime: pts); frames += 1 } } }
if let aIn = aIn, let aOut = aOut { group.enter()
  aIn.requestMediaDataWhenReady(on: DispatchQueue(label: "a")) {
    while aIn.isReadyForMoreMediaData { guard let sb = aOut.copyNextSampleBuffer() else { aIn.markAsFinished(); group.leave(); return }; aIn.append(sb) } } }
group.notify(queue: .main) { writer.finishWriting {
  let mb = (try? FileManager.default.attributesOfItem(atPath: outURL.path)[.size] as? Int) ?? 0
  print("ok \(outURL.lastPathComponent) \(outW)x\(outH) frames=\(frames) \((mb ?? 0)/1024/1024)MB status=\(writer.status.rawValue)"); exit(writer.status == .completed ? 0 : 2) } }
RunLoop.main.run()
