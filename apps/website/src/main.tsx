import React from "react";
import { createRoot } from "react-dom/client";
import "./index.css";
import { DealixWebsite } from "./pages/public/DealixWebsite";

createRoot(document.getElementById("root")!).render(
  <React.StrictMode>
    <DealixWebsite />
  </React.StrictMode>
);
