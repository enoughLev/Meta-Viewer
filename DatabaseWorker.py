import sqlite3

class MetadataDatabase:
    def __init__(self, db_path):
        self.db_path = db_path

    def connect(self):
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()

    def close(self):
        if hasattr(self, 'conn'):
            self.conn.close()

    import sqlite3

    def insert_metadata(self, data):
        """
        Вставляет данные в таблицу с указанными полями.
        При ошибках выводит подробное сообщение.
        """
        columns = (
            "NameFile, Make, Model, Software, DateTime, HostComputer, Mode, Flash, "
            "ColorSpace, ExifImageWidth, ExifImageHeight, OffsetTime, Latitude, Longitude"
        )

        placeholders = ', '.join('?' for _ in columns.split(', '))

        sql = f"INSERT OR REPLACE INTO metadata_table ({columns}) VALUES ({placeholders})"

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
        except sqlite3.IntegrityError as e:
            print(f"Ошибка целостности данных: {e}")
        except sqlite3.OperationalError as e:
            print(f"Операционная ошибка SQLite: {e}")
        except sqlite3.DatabaseError as e:
            print(f"Ошибка базы данных SQLite: {e}")
        except Exception as e:
            print(f"Неизвестная ошибка при вставке данных: {e}")

    def insert_image(self, image_path):
        """
        Вставляет фотографию из файла image_path в таблицу image_table в поле image.
        id задается автоматически.
        """
        try:
            with open(image_path, 'rb') as file:
                img_blob = file.read()

            sql = "INSERT INTO image_table (image) VALUES (?)"
            self.cursor.execute(sql, (img_blob,))
            self.conn.commit()
            print("Изображение успешно добавлено в базу.")
        except sqlite3.IntegrityError as e:
            print(f"Ошибка целостности данных: {e}")
        except sqlite3.OperationalError as e:
            print(f"Операционная ошибка SQLite: {e}")
        except sqlite3.DatabaseError as e:
            print(f"Ошибка базы данных SQLite: {e}")
        except Exception as e:
            print(f"Неизвестная ошибка при вставке изображения: {e}")

    def fetch_metadata_by_id(self, record_id):
        sql = "SELECT * FROM metadata_table WHERE id=?"
        self.cursor.execute(sql, (record_id,))
        row = self.cursor.fetchone()
        if row:
            columns = [description[0] for description in self.cursor.description]
            return dict(zip(columns, row))
        else:
            return None
