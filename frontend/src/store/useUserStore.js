import { create } from "zustand";
import { devtools, persist } from "zustand/middleware";
import AuthService from "../services/AuthService";
import { error, success } from "../messages";

const useUserStore = create(
  persist(
    devtools((set) => ({
      isAuth: false,
      isLoading: false,
      user: {},
      token: "",
      timeOnPlatform: 0,
      login: async (email, password) => {
        set({ isLoading: true });
        try {
          const loginResponse = await AuthService.login(email, password);
          set({ token: loginResponse.data.access_token });

          const userResponse = await AuthService.get_user();
          set({ user: userResponse.data });

          set({ isAuth: true });
          set({
            timeOnPlatform: userResponse.data.time_on_platform,
          });
        } catch (e) {
          set({ error: "Неудачная авторизация" });
          error("Пароль/логин не верные");
        }

        set({ isLoading: false });
      },
      logout: async () => {
        set({ token: "" });
        set({ user: {} });
        set({ isAuth: false });
      },
      register: async (email, password) => {
        set({ isLoading: true });
        try {
          const registerResponse = await AuthService.register(email, password);
          if (registerResponse.status !== 200) {
            error("Ошибка при регистрации");
          }
          success("Регистрация прошла успешно");
        } catch (e) {
          error("Ошибка при регистрации");
        }

        set({ isLoading: false });
      },
      checkAuth: async () => {
        try {
          const userResponse = await AuthService.get_user();
          set({ user: userResponse.data });

          set({ isAuth: true });
        } catch (e) {
          set({ isAuth: false });
        }
      },
      setIsAuth: (isAuth) =>
        set((state) => ({
          isAuth: isAuth,
        })),
      setTimeOnPlatform: (minutes) =>
        set((state) => ({
          timeOnPlatform: minutes,
        })),
    })),
    { name: "useUserStore" }
  )
);

export default useUserStore;
