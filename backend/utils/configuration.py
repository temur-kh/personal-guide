SITE_NAME = 'site'
DATABASE_NAME = 'database_name'
USERNAME = 'username'
PASSWORD = 'password'

# Константы для service.py
TRIP_TYPES_MAPPING = 'route_types_mapping'
HISTORIC_TRIP = 'historic'
ARCHITECTURE_TRIP = 'architecture'
ENTERTAINMENT_TRIP = 'entertainment'
CUSTOM_TRIP = 'custom'
HISTORIC_TAG = 'historic'
RELIGION_TAG = 'religion'
ARCHITECTURE_TAG = 'architecture'
TOURISM_TAG = 'tourism'
ENTERTAINMENT_TAG = 'entertainment'


osm_data_processor = {
    SITE_NAME: 'mongodb',
    DATABASE_NAME: 'database',
    USERNAME: 'user',
    PASSWORD: 'personalguide2020'
}


service = {
    TRIP_TYPES_MAPPING: {
        HISTORIC_TRIP: [
            HISTORIC_TAG, RELIGION_TAG,
        ],
        ARCHITECTURE_TRIP: [
            ARCHITECTURE_TAG, TOURISM_TAG, RELIGION_TAG,
        ],
        ENTERTAINMENT_TRIP: [
            ENTERTAINMENT_TAG,
        ],
        CUSTOM_TRIP: [
            HISTORIC_TAG, RELIGION_TAG, ARCHITECTURE_TAG, TOURISM_TAG, ENTERTAINMENT_TAG,
        ]
    }
}

# Категории:
# Entertaiment, religion, tourism, architecture, historic
#
# Historic:  historic, religion
# Architecture: architecture, tourism, religion
# Entretaiment: entertaiment,
# Custom:
