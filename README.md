##Smart Home API 
Overview
This project implements a REST API using Django Rest Framework (DRF) for managing temperature sensors in a smart home environment. The system supports basic CRUD operations (Create, Read, Update, Delete) for sensors and their temperature measurements.

Key Features
Sensor Management: Create, update, and retrieve sensors.
Temperature Measurement: Add temperature measurements associated with sensors.
Detailed Sensor View: Retrieve a sensor along with its temperature measurements.
Optional Image Attachment: Sensors can optionally attach images to temperature measurements.
Models
The project includes two main models:

Sensor:

name: The name of the sensor (e.g., "ESP32").
description: An optional description of where the sensor is located (e.g., "Living room" or "Kitchen").
Measurement:

sensor_id: Foreign key linking the measurement to a specific sensor.
temperature: The temperature recorded by the sensor, in degrees Celsius.
created_at: The timestamp when the measurement was taken.
image: (Optional) An image associated with the measurement, if available.
API Endpoints
Sensor Endpoints
Create Sensor: POST /sensors/

Request Body: { "name": "ESP32", "description": "Kitchen sensor" }
Update Sensor: PATCH /sensors/{id}/

Request Body: { "name": "ESP32", "description": "Updated description" }
List Sensors: GET /sensors/

Response: A list of sensors with their ID, name, and description.
Retrieve Sensor: GET /sensors/{id}/

Response: Detailed information about the sensor including all associated measurements.
Measurement Endpoints
Add Measurement: POST /measurements/
Request Body: { "sensor_id": 1, "temperature": 22.5 }
Optional: Include an image with the measurement.
Installation and Setup
Prerequisites
Python 3.x
PostgreSQL database
Steps
Clone the repository:

bash
Copy code
git clone <repository_url>
cd smart-home-api
Install dependencies:

bash
Copy code
pip install -r requirements.txt
Set up the PostgreSQL database:

Create a database for the project.
Configure the database settings in settings.py.
Apply database migrations:

bash
Copy code
python manage.py migrate
Run the development server:

bash
Copy code
python manage.py runserver
Testing the API:

Use the provided requests.http file for examples of how to interact with the API using HTTP requests.
Additional Features
Image Attachment for Measurements
Sensors now support attaching images to their temperature measurements. To enable this feature:

Ensure that the Measurement model includes an ImageField:
python
Copy code
image = models.ImageField(null=True, blank=True)
Use the appropriate endpoint to upload images along with temperature data.
Tips and Tricks
Auto Timestamps: Use auto_now_add=True for the created_at field in Measurement to automatically set the timestamp when a measurement is created.
Nested Serializers: To display measurements in the sensor detail view, use nested serializers in DRF.
Conclusion
This project demonstrates how to create a simple yet effective REST API for managing IoT devices like temperature sensors in a smart home. The flexible design allows for easy expansion, such as adding new types of sensors or additional features like image attachments.



# Умный дом

## Техническая задача: реализовать некоторые действия из CRUD, используя Django Rest Framework.

**CRUD** — аббревиатура для Create-Read-Update-Delete. Ей обозначают логику для операций создания-чтения-обновления-удаления сущностей. Подробнее: https://ru.wikipedia.org/wiki/CRUD.

## Описание

У нас есть программируемые датчики, измеряющие температуру. Раз в некоторый интервал времени датчики делают запрос по API и записывают свои показания. В показания датчики передают свой ID и текущую температуру в градусах Цельсия.

Необходимо реализовать REST API для добавления и изменения датчиков, их просмотра и добавления новых измерений температуры.

Требуется задать две модели — они уже описаны в models.py:

- датчик:

  - название,
  - описание (необязательное, например, «спальня» или «корридор на 2 этаже»).

- измерение температуры:

  - ID датчика,
  - температура при измерении,
  - дата и время измерения.

Для сериализаторов используйте `ModelSerializer`.

---

Запросы, которые должны быть реализованы в системе:

1. Создать датчик. Указываются название и описание датчика.
2. Изменить датчик. Указываются название и описание.
3. Добавить измерение. Указываются ID датчика и температура.
4. Получить список датчиков. Выдаётся список с краткой информацией по датчикам: ID, название и описание.

```json
[
  {
    "id": 2,
    "name": "ESP32",
    "description": "Датчик на кухне за холодильником"
  },
  {
    "id": 1,
    "name": "ESP32",
    "description": "Перенес датчик на балкон"
  }
]
```

5. Получить информацию по конкретному датчику. Выдаётся полная информация по датчику: ID, название, описание и список всех измерений с температурой и временем.

```json
{
  "id": 1,
  "name": "ESP32",
  "description": "Перенес датчик на балкон",
  "measurements": [
    {
      "temperature": 22.3,
      "created_at": "2021-10-23T16:44:51.432328Z"
    },
    {
      "temperature": 22.5,
      "created_at": "2021-10-23T16:45:51.091212Z"
    }
  ]
}
```

Примеры запросов можно посмотреть в файле [requests.http](./requests.http).

## Подсказки

1. Вам необходимо будет изменить файлы `models.py`, `serializers.py`, `views.py` и `urls.py`. В места, где нужно добавлять код, включены `TODO`-комментарии. После того, как вы добавите код, комментарии можно удалить.

2. Для автоматического проставления времени используйте аргументы: `auto_now` (при обновлении) и `auto_now_add` (при создании). Подробнее: https://docs.djangoproject.com/en/3.1/ref/models/fields/#django.db.models.DateField.

3. Для сериализатора с подробной информацией по датчику для отображения списка измерений необходимо использовать [вложенный сериализатор](https://www.django-rest-framework.org/api-guide/serializers/#dealing-with-nested-objects). Должен получиться примерно такой код:

```python
class MeasurementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Measurement
        fields = ['temperature', 'created_at']


class SensorDetailSerializer(serializers.ModelSerializer):
    measurements = MeasurementSerializer(read_only=True, many=True)

    class Meta:
        model = Sensor
        fields = ['id', 'name', 'description', 'measurements']
```

## Дополнительные задания

### Прикрепление картинки к измерению

Датчики стали более продвинутыми и могут также прикреплять снимки. Добавьте nullable-поле к модели `Measurement` для сохранения изображений. https://www.django-rest-framework.org/api-guide/fields/#imagefield

Обратите внимание, что поле должно быть опциональным — некоторые датчики прикладывают фото, а некоторые — нет. Для старых датчиков ничего не должно сломаться.

## Документация по проекту

Для запуска проекта необходимо

Установить зависимости:

```bash
pip install -r requirements.txt
```

Вам необходимо будет создать базу в postgres и прогнать миграции:

```base
python manage.py migrate
```

Выполнить команду:

```bash
python manage.py runserver
```
