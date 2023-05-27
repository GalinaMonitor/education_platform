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
                        fontSize: 14,
                        colorLink: '#FF7D1F',
                        colorLinkActive: '#FF7D1F',
                        colorLinkHover: '#FF7D1F',
                        colorPrimaryHover: '#FF7D1F',
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
