import express from "express";
import { connect } from "./db";

connect();

const app = express();

app.use(morgan("dev"));

app.use(express.json());
app.use(cookieParser());

app.use("/api/auth", authRouter);
app.use("/api/user", userRouter);
app.use("/api/survey", surveyAnswersRouter);
app.use("/api/diary", foodDiaryRouter);

app.listen(process.env.PORT || 5000, () => console.log("server started"));
