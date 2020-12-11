import {makeStyles, Slider, withStyles} from "@material-ui/core"

export const useStyles = makeStyles((_) => ({
    grid: {
        marginTop: '10px',
    },
    durationInput: {
        width: 75,
        marginLeft: '30px',
        marginTop: '15px'
    },
    formControl: {
        minWidth: 120,
    },
    submitButton: {
        textAlign: 'center',
        marginTop: '20px'
    },
    mapComponent: {
        paddingLeft: '90px',
        flexBasis: '70%'
    },
    submitForm: {
        maxWidth: '30%',
        flexBasis: '30%'
    }
}));

export const borderProps = {
    borderColor: "#5064e1",
    border: 2,
    borderRadius: 16,
    marginTop: '10px',
    marginBottom: '10px',
    padding: '10px',
    width: '100%'
};

export const CustomSlider = withStyles({
    root: {
        color: '#3f51b5',
        height: 8
    },
    thumb: {
        height: 24,
        width: 24,
        backgroundColor: '#fff',
        border: '2px solid currentColor',
        marginTop: -8,
        marginLeft: -12,
        '&:focus, &:hover, &$active': {
            boxShadow: 'inherit',
        },
    },
    active: {},
    valueLabel: {
        left: 'calc(-50% + 4px)',
    },
    track: {
        height: 8,
        borderRadius: 4,
    },
    rail: {
        height: 8,
        borderRadius: 4,
    },
    mark: {
        backgroundColor: '#5064e1',
        height: 8,
        width: 1,
        marginTop: -6,
    }
})(Slider);

export const durationMarks = [
    {
        value: 30,
        label: '30 минут',
    },
    {
        value: 60,
    },
    {
        value: 90,
    },
    {
        value: 120,
    },
    {
        value: 150,
    },
    {
        value: 180,
    },
    {
        value: 210,
    },
    {
        value: 240,
    },
    {
        value: 270,
    },
    {
        value: 300,
    },
    {
        value: 330,
    },
    {
        value: 360,
        label: '6 часов',
    }
];

export const cityCenters = {
    "berlin": {
        lat: 52.5149111,
        lng: 13.3910441
    },
    "kaliningrad": {
        lat: 54.7105,
        lng: 20.5145
    },
    "saint-petersburg": {
        lat: 59.9423,
        lng: 30.3297
    }
};
