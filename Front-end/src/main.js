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

applyTheme(readStoredTheme());


if (window.location.pathname === "/") {
    window.history.replaceState({}, "", "/home");
}

const router = defineRoutes([
  {path: "/", element: () => {location.pathname = "/home" ; return ""}},
  {path: "/home", element: HomePage},
  {path: "/contattaci", element: ContactPage}
])


createRoot(
  "app",
  jd.router(router),
);

