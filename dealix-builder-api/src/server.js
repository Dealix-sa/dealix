import "dotenv/config";
import express from "express";
import { builderRouter } from "./routes/builder.js";

const app = express();
app.use(express.json({ limit: "4mb" }));

app.get("/", (req, res) => {
  res.json({
    ok: true,
    name: "Dealix API-First Builder",
    endpoints: ["/builder/health", "/builder/plan", "/builder/founder-brief"]
  });
});

app.use("/builder", builderRouter);

app.use((err, req, res, next) => {
  res.status(500).json({
    ok: false,
    error: err.message || "Unknown error"
  });
});

const port = Number(process.env.PORT || 8787);
app.listen(port, () => {
  console.log(`Dealix Builder API running on http://localhost:${port}`);
});
