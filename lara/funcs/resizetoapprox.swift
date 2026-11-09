import UIKit

extension UIImage {
    func resizeToApprox(allowedSizeInBytes: Int) throws -> Data {
        if let data = self.jpegData(compressionQuality: 0.99), data.count <= allowedSizeInBytes {
            return data
        }

        var left: CGFloat = 0.0
        var right: CGFloat = 1.0
        var mid = (left + right) / 2.0

        var closestImage: Data?
        guard var newResImage = self.jpegData(compressionQuality: 1) else {
            throw NSError(domain: "IconThemer", code: 1, userInfo: [NSLocalizedDescriptionKey: "无法压缩图片"])
        }

        for _ in 0...13 {
            if newResImage.count < allowedSizeInBytes {
                left = mid
                closestImage = newResImage
            } else if newResImage.count > allowedSizeInBytes {
                right = mid
            } else {
                return newResImage
            }

            mid = (left + right) / 2.0
            guard let newData = self.jpegData(compressionQuality: mid) else {
                throw NSError(domain: "IconThemer", code: 1, userInfo: [NSLocalizedDescriptionKey: "无法压缩图片"])
            }
            newResImage = newData
        }

        if let closestImage {
            return closestImage
        }

        throw NSError(domain: "IconThemer", code: 1, userInfo: [NSLocalizedDescriptionKey: "无法把图片压缩到原始大小限制以内"])
    }
}
