import React from "react";
import {BrowserRouter as Router, Route, Switch} from "react-router-dom";
import BasicForm from "./components/BasicForm.js";
import ResultForm from "./components/ResultForm.js";
import {AppBar, Container, Toolbar, Typography} from "@material-ui/core";
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
    toolBar: {
        height: "64px",
        paddingTop: "5px",
        paddingBottom: "5px"
    },
    appBar: {
        borderRadius: "8px"
    }
}));

function App() {
    const classes = useStyles();
    return (
        <Container maxWidth="false" className={classes.root}>
            <AppBar position="static" className={classes.appBar}>
                <Toolbar className={classes.toolBar}>
                    <a href="/" style={{height: "100%"}}>
                        <img src="logo_title.png" alt="logo" className={classes.logo}/>
                    </a>
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
