import './App.css';
import {Layout} from "antd";
import AppRouter from "./components/AppRouter";
import {BrowserRouter} from "react-router-dom";
import {useEffect} from "react";
import useUserStore from "./store";

const App = () => {
    const {checkAuth} = useUserStore()

    useEffect(() => {
        checkAuth()
    }, [])

    return (
        <BrowserRouter>
            <Layout className={'h-full'}>
                <AppRouter/>
            </Layout>
        </BrowserRouter>
    );
}

export default App;
