import {create} from "zustand";
import {devtools, persist} from "zustand/middleware";
import AuthService from "../services/AuthService";


const useUserStore = create(persist(devtools((set) => ({
    isAuth: false,
    error: '',
    isLoading: false,
    user: {},
    token: '',
    login: async (email, password) => {
        set({isLoading: true})
        try {
            const login_response = await AuthService.login(email, password);
            set({token: login_response.data.access_token});

            const user_response = await AuthService.get_user();
            set({user: user_response.data})

            set({isAuth: true})
        } catch (e) {
            set({error: 'Неудачная авторизация'})
        }

        set({isLoading: false})
    },
    register: async (values) => {
        set({isLoading: true})
        try {
            const register_response = await AuthService.register(values);
            if (register_response.status !== 200) {
                set({error: 'Неудачная регистрация'})
            }
        } catch (e) {
            set({error: 'Неудачная регистрация'})
        }

        set({isLoading: false})
    },
    checkAuth: async () => {
        try {
            const user_response = await AuthService.get_user();
            set({user: user_response.data})

            set({isAuth: true})
        } catch (e) {
            set({isAuth: false})
            set({error: 'Неудачная авторизация'})
        }
    },
    setIsAuth: (isAuth: boolean) => set((state) => ({
        isAuth: isAuth
    }))
})), {name: 'useUserStore'}))

export default useUserStore;
