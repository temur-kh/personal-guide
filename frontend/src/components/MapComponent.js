// @flow

import React, {createRef, Component} from 'react'
import {Map, Marker, Popup, TileLayer} from 'react-leaflet'
import "../css/MapComponent.css"

type State = {
    latlng: {
        lat: number,
        lng: number,
    },
}

const mapRef = createRef<Map>();
let startLatLng = {
    lat: 52.5149111,
    lng: 13.3910441
}

export function changeView(center) {
    const {current = {}} = mapRef;
    const {leafletElement: map} = current;
    map.setView(center, 14);
    startLatLng = center;
}

export default class MapComponent extends Component<{}, State> {
    state = {
        latlng: startLatLng
    }

    handleClick = (e: Object) => {
        this.setState({
            latlng: e.latlng,
        })
        startLatLng = e.latlng;
        if (this.props.onChange) {
            this.props.onChange(this.state);
        }
    }

    render() {
        const marker =
            <Marker position={startLatLng}>
                <Popup>Стартовая точка</Popup>
            </Marker>

        return (
            <Map
                center={startLatLng}
                length={4}
                onClick={this.handleClick}
                ref={mapRef}
                zoom={14}>
                <TileLayer
                    attribution='&amp;copy <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
                    url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                />
                {marker}
            </Map>
        )
    }
}
