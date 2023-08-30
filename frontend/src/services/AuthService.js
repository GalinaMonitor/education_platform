import $api from "../api";

export default class AuthService {
  static async login(email, password) {
    return $api.post("/auth/token", { email, password });
  }

  static async register(email, password) {
    return $api.post("/auth/users", { email, password });
  }

  static async prepare_restore_password(email) {
    return $api.post("/auth/users/prepare_restore_password", { email });
  }

  static async restore_password(email, password, uuid) {
    return $api.post(`/auth/users/restore_password/${email}/${uuid}`, {
      password,
    });
  }

  static async activate_user(email, uuid) {
    return $api.post(`/auth/users/activate_user/${email}/${uuid}`);
  }

  static async get_user() {
    return $api.get("/auth/users/me");
  }

  static async logout() {
    return $api.post("/logout");
  }
}
