import React, {useState} from "react";

import Alert from "@material-ui/lab/Alert";
import MapComponent from './MapComponent'
import {useHistory} from "react-router-dom";
import {
    Button,
    Container,
    Grid,
    Typography,
    MenuItem,
    Select,
    OutlinedInput,
    FormControl,
    FormGroup,
    FormControlLabel,
    Checkbox,
    Box
} from "@material-ui/core"
import {useStyles, durationMarks, CustomSlider, borderProps} from "../constants.js"

import axios from "axios";


export default function BasicForm() {
    let history = useHistory();
    const url = "api/submit"
    const minDuration = 30
    const maxDuration = 360
    const durationStep = 30
    const classes = useStyles()
    const [startLatLng, setStartLatLng] = useState({
        lat: 52.5149111,
        lng: 13.3910441
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
        entertainment_museum: true,
        entertainment_theatre: true,
        entertainment_cinema: true,
        entertainment_zoo: true,
        entertainment_park: true,
        entertainment_planetarium: true,
        entertainment_aquarium: true,
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

    function handleInputTripType(e) {
        setTripType(e.target.value);
        setDisplayPlaces("block");
        setPlaces({...historicPlaces, ...tourismPlaces, ...architecturePlaces, ...religionPlaces, ...entertainmentPlaces})
    }

    function handleInputNeedReturn(e) {
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
                    {getFormControlLabel(
                        places.entertainment_museum, "entertainment_museum", "Музеи/галереи/выставки"
                    )}
                    {getFormControlLabel(
                        places.entertainment_theatre, "entertainment_theatre", "Театры"
                    )}
                    {getFormControlLabel(
                        places.entertainment_cinema, "entertainment_cinema", "Кинотеатры"
                    )}
                    {getFormControlLabel(
                        places.entertainment_zoo, "entertainment_zoo", "Зоопарки"
                    )}
                    {getFormControlLabel(
                        places.entertainment_park, "entertainment_park", "Парки аттракционов"
                    )}
                    {getFormControlLabel(
                        places.entertainment_planetarium, "entertainment_planetarium", "Зоопарки"
                    )}
                    {getFormControlLabel(
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
                                <Grid item xs={12} sm={12} md={12} lg={12} className={classes.grid}>
                                    <FormControl variant="outlined" className={classes.formControl}>
                                        <Typography variant="h6" shrink fullWidth={true} id="trip_type">
                                            Тип маршрута:
                                        </Typography>
                                        <Select
                                            required
                                            labelId="trip_type"
                                            value={tripType}
                                            onChange={handleInputTripType}
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
                                <Grid item xs={12} sm={12} md={12} lg={12} className={classes.grid}>
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
                                        onChange={handleInputNeedReturn}
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
                                <div style={{marginTop: 10}}>
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
