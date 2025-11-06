import sqlite3


class MetadataDatabase:
    def __init__(self, db_path):
        self.cursor = None
        self.conn = None
        self.db_path = db_path


    def connect(self):
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()


    def close(self):
        if hasattr(self, 'conn'):
            self.conn.close()


    # Получение картинки и данных из БД
    def fetch_images_and_names(self):
        query = '''
        SELECT metadata_table.id, metadata_table.NameFile, image_table.Image
        FROM metadata_table
        JOIN image_table ON metadata_table.id = image_table.id
        '''
        self.cursor.execute(query)
        rows = self.cursor.fetchall()
        result = {}
        for id_, name, image_data in rows:
            result[id_] = [name, image_data]  # в значении список: [название, фото (байты)]

        return result


    # Удаление данных из БД
    # также очищает порядок инкрементации, чтобы корректно добавлять новые записи
    def delete_row(self, row_id):
        try:
            delete_meta = "DELETE FROM metadata_table WHERE id = ?"
            delete_photo = "DELETE FROM image_table WHERE id = ?"
            self.cursor.execute(delete_meta, (row_id,))
            self.cursor.execute(delete_photo, (row_id,))
            update_meta = "UPDATE sqlite_sequence SET seq = 0 WHERE name = 'metadata_table'"
            update_image = "UPDATE sqlite_sequence SET seq = 0 WHERE name = 'image_table'"
            self.cursor.execute(update_meta)
            self.cursor.execute(update_image)
            self.conn.commit()

            print(f"Deleted row with ID {row_id} from database")
        except Exception as e:
            print(f"Error deleting row with ID {row_id}: {e}")


    # Загрузка метаданных в metadata_table
    def insert_metadata(self, data):
        columns = (
            "NameFile, Make, Model, Software, DateTime, HostComputer, Mode, Flash, "
            "ColorSpace, ExifImageWidth, ExifImageHeight, OffsetTime, Latitude, Longitude"
        )
        placeholders = ', '.join('?' for _ in columns.split(', '))
        sql = f"INSERT INTO metadata_table ({columns}) VALUES ({placeholders})"

        try:
            int_fields = ['Flash', 'ColorSpace', 'ExifImageWidth', 'ExifImageHeight']
            real_fields = ['Latitude', 'Longitude']

            params = []
            for col in columns.split(', '):
                val = data.get(col)
                if col in int_fields:
                    val = int(val) if val is not None else None
                elif col in real_fields:
                    val = float(val) if val is not None else None
                params.append(val)

            self.cursor.execute(sql, tuple(params))
            self.conn.commit()
        except Exception as e:
            print(f"Error with insert metadata: {e}")


    # Загрузка изображения в image_table.image
    def insert_image(self, image_path):
        try:
            with open(image_path, 'rb') as file:
                img_blob = file.read()

            sql = "INSERT INTO image_table (image) VALUES (?)"
            self.cursor.execute(sql, (img_blob,))
            self.conn.commit()
            print("Изображение успешно добавлено в базу.")
        except Exception as e:
            print(f"Error with insert image: {e}")
