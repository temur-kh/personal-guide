import React, {useEffect, useState} from "react";

import ResultMapComponent from './ResultMapComponent'
import {useLocation} from "react-router-dom";
import {
    Container,
    Grid,
    Link,
    Typography,
    Button
} from "@material-ui/core"
import {useStyles} from "../constants"

const MapContent = (props) => {
    return <ResultMapComponent route={props.data} start={props.start} style/>;
};

export default function ResultForm() {
    const response = useLocation().response;
    const start = useLocation().start;
    const classes = useStyles();
    const [routeIndex, setRouteIndex] = useState(0);
    const noRoutes = response === undefined || response.routes.length === 0;

    const routes = noRoutes
        ? <Typography variant="h6" shrink fullWidth={false} className={classes.routeEmpty}>
            К сожалению, подходящий маршрут найти не удалось. Попробуйте задать новые параметры и повторить поиск
        </Typography>
        : response.routes.map((route, i) => (
            <Grid item xs={12} sm={12} md={12} lg={12} className={classes.submitButton}>
                <Typography variant="h6" shrink fullWidth={false}
                            className={classes.routeButton}
                            onClick={() => setRouteIndex(i)}>
                    Посмотреть маршрут №{i + 1}:
                </Typography>
            </Grid>
        ));

    return (
        <Container maxWidth="false">
            <Grid container>
                <Grid item xs={2}>
                    <Grid container>
                        {routes}
                        <Grid item xs={12} sm={12} md={12} lg={12} className={classes.submitButton}>
                            <Link href="/">
                                <Button type="submit" color="primary" variant="contained">
                                    Построить новый маршрут
                                </Button>
                            </Link>
                        </Grid>
                    </Grid>
                </Grid>
                <Grid item xs={10} className={classes.resultMap}>
                    <MapContent data={noRoutes ? undefined : response.routes[routeIndex]} start={start}/>
                </Grid>
            </Grid>
        </Container>
    );
}
