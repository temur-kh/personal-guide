import React, {useEffect, useState} from "react";

import Alert from "@material-ui/lab/Alert";
import MapComponent, {changeView} from './MapComponent'
import {useHistory} from "react-router-dom";
import {
    Box,
    Button,
    Checkbox,
    Container,
    FormControl,
    FormControlLabel,
    FormGroup,
    Grid,
    MenuItem,
    OutlinedInput,
    Select,
    Typography
} from "@material-ui/core"
import {borderProps, cityCenters, CustomSlider, durationMarks, useStyles} from "../constants"

import axios from "axios";


export default function BasicForm() {
    let history = useHistory();
    const url = "api/submit"
    const minDuration = 30
    const maxDuration = 360
    const durationStep = 30
    const classes = useStyles()
    const [city, setCity] = useState("berlin")
    const [firstLoad, setFirstLoad] = useState(true)
    const [startLatLng, setStartLatLng] = useState({
        lat: 52.5120716,
        lng: 13.3864754
    })
    const [duration, setDuration] = useState(120)
    const [tripType, setTripType] = useState("historic")
    const [needReturn, setNeedReturn] = useState(false)
    const [loadingStatus, setLoadingStatus] = useState(undefined)
    const [displayPlaces, setDisplayPlaces] = useState("block")
    const [historicPlaces] = useState({
        historic_historic: true,
        historic_archaeological: true,
        historic_tomb: true,
        historic_military: true,
        historic_transport: true,
        historic_memorial: true,
        historic_city: true
    });
    const [tourismPlaces] = useState({
        tourism_monument: true,
        tourism_sculpture: true,
        tourism_viewpoint: true,
        tourism_tourism: true,
        tourism_fountain: true
    });
    const [architecturePlaces] = useState({
        architecture: true
    });
    const [religionPlaces] = useState({
        religion_building: true,
        religion_church: true
    });
    const [entertainmentPlaces] = useState({
        entertainment_art: true,
        entertainment_museum: false,
        entertainment_theatre: false,
        entertainment_cinema: false,
        entertainment_zoo: false,
        entertainment_park: false,
        entertainment_planetarium: false,
        entertainment_aquarium: false,
    });
    const [additionalPlaces, setAdditionalPlaces] = useState({
        finance_bank: false,
        finance_atm: false,
        finance_bureau_de_change: false,
        food_pub: false,
        food_fast: false,
        food_cafe: false,
        food_restaurant: false,
        pharmacy: false,
        post: false,
        shop: false,
        wc: false,
        telephone: false,
    });
    const [places, setPlaces] = useState(
        {...historicPlaces, ...tourismPlaces, ...architecturePlaces, ...religionPlaces, ...entertainmentPlaces}
    );

    useEffect(() => {
        if (firstLoad) {
            handleCityChange("berlin");
            setFirstLoad(false);
        }
    });

    function handleSelectCity(e) {
        handleCityChange(e.target.value);
    }

    function handleCityChange(city) {
        setCity(city);
        let cityCenter;
        switch (city) {
            case "kaliningrad":
                cityCenter = cityCenters.kaliningrad;
                break;
            case "saint-petersburg":
                cityCenter = cityCenters["saint-petersburg"];
                break;
            case "berlin":
            default:
                cityCenter = cityCenters.berlin;
                break;
        }
        changeView(cityCenter);
        setStartLatLng(cityCenter);
    }

    function handleSelectTripType(e) {
        setTripType(e.target.value);
        setDisplayPlaces("block");
        setPlaces({...historicPlaces, ...tourismPlaces, ...architecturePlaces, ...religionPlaces, ...entertainmentPlaces})
    }

    function handleSelectNeedReturn(e) {
        setNeedReturn(Boolean(e.target.value));
    }

    function handleMapChanges(e) {
        setStartLatLng(e.latlng)
    }

    const handleDurationSliderChange = (event, newDuration) => {
        setDuration(newDuration);
    };

    const handleDurationInputChange = (event) => {
        setDuration(event.target.value === '' ? '' : Number(event.target.value));
    };

    const handleDurationBlur = () => {
        if (duration < minDuration) {
            setDuration(minDuration);
        } else if (duration > maxDuration) {
            setDuration(maxDuration);
        }
    };

    const handlePlacesCheckboxChange = (event) => {
        setPlaces({...places, [event.target.name]: event.target.checked});
    };

    const handleAdditionalPlacesCheckboxChange = (event) => {
        setAdditionalPlaces({...additionalPlaces, [event.target.name]: event.target.checked});
    };

    function handleSubmit(e) {
        e.preventDefault();
        const data = new FormData();
        data.set("start_lat", startLatLng.lat);
        data.set("start_lng", startLatLng.lng);
        data.set("duration", duration);
        data.set("trip_type", tripType);
        data.set("need_return", needReturn);
        const tags = Object.entries(places).map(([tag, checked]) => {
            return checked && tag.startsWith(tripType) ? tag : undefined;
        }).filter(tag => tag !== undefined);
        data.set("tags", tags);

        const constraints = Object.entries(additionalPlaces).map(([tag, checked]) => {
            return checked ? tag : undefined;
        }).filter(tag => tag !== undefined);
        data.set("constraints", constraints);

        setLoadingStatus("loading");
        axios({
            method: "post",
            url: url,
            data: data,
        })
            .then(function (response) {
                console.log(response);
                setLoadingStatus("success");
                history.push({
                    pathname: "/result",
                    start: startLatLng,
                    response: response.data
                });
            })
            .catch(function (response) {
                setLoadingStatus("error");
                console.log(response);
            })
    }

    function Alerting() {
        if (loadingStatus === "success") {
            return <Alert severity="success">Маршрут был успешно посчитан.</Alert>;
        } else if (loadingStatus === "error") {
            return <Alert severity="error">Упс. Произошла ошибка!</Alert>;
        } else if (loadingStatus === "loading") {
            return <Alert severity="info">Идет просчет наилучшего пути...</Alert>;
        } else {
            return null;
        }
    }

    function getAdditionalFormControlLabel(checked, name, label) {
        return <FormControlLabel control={
            <Checkbox
                checked={checked}
                onChange={handleAdditionalPlacesCheckboxChange}
                name={name}
                color="primary"
            />
        } label={label}
        />
    }

    function getDisabledFormControlLabel(checked, name, label) {
        return <FormControlLabel disabled control={
            <Checkbox
                checked={checked}
                onChange={handlePlacesCheckboxChange}
                name={name}
                color="primary"
            />
        } label={label}
        />
    }

    function getFormControlLabel(checked, name, label) {
        return <FormControlLabel control={
            <Checkbox
                checked={checked}
                onChange={handlePlacesCheckboxChange}
                name={name}
                color="primary"
            />
        } label={label}
        />
    }

    function getFromGroupTripSubtypes() {
        switch (tripType) {
            case "historic":
                return <FormGroup row>
                    {getFormControlLabel(
                        places.historic_archaeological, "historic_archaeological", "Археология"
                    )}
                    {getFormControlLabel(
                        places.historic_tomb, "historic_tomb", "Могилы"
                    )}
                    {getFormControlLabel(
                        places.historic_military, "historic_military", "Военная история"
                    )}
                    {getFormControlLabel(
                        places.historic_city, "historic_city", "Замки и оборонительные стены"
                    )}
                    {getFormControlLabel(
                        places.historic_memorial, "historic_memorial", "Памятные таблички"
                    )}
                </FormGroup>
            case "tourism":
                return <FormGroup row>
                    {getFormControlLabel(
                        places.tourism_monument, "tourism_monument", "Монументы"
                    )}
                    {getFormControlLabel(
                        places.tourism_sculpture, "tourism_sculpture", "Скульптуры и статуи"
                    )}
                    {getFormControlLabel(
                        places.tourism_viewpoint, "tourism_viewpoint", "Смотровые площадки"
                    )}
                    {getFormControlLabel(
                        places.tourism_tourism, "tourism_tourism", "Туристические места"
                    )}
                    {getFormControlLabel(
                        places.tourism_fountain, "tourism_fountain", "Фонтаны"
                    )}
                </FormGroup>
            case "religion":
                return <FormGroup row>
                    {getFormControlLabel(
                        places.religion_building, "religion_building", "Религиозные сооружения"
                    )}
                    {getFormControlLabel(
                        places.religion_church, "religion_church", "Соборы и храмы"
                    )}
                </FormGroup>
            case "entertainment":
                return <FormGroup row>
                    {getFormControlLabel(
                        places.entertainment_art, "entertainment_art", "Произведения искусства"
                    )}
                    {getDisabledFormControlLabel(
                        places.entertainment_museum, "entertainment_museum", "Музеи/галереи/выставки"
                    )}
                    {getDisabledFormControlLabel(
                        places.entertainment_theatre, "entertainment_theatre", "Театры"
                    )}
                    {getDisabledFormControlLabel(
                        places.entertainment_cinema, "entertainment_cinema", "Кинотеатры"
                    )}
                    {getDisabledFormControlLabel(
                        places.entertainment_zoo, "entertainment_zoo", "Зоопарки"
                    )}
                    {getDisabledFormControlLabel(
                        places.entertainment_park, "entertainment_park", "Парки аттракционов"
                    )}
                    {getDisabledFormControlLabel(
                        places.entertainment_planetarium, "entertainment_planetarium", "Зоопарки"
                    )}
                    {getDisabledFormControlLabel(
                        places.entertainment_aquarium, "entertainment_aquarium", "Океанариумы"
                    )}
                </FormGroup>
            case "architecture":
            default:
                return null;
        }
    }

    function getAdditionalPlaces() {
        return <FormGroup row>
            {getAdditionalFormControlLabel(
                additionalPlaces.finance_bank, "finance_bank", "Банк"
            )}
            {getAdditionalFormControlLabel(
                additionalPlaces.finance_atm, "finance_atm", "Банкомат"
            )}
            {getAdditionalFormControlLabel(
                additionalPlaces.finance_bureau_de_change, "finance_bureau_de_change", "Обмен валют"
            )}
            {getAdditionalFormControlLabel(
                additionalPlaces.food_pub, "food_pub", "Бар, паб"
            )}
            {getAdditionalFormControlLabel(
                additionalPlaces.food_fast, "food_fast", "Fast food"
            )}
            {getAdditionalFormControlLabel(
                additionalPlaces.food_cafe, "food_cafe", "Кафе"
            )}
            {getAdditionalFormControlLabel(
                additionalPlaces.food_restaurant, "food_restaurant", "Ресторан"
            )}
            {getAdditionalFormControlLabel(
                additionalPlaces.pharmacy, "pharmacy", "Аптека"
            )}
            {getAdditionalFormControlLabel(
                additionalPlaces.post, "post", "Почта"
            )}
            {getAdditionalFormControlLabel(
                additionalPlaces.shop, "shop", "Магазин"
            )}
            {getAdditionalFormControlLabel(
                additionalPlaces.wc, "wc", "Туалет"
            )}
            {getAdditionalFormControlLabel(
                additionalPlaces.telephone, "telephone", "Телефон"
            )}
        </FormGroup>
    }

    return (
        <Container maxWidth="false">
            <Grid container>
                <Grid item xs={3} className={classes.submitForm}>
                    <form onSubmit={handleSubmit}>
                        <Grid container>
                            <Grid item xs={12} sm={12} md={12} lg={12}>
                                <FormControl variant="outlined" className={classes.formControl}>
                                    <Typography variant="h6" shrink fullWidth={true} id="city">
                                        Город:
                                    </Typography>
                                    <Select
                                        required
                                        labelId="city"
                                        value={city}
                                        onChange={handleSelectCity}
                                    >
                                        <MenuItem value={"berlin"}>Берлин</MenuItem>
                                        <MenuItem value={"kaliningrad"}>Калинград</MenuItem>
                                        <MenuItem value={"saint-petersburg"}>Санкт-Петербург</MenuItem>
                                    </Select>
                                </FormControl>
                            </Grid>
                            <Grid item xs={11} sm={11} md={11} lg={11} className={classes.grid}>
                                <Typography variant="h6" shrink fullWidth={true} id="duration-label">
                                    Длительность маршрута(в минутах):
                                </Typography>
                                <CustomSlider
                                    valueLabelDisplay="auto"
                                    aria-label="duration slider"
                                    defaultValue={duration}
                                    value={duration}
                                    step={durationStep}
                                    marks={durationMarks}
                                    min={minDuration}
                                    max={maxDuration}
                                    onChange={handleDurationSliderChange}
                                    aria-labelledby="duration-label"
                                />
                            </Grid>
                            <Grid item xs={1} sm={1} md={1} lg={1} className={classes.grid}>
                                <OutlinedInput
                                    required
                                    className={classes.durationInput}
                                    name="duration"
                                    id="duration"
                                    value={duration}
                                    fullWidth={true}
                                    onChange={handleDurationInputChange}
                                    onBlur={handleDurationBlur}
                                    inputProps={{
                                        step: durationStep,
                                        min: minDuration,
                                        max: maxDuration,
                                        type: 'number',
                                        'aria-labelledby': 'duration-label',
                                    }}
                                />
                            </Grid>
                            <Box {...borderProps} display={displayPlaces}>
                                <Grid item xs={12} sm={12} md={12} lg={12}>
                                    <FormControl variant="outlined" className={classes.formControl}>
                                        <Typography variant="h6" shrink fullWidth={true} id="trip_type">
                                            Тип маршрута:
                                        </Typography>
                                        <Select
                                            required
                                            labelId="trip_type"
                                            value={tripType}
                                            onChange={handleSelectTripType}
                                        >
                                            <MenuItem value={"historic"}>Исторический</MenuItem>
                                            <MenuItem value={"architecture"}>Архитектурный</MenuItem>
                                            <MenuItem value={"entertainment"}>Культурный</MenuItem>
                                            <MenuItem value={"tourism"}>Туристический</MenuItem>
                                            <MenuItem value={"religion"}>Религиозный</MenuItem>
                                        </Select>
                                    </FormControl>
                                </Grid>
                                <Grid item xs={12} sm={12} md={12} lg={12} className={classes.grid}>
                                    <Box>{getFromGroupTripSubtypes}</Box>
                                </Grid>
                            </Box>
                            <Box {...borderProps} display={displayPlaces}>
                                <Grid item xs={12} sm={12} md={12} lg={12}>
                                    <Typography variant="h6" shrink fullWidth={true} id="additional_places">
                                        Хочу еще посетить:
                                    </Typography>
                                    <Box>{getAdditionalPlaces}</Box>
                                </Grid>
                            </Box>
                            <Grid item xs={12} sm={12} md={12} lg={12} className={classes.grid}>
                                <FormControl variant="outlined" className={classes.formControl}>
                                    <Typography variant="h6" shrink fullWidth={true} id="need_type">
                                        Хочу вернуться:
                                    </Typography>
                                    <Select
                                        required
                                        labelId="need-return"
                                        value={needReturn}
                                        onChange={handleSelectNeedReturn}
                                    >
                                        <MenuItem value={true}>Да</MenuItem>
                                        <MenuItem value={false}>Нет</MenuItem>
                                    </Select>
                                </FormControl>
                            </Grid>

                            <Grid item xs={12} sm={12} md={12} lg={12} className={classes.submitButton}>
                                <Button type="submit" color="primary" variant="contained">
                                    Построить маршрут
                                </Button>
                                <div style={{marginTop: 10, marginBottom: 10}}>
                                    <Alerting/>
                                </div>
                            </Grid>
                        </Grid>
                    </form>
                </Grid>
                <Grid item xs={9} className={classes.mapComponent}>
                    <MapComponent onChange={handleMapChanges}/>
                </Grid>
            </Grid>
        </Container>
    );

}
