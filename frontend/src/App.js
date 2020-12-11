import React from "react";
import {BrowserRouter as Router, Route, Switch} from "react-router-dom";
import BasicForm from "./components/BasicForm.js";
import ResultForm from "./components/ResultForm.js";
import {Container} from "@material-ui/core";
import AppBar from "@material-ui/core/AppBar";
import Toolbar from "@material-ui/core/Toolbar";
import Typography from "@material-ui/core/Typography";
import {makeStyles} from "@material-ui/core/styles";

const useStyles = makeStyles((_) => ({
    root: {
        backgroundColor: "#eaeaea"
    },
    title: {
        marginLeft: "15px"
    },
    logo: {
        maxHeight: "100%",
        maxWidth: "100%"
    },
    toolbar: {
        height: "64px",
        paddingTop: "5px",
        paddingBottom: "5px",
        borderRadius: "8px"
    }
}));

function App() {
    const classes = useStyles();
    return (
        <Container maxWidth="false" className={classes.root}>
            <AppBar position="static">
                <Toolbar className={classes.toolbar}>
                    <img src="logo_title.png" alt="logo" className={classes.logo} />
                    <Typography variant="h6" className={classes.title}>
                        WalkCreator
                    </Typography>
                </Toolbar>
            </AppBar>
            <br/>
            <Router>
                <Switch>
                    <Route exact path="/" component={BasicForm}/>
                    <Route path="/result" component={ResultForm}/>
                </Switch>
            </Router>
        </Container>
    );
}

export default App;
