import React from "react";
import BasicForm from "./components/BasicForm.js";
import {Container} from "@material-ui/core";
import AppBar from "@material-ui/core/AppBar";
import Toolbar from "@material-ui/core/Toolbar";
import Typography from "@material-ui/core/Typography";
import {makeStyles} from "@material-ui/core/styles";

const useStyles = makeStyles((_) => ({
    input: {
        margin: 5,
    },
}));

function App() {
    const classes = useStyles();
    return (
        <Container>
            <AppBar position="static">
                <Toolbar>
                    <Typography variant="h6" className={classes.title}>
                        Персональный гид
                    </Typography>
                </Toolbar>
            </AppBar>
            <br/>
            <BasicForm/>
        </Container>
    );
}

export default App;
