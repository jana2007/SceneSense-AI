
import sqlite3
import json
from datetime import datetime


class AnalysisHistory:

    def __init__(self):
        self.connection = sqlite3.connect(
            "scenesense_history.db",
            check_same_thread=False
        )

        self.create_table()

    def create_table(self):

        cursor = self.connection.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                filename TEXT,
                detected_objects TEXT,
                scene_description TEXT,
                extracted_text TEXT,
                analysis_time TEXT
            )
        """)

        self.connection.commit()

    def save_analysis(
        self,
        filename,
        detected_objects,
        scene_description,
        extracted_text
    ):

        cursor = self.connection.cursor()

        cursor.execute("""
            INSERT INTO history (
                filename,
                detected_objects,
                scene_description,
                extracted_text,
                analysis_time
            )
            VALUES (?, ?, ?, ?, ?)
        """, (
            filename,
            json.dumps(detected_objects),
            scene_description,
            json.dumps(extracted_text),
            datetime.now().strftime("%d-%m-%Y %I:%M:%S %p")
        ))

        self.connection.commit()

    def get_history(self):

        cursor = self.connection.cursor()

        cursor.execute("""
            SELECT * FROM history
            ORDER BY id DESC
        """)

        records = cursor.fetchall()

        history = []

        for record in records:

            history.append({
                "id": record[0],
                "filename": record[1],
                "detected_objects": json.loads(record[2]),
                "scene_description": record[3],
                "extracted_text": json.loads(record[4]),
                "analysis_time": record[5]
            })

        return history

    def get_analytics(self):

        records = self.get_history()

        total_images = len(records)

        total_objects = 0

        object_counts = {}

        for record in records:

            objects = record["detected_objects"]

            total_objects += len(objects)

            for obj in objects:

                name = obj["name"].title()

                object_counts[name] = (
                    object_counts.get(name, 0) + 1
                )

        unique_objects = len(object_counts)

        most_common = sorted(
            object_counts.items(),
            key=lambda item: item[1],
            reverse=True
        )

        return {
            "total_images": total_images,
            "total_objects": total_objects,
            "unique_objects": unique_objects,
            "object_counts": object_counts,
            "most_common": most_common
        }

    def close(self):
        self.connection.close()
