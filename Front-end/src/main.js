import "./style.css";
import { createRoot } from "just-dom";
import { jd } from "./jd.config.js";
import {
  applyTheme,
  readStoredTheme,
  themeToggleButton,
} from "./components/theme-toggle";
import { HomeHeader } from "./components/home-header.js";
import { defineRoutes } from "@just-dom/router";
import { navigate } from "@just-dom/router";
import { HomePage } from "./pages/home-page.js";
import { ContactPage } from "./pages/contact-page.js";
import { LoginPage } from "./pages/login-page.js";
import { RegisterPage } from "./pages/register-page.js";
import { NotFoundPage } from "./pages/not-found-page.js";
import { UserPage } from "./pages/user-page.js";

applyTheme(readStoredTheme());


if (window.location.pathname === "/") {
    window.history.replaceState({}, "", "/home");
}

const router = defineRoutes([
  {path: "/", element: () => {location.pathname = "/home" ; return ""}},
  {path: "/home", element: HomePage},
  {path: "/contattaci", element: ContactPage},
  {path: "/register", element: RegisterPage},
  {path: "/login", element: LoginPage},
  {path: "/users/:user_id", element: UserPage},
  {path: "*", element: NotFoundPage},
])


createRoot(
  "app",
  jd.router(router),
);

