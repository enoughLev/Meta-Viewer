from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS

class ImageMetadataExtractor:
    def __init__(self, image_path):
        self.image_path = image_path
        self.image = Image.open(image_path)
        self.exif_data = self.get_exif_data()

    def get_exif_data(self):
        exif_data = {}
        info = self.image._getexif()
        if info:
            for tag, value in info.items():
                decoded = TAGS.get(tag, tag)
                exif_data[decoded] = value
        return exif_data

    def get_gps_info(self):
        gps_info = {}
        if "GPSInfo" in self.exif_data:
            for key in self.exif_data["GPSInfo"].keys():
                decode = GPSTAGS.get(key, key)
                gps_info[decode] = self.exif_data["GPSInfo"][key]
        return gps_info

    def convert_to_degrees(self, value):
        d = value[0].numerator / value[0].denominator
        m = value[1].numerator / value[1].denominator
        s = value[2].numerator / value[2].denominator
        degrees = d + (m / 60.0) + (s / 3600.0)
        return degrees

    def get_coordinates(self):
        gps_info = self.get_gps_info()
        lat = None
        lon = None
        if "GPSLatitude" in gps_info and "GPSLatitudeRef" in gps_info:
            lat = self.convert_to_degrees(gps_info["GPSLatitude"])
            if gps_info["GPSLatitudeRef"] != "N":
                lat = -lat
        if "GPSLongitude" in gps_info and "GPSLongitudeRef" in gps_info:
            lon = self.convert_to_degrees(gps_info["GPSLongitude"])
            if gps_info["GPSLongitudeRef"] != "E":
                lon = -lon
        return lat, lon

    def print_all_metadata(self):
        print("All EXIF metadata:")
        print(f"Mode: {self.image.mode}")
        for key, val in self.exif_data.items():
            if key != "GPSInfo":
                print(f"{key}: {val}")

        gps_info = self.get_gps_info()
        if gps_info:
            print("\nGPS Metadata:")
            for key, val in gps_info.items():
                print(f"{key}: {val}")
            lat, lon = self.get_coordinates()
            print(f"\nDecoded GPS Coordinates:\nLatitude: {lat}\nLongitude: {lon}")
        else:
            print("\nNo GPS metadata found.")

# Пример использования:
if __name__ == "__main__":
    extractor = ImageMetadataExtractor("path_to_your_image.jpg")
    extractor.print_all_metadata()
