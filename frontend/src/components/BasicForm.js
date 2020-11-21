import React, {useState, createRef} from "react";
import {makeStyles} from "@material-ui/core/styles";
import TextField from "@material-ui/core/TextField";
import Button from "@material-ui/core/Button";
import Container from "@material-ui/core/Container";
import Grid from "@material-ui/core/Grid";
import Typography from "@material-ui/core/Typography";
import Alert from "@material-ui/lab/Alert";
import InputLabel from '@material-ui/core/InputLabel';
import MenuItem from '@material-ui/core/MenuItem';
import Select from '@material-ui/core/Select';
import MapComponent from './MapComponent'

import axios from "axios";

const useStyles = makeStyles((_) => ({
    input: {
        margin: 5,
    },
}));

function getStartDT() {
    return new Date((new Date()).getTime() + (5 * 60 * 1000));
}

function getEndDT(startDT) {
    return new Date(startDT.getTime() + (2 * 3600 * 1000));
}

function getDTString(datetime) {
    return datetime.toISOString().slice(0, 16)
}

export default function BasicForm() {
    const url = "api/submit"
    const classes = useStyles()
    const [startLoc, setStartLoc] = useState("")
    const [coords, setCoords] = useState(false)
    const [startDT, setStartDT] = useState(getDTString(getStartDT()))
    const [endDT, setEndDT] = useState(getDTString(getEndDT(getStartDT())))
    const [tripType, setTripType] = useState("history")
    const [success, setSuccess] = useState(undefined)

    function handleInputStartLoc(e) {
        setStartLoc(e.target.value);
        setCoords(false);
    }

    function handleInputStartDT(e) {
        setStartDT(e.target.value);
    }

    function handleInputEndDT(e) {
        setEndDT(e.target.value);
    }

    function handleInputTripType(e) {
        setTripType(e.target.value);
    }

    function handleMapChanges(e) {
        let coords = e.latlng.lat + " " + e.latlng.lng
        setStartLoc(coords);
        setCoords(true);
    }

    function handleSubmit(e) {
        e.preventDefault();
        const data = new FormData();
        data.set("start_loc", startLoc);
        data.set("is_coords", coords);
        data.set("start_datetime", startDT);
        data.set("end_datetime", endDT);
        data.set("trip_type", tripType)

        axios({
            method: "post",
            url: url,
            data: data,
        })
            .then(function (response) {
                console.log(response);
                setSuccess(true);
            })
            .catch(function (response) {
                setSuccess(false);
                console.log(response);
            });
    }

    function Alerting() {
        if (success === true) {
            return <Alert severity="success">Data successfully sent !</Alert>;
        } else if (success === false) {
            return <Alert severity="error">Oops. An error just occurred!</Alert>;
        } else {
            return null;
        }
    }

    return (
        <Container>
            <MapComponent onChange={handleMapChanges}/>
            <form onSubmit={handleSubmit}>
                <Grid container justify="center">

                    <Grid item xs={12} sm={12} md={6} lg={6} className={classes.input}>
                        <TextField
                            required
                            name="start_loc"
                            id="start_loc"
                            label="Start location"
                            fullWidth={true}
                            value={startLoc}
                            onChange={handleInputStartLoc}
                        />
                    </Grid>

                    <Grid item xs={12} sm={12} md={6} lg={6} className={classes.input}>
                        <TextField
                            required
                            type="datetime-local"
                            name="start_dt"
                            id="start_dt"
                            label="Start DateTime"
                            fullWidth={true}
                            value={startDT}
                            onChange={handleInputStartDT}
                            InputLabelProps={{
                                shrink: true,
                            }}
                        />
                    </Grid>

                    <Grid item xs={12} sm={12} md={6} lg={6} className={classes.input}>
                        <TextField
                            required
                            type="datetime-local"
                            name="end_dt"
                            id="end_dt"
                            label="End DateTime"
                            fullWidth={true}
                            value={endDT}
                            onChange={handleInputEndDT}
                            InputLabelProps={{
                                shrink: true,
                            }}
                        />
                    </Grid>


                    <Grid item xs={12} sm={12} md={6} lg={6} className={classes.input}>
                        <InputLabel shrink fullWidth={true} id="trip_type">
                            Trip type
                        </InputLabel>
                        <Select
                            labelId="trip_type"
                            value={tripType}
                            onChange={handleInputTripType}
                            displayEmpty
                            className={classes.selectEmpty}
                            inputProps={{'aria-label': 'Without label'}}
                        >
                            <MenuItem value={"historic"}>Исторический</MenuItem>
                            <MenuItem value={"architecture"}>Архитектурный</MenuItem>
                            <MenuItem value={"entertainment"}>Развлекательный</MenuItem>
                            <MenuItem value={"custom"}>Кастомный</MenuItem>
                        </Select>
                    </Grid>

                    <Grid item xs={12} sm={12} md={6} lg={6}>
                        <Typography align="center">
                            <Button type="submit" color="primary" variant="contained">
                                Submit
                            </Button>
                            <div style={{marginTop: 10}}>
                                <Alerting/>
                            </div>
                        </Typography>
                    </Grid>
                </Grid>
            </form>
        </Container>
    );

}
