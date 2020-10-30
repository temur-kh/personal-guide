// @flow

import React, {createRef, Component} from 'react'
import {Map, Marker, Popup, TileLayer} from 'react-leaflet'

type State = {
    hasLocation: boolean,
    latlng: {
        lat: number,
        lng: number,
    },
}

export default class MapComponent extends Component<{}, State> {
    state = {
        hasLocation: false,
        latlng: {
            lat: 51.505,
            lng: -0.09,
        },
    }

    mapRef = createRef<Map>()

    handleClick = (e: Object) => {
        this.setState({
            hasLocation: true,
            latlng: e.latlng,
        })
        if (this.props.onChange) {
            this.props.onChange(this.state);
        }
    }

    // handleLocationFound = (e: Object) => {
    //     this.setState({
    //         hasLocation: true,
    //         latlng: e.latlng,
    //     })
    // }

    render() {
        const marker = this.state.hasLocation ? (
            <Marker position={this.state.latlng}>
                <Popup>You are here</Popup>
            </Marker>
        ) : null

        return (
            <Map
                center={this.state.latlng}
                length={4}
                onClick={this.handleClick}
                // onLocationfound={this.handleLocationFound}
                ref={this.mapRef}
                zoom={13}>
                <TileLayer
                    attribution='&amp;copy <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
                    url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                />
                {marker}
            </Map>
        )
    }
}