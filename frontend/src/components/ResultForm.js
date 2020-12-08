import Container from "@material-ui/core/Container";
import ResultMapComponent from './ResultMapComponent'
import {useLocation} from "react-router-dom";

export default function ResultForm() {
    const response = useLocation().response;
    return (
        <Container maxWidth="false">
            <ResultMapComponent pathData={response}/>
        </Container>
    );
}
