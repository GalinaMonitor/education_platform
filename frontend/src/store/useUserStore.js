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
          } else {
            success(
              "Вам на почту было направлено письмо для активации аккаунта. Проверьте папку спам."
            );
          }
        } catch (e) {
          if (e.response?.data?.detail === "User already registered") {
            error("Аккаунт с такой электронной почтой уже зарегистрирован");
          } else {
            error("Ошибка при регистрации");
          }
        }

        set({ isLoading: false });
      },
      prepareRestorePassword: async (email) => {
        set({ isLoading: true });
        try {
          const registerResponse = await AuthService.prepare_restore_password(
            email
          );
          if (registerResponse.status !== 200) {
            error("Ошибка при восстановлении");
          } else {
            success(
              "Ссылка на восстановление пароля отправлена вам на почту. Проверьте папку спам."
            );
          }
        } catch (e) {
          error("Ошибка при восстановлении");
        }
        set({ isLoading: false });
      },
      restorePassword: async (email, password, uuid) => {
        set({ isLoading: true });
        try {
          const registerResponse = await AuthService.restore_password(
            email,
            password,
            uuid
          );
          if (registerResponse.status !== 200) {
            error("Ошибка при восстановлении");
          } else {
            success("Пароль обновлен");
          }
        } catch (e) {
          error("Ошибка при восстановлении");
        }
        set({ isLoading: false });
      },
      activateUser: async (email, uuid) => {
        set({ isLoading: true });
        try {
          const registerResponse = await AuthService.activate_user(email, uuid);
          if (registerResponse.status !== 200) {
            error("Ошибка при активации");
          } else {
            success("Ваша учетная запись активирована");
          }
        } catch (e) {
          error("Ошибка при активации");
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
