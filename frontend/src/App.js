import './App.css';
import {ConfigProvider, Layout} from "antd";
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
            <ConfigProvider
                theme={{
                    token: {
                        colorPrimary: '#FF7D1F',
                        colorInfo: '#FF7D1F',
                        fontFamily: 'Manrope',
                        borderRadius: 10,
                    },
                }}
            >
                <Layout className={'h-full'}>
                    <AppRouter/>
                </Layout>
            </ConfigProvider>
        </BrowserRouter>
    );
}

export default App;
