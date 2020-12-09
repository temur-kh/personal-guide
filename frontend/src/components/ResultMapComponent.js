// @flow

import React, {Component, createRef} from 'react'
import {Map, Marker, TileLayer} from 'react-leaflet'
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
    mapRef = createRef<Map>()

    render() {
        const markers = (
            this.props.pathData.points.map(point => (
                <Marker
                    position={[point.lat, point.lng]}
                    icon={getIcon(point.category)}
                />
            ))
        );

        const path = this.props.pathData.paths.map(path => {
            return [path.lat, path.lng];
        })

        return (
            <Map center={this.props.pathData.paths[0]}
                 ref={this.mapRef}
                 zoom={14}
                 className={'leaflet-container-result'}>
                <TileLayer
                    attribution='&amp;copy <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
                    url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                />
                {markers}
                (pathData.paths.map(path => {
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
        )
    }
}
