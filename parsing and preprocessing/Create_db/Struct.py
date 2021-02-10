# Collection: nodes

element = {'_id': {},
           'location': {'coordinates': [float, float],  # lon lat
                        'type': 'Point'},
           'name': str,
           'old_name': str,
           'road': bool,
           'important': bool,
           'city': str,
           'entrance': str,  # id way/relation для которого он является входом или True - если это вход в здание
           'save': bool,
           'crossroads': bool,
           'tags': [],
           'global_tags': [],

           'id_place': str,
           'rate': int,
           'kinds': [],
           'description': str,

           'cuisine': [],  # тип кухни
           'dietary_restrictions': [],  # диетические ограничения
           'hours': [(int, int), (int, int), (int, int), (int, int), (int, int), (int, int), (int, int)],
           # часы работы по дням недели
           'photo': {'small': {'width', 'url', 'height'},
                     'thumbnail': {'width', 'url', 'height'},
                     'original': {'width', 'url', 'height'},
                     'large': {'width', 'url', 'height'},
                     'medium': {'width', 'url', 'height'}},
           'awards': ['award_types'],
           'rating': float,  # округленный рейтинг
           'raw_ranking': float,  # не округленный рейтинг
           'ranking_position': float,  # позиция в рейтинге
           'num_reviews': int,  # кол-во отзывовэ
           'ranking_category': str,
           "price_level": int,
           "price": [min, max]  # цены в долларах
           },

# Collection: ways
element = {'_id': {},
           'location': {'coordinates': [[float, float], [float, float], ...],  # lon lat
                        'type': 'LineString'},
           'road': bool,
           'important': bool,
           'city': str,
           'entrance': str,  # id node которая является входом (а также узлом графа)
           'nodes': [],
           'simple_nodes': [],
           'simple_way': [[[float, float], [float, float], ...],
                          [[float, float], [float, float], ...], ...],  # !! LAT LON ( путь между двумя точками simple_nodes)
           'length': []}

# Collection: relations
element = {'_id': {},
           'location': {'coordinates': [[[float, float], [float, float], ...],
                                        [[float, float], [float, float], ...], ...],  # lon lat
                        'type': 'MultiLineString'},
           'road': bool,
           'important': bool,
           'city': str,
           'entrance': str,  # id node которая является входом (а также узлом графа)
           'ways': []}
