from graph_constructor.tags import all_tags


class StartingParams:
    def __init__(self, params):
        lat = params.get('start_lat')
        lon = params.get('start_lng')
        self.start_coordinates = [lon, lat]
        self.distance = params.get('distance')
        self.tags = params.get('tags')
        self.time_for_route = params.get('duration')
        self.speed = params.get('speed')

        self.global_tags = self._set_global_tags()
        self.start_point = {}

    def set_start_point(self, start_point):
        self.start_point = start_point

    def _set_global_tags(self):
        global_tags = set(all_tags.get(tag) for tag in self.tags)
        return {global_tag: [tag for tag in self.tags if all_tags.get(tag) == global_tag]
                for global_tag in global_tags}

    def get_key(self):
        coord = self.start_point['location']['coordinates']
        return "_".join((str(coord),
                         str(self.distance),
                         str(self.tags)))

    def get_city(self):
        return self.start_point.get('city')

    def get_start_id(self):
        return self.start_point['id_osm']

    def get_start_point_coord(self):
        coord = self.start_point['location']['coordinates']
        return [coord[1], coord[0]]

    def get_start_point_attrs(self):
        """
        Получение аттрибутов точек интереса для возврата на фронтенд.
        Args:
            params(dict) - параметры с ограничениями для маршрута.
        Returns:
            attrs(dict) - аттрибуты для стартовой точки.
        """

        def printable_speed(speed):
            return speed * 60 / 1000

        speed = printable_speed(self.speed)

        title = 'Стартовая точка'
        description = f"Продолжительность машрута: {self.time_for_route} минут.\n" + \
                      f"Ориентировочная скорость пешехода: {speed:0.1f} км/ч."
        attrs = {
            'category_title': title,
            'title': title,
            'description': description
        }
        return attrs
