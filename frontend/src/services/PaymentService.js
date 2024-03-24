import $api from "../api";

export default class PaymentService {
  static async create_payment_link(subscriptionType) {
    return $api.post(`/payment/get_payment_link/${subscriptionType}/`);
  }
}
