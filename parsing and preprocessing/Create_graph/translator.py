from google_trans_new import google_translator

from connect import db

translator = google_translator()
cities = ['Kaliningrad', 'SaintPetersburg', 'Berlin']


def translate():
    for city in cities:
        poi = list(db.poi.find({'city': city}))
        for data in poi:
            text = data['description']
            if text is not None:
                result = translator.translate(text, lang_tgt='ru')
                db.poi.update({'_id': data['_id']}, {'$set': {'description': result}})

            name = data.get('name')
            if name is not None and (len(name) > 0):
                result = translator.translate(name, lang_tgt='ru')
                db.poi.update({'_id': data['_id']}, {'$set': {'name': result}})
