
def euclidean_distance(p1, p2):
    """
    Евклидово расстояние между двумя точками.

    Params:
        p1([double, double]) - lat и lon первой точки.
        p2([double, double]) - lat и lon второй точки.

    Return:
        double - Евклидово расстояние между двумя точками.
    """

    return sum([(first - second) ** 2 for first, second in zip(p1, p2)])


def get_matrix_distance(points, distance_function=euclidean_distance):
    """
    Матрица расстояний для точек.

    Params:
        points(array-like) - массив с точками.
        distance_function(func) - функция для поиска расстояния.

    Returns:
        2-d array-like - матрица расстояний.
    """

    matrix_distance = []
    for p1 in points:
        point_distance = []
        for p2 in points:
            point_distance.append(distance_function(p1, p2))
        matrix_distance.append(point_distance)
    return matrix_distance


def get_points_coordinates_from_query_result(query_result):
    """
    Извлечение координат точек после запроса к базе данных.

    Params:
        query_result(list) - результат запроса к базе данных.

    Returns:
        list - список точек с координатами lat и lon.

    """

    points = []
    for item in query_result:
        coordinates = item['location']['coordinates']
        points.append([coordinates[1], coordinates[0]])
    return points
