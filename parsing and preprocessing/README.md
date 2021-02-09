Для загрузки данных из osm:
1. получить из osm Relation ID города. В нашем случае:
    * Калининград - 1674442
    * Берлин - 62422
    * Санкт-Петербург - 421007
2. Загрузить полигон города по полученному ID, воспользовавшись [сайтом](http://polygons.openstreetmap.fr) в формате **poly**
3. На [сайте](https://download.geofabrik.de/index.html) скачать данные по интересующему региону (в нашем случае для Европы) в формате **osm.pbf**. 
4. Установить **Osmosis** и извлечь из данных, выгруженных в п.3 только необходимый город с помощью команды:

``osmosis --read-pbf-fast file="europe-latest.osm.pbf" --bounding-polygon file="CITY.poly" --write-xml file="data/CITY.osm"``