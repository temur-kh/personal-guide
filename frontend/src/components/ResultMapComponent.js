// @flow

import React, {Component, createRef} from 'react'
import {Map, Marker, Popup, TileLayer} from 'react-leaflet'
import Polyline from 'react-leaflet-arrowheads'
import {Icon} from 'leaflet'
import "../css/ResultMapComponent.css"

function getIcon(iconType) {
    let iconUrl = "/custom_icons/";
    switch(iconType) {
        case 'food':
            iconUrl += "restaurant.png";
            break;
        case 'post':
            iconUrl += "post.png";
            break;
        case 'finance':
            iconUrl += "atm.png";
            break;
        case 'shop':
            iconUrl += "shop.png";
            break;
        case 'wc':
            iconUrl += "toilet.png";
            break;
        case 'telephone':
            iconUrl += "phone.png";
            break;
        case 'pharmacy':
            iconUrl += "hospital.png";
            break;

        case 'religion':
            iconUrl += "church.png";
            break;
        case 'entertainment':
            iconUrl += "museum.png";
            break;
        case 'historic':
            iconUrl += "castle.png";
            break;
        case 'architecture':
            iconUrl += "arch.png";
            break;
        case 'tourism':
            iconUrl += "obelisk.png";
            break;
        case 'start_point':
            iconUrl += "start.png";
            break;
        default:
            iconUrl += "default.png";
            break;
    }
    return new Icon({
        iconUrl: iconUrl,
        iconSize: [40, 40],
        iconAnchor: [20, 40]
    });
}

export default class ResultMapComponent extends Component<{}> {


    render() {
        const mapRef = createRef<Map>();
        const route = this.props.route;
        const popupRef = route !== undefined
            ? Array.from({length: route.points.length}, a => createRef<Popup>())
            : undefined;
        if (route === undefined) {
            return (
                <Map center={this.props.start === undefined ? {lat: 52.5120716, lng: 13.3864754} : this.props.start}
                     ref={mapRef}
                     zoom={14}
                     className={'leaflet-container-result'}>
                    <TileLayer
                        attribution='&amp;copy <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
                        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                    />
                    }))
                </Map>
            );
        }
        const markers = (
            route.points.map((point, i) => (
                <Marker
                    position={[point.lat, point.lng]}
                    icon={getIcon(point.category)}
                >
                    <Popup maxHeight={350} keepInView={true} ref={popupRef[i]}>
                        <div>
                            <h2 className="popup-title">
                                {point.attributes.title !== undefined && point.attributes.title !== null
                                    ? point.attributes.title
                                    : point.attributes.category_title}
                            </h2>
                            {point.attributes.food_rating !== undefined &&
                            <h3>Рейтинг: {point.attributes.food_rating}</h3>
                            }
                            {point.attributes.description !== undefined &&
                            <p className="popup-text">
                                {point.attributes.description.replace(/<(?:.|\n)*?>/gm, '')}
                            </p>
                            }
                            {point.attributes.poi_photo !== undefined &&
                            <img className="popup-photo"
                                 src={point.attributes.poi_photo}
                                 alt="POI"
                                 onLoad={() => popupRef[i].current.leafletElement.update()}
                            />
                            }
                            {point.attributes.food_images !== undefined &&
                            point.attributes.food_images.medium !== undefined &&
                            point.attributes.food_images.medium.url !== undefined &&
                            <img className="popup-photo" src={point.attributes.food_images.medium.url} alt="Food"/>
                            }
                        </div>
                    </Popup>
                </Marker>
            ))
        );

        const path = route.paths.map(path => {
            return [path.lat, path.lng];
        });

        return (
            <Map center={this.props.start}
                 ref={mapRef}
                 zoom={14}
                 className={'leaflet-container-result'}>
                <TileLayer
                    attribution='&amp;copy <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
                    url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                />
                {markers}
                (route.paths.map(path => {
                <Polyline
                    positions={[path]}
                    color={'black'}
                    opacity={0.8}
                    width={6}
                    arrowheads={{
                        'size': '40%',
                        'frequency': '130m',
                        'yawn': 35,
                        'fill': false
                    }}/>
            }))
            </Map>
        );
    }
}
