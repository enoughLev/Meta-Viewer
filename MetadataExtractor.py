import os

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

    def display_metadata(self):
        # Начинаем формировать текст для отображения
        text_output = f"Image Mode: {self.image.mode}\n\nAll EXIF metadata:\n"
        for key, val in self.exif_data.items():
            if key != "GPSInfo":
                text_output += f"{key}: {val}\n"

        gps_info = self.get_gps_info()
        if gps_info:
            text_output += "\nGPS Metadata:\n"
            for key, val in gps_info.items():
                text_output += f"{key}: {val}\n"
            lat, lon = self.get_coordinates()
            text_output += f"\nDecoded GPS Coordinates:\nLatitude: {lat}\nLongitude: {lon}\n"
        else:
            text_output += "\nNo GPS metadata found.\n"

        return text_output

    def get_metadata_dict(self):
        filename = os.path.basename(self.image_path)  # Получаем только имя файла с расширением

        metadata = {
            "NameFile": filename,
            "Make": self.exif_data.get("Make"),
            "Model": self.exif_data.get("Model"),
            "Software": self.exif_data.get("Software"),
            "DateTime": self.exif_data.get("DateTime"),
            "HostComputer": self.exif_data.get("HostComputer"),
            "Mode": self.image.mode,
            "Flash": self.exif_data.get("Flash"),
            "ColorSpace": self.exif_data.get("ColorSpace"),
            "ExifImageWidth": self.exif_data.get("ExifImageWidth"),
            "ExifImageHeight": self.exif_data.get("ExifImageHeight"),
            "OffsetTime": self.exif_data.get("OffsetTime"),
        }

        gps_info = self.get_gps_info()
        if gps_info:
            latitude, longitude = self.get_coordinates()
            metadata["Latitude"] = latitude
            metadata["Longitude"] = longitude
        else:
            metadata["Latitude"] = None
            metadata["Longitude"] = None

        return metadata


# Пример использования:
if __name__ == "__main__":
    extractor = ImageMetadataExtractor("path_to_your_image.jpg")
    extractor.print_all_metadata()
