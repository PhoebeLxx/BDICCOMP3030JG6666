<script>
import Welcome from "../pages/Welcome.vue";
import Home from "../pages/Home.vue";
import BaggageHome from "../pages/Page-Baggage-Home.vue";
import BaggageOrder1 from "../pages/Page-Baggage-Order.vue";
import BaggageOrder from "../pages/Page-Baggage-CreateOrder.vue";
import EmployeeOrder from "../pages/Page-Employee-Order.vue";
import CustomerCenter from "../pages/Profile-Customer-Center.vue";
import CustomerInfo from "../pages/Profile-Customer-Info.vue";
import Login from "../pages/User-Login.vue";
import Register from "../pages/User-Register.vue";

const routes = [
  {path: "/", component: Welcome},
  { path: "/home", component: Home },
  { path: "/baggage/home", component: BaggageHome },
  { path: "/baggage/order", component: BaggageOrder },
  { path: "/baggage/order1", component: BaggageOrder1 },
  { path: "/employee/order", component: EmployeeOrder },
  { path: "/login", component: Login },
  { path: "/register", component: Register },

  // Profile Pages
  { path: "/customer/center", component: CustomerCenter },
  { path: "/customer/info", component: CustomerInfo }
];

export default routes;
</script>
