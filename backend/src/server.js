import dotenv from "dotenv";
import app from "./app.js";
import connectDB from "./db/index.db.js";

dotenv.config();

const port = process.env.PORT || 3000;

const startServer = async () => {
	await connectDB();

	app.listen(port, () => {
		console.log(`Server running on port ${port}`);
	});
};

startServer();
