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

export default class MapComponent extends Component<{}, State> {
    state = {
        latlng: {
            lat: 52.5149111,
            lng: 13.3910441
        },
    }

    mapRef = createRef<Map>()

    handleClick = (e: Object) => {
        this.setState({
            latlng: e.latlng,
        })
        if (this.props.onChange) {
            this.props.onChange(this.state);
        }
    }

    render() {
        const marker =
            <Marker position={this.state.latlng}>
                <Popup>Стартовая точка</Popup>
            </Marker>

        return (
            <Map
                center={this.state.latlng}
                length={4}
                onClick={this.handleClick}
                ref={this.mapRef}
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
