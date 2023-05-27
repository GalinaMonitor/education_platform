import {create} from "zustand";
import {devtools, persist} from "zustand/middleware";
import AuthService from "../services/AuthService";
import {error, success} from "../messages";


const useUserStore = create(persist(devtools((set) => ({
    isAuth: false,
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
    logout: async () => {
        set({token: ''});
        set({user: {}});
        set({isAuth: false})
    },
    register: async (email, password) => {
        set({isLoading: true})
        try {
            const register_response = await AuthService.register(email, password);
            if (register_response.status !== 200) {
                error("Ошибка при регистрации")
            }
            success("Регистрация прошла успешно")
        } catch (e) {
            error("Ошибка при регистрации")
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
        }
    },
    setIsAuth: (isAuth: boolean) => set((state) => ({
        isAuth: isAuth
    }))
})), {name: 'useUserStore'}))

export default useUserStore;