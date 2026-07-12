import mongoose from "mongoose";

const connectDB = async () => {
  try {
    const connectionInstance = await mongoose.connect(process.env.MONGO_URI);
    if(connectionInstance.connection.readyState === 1) {
      console.log("MongoDB connected successfully");
    } else {
      console.log("MongoDB connection failed");
    }
  } catch (error) {
    console.log(`Error: ${error.message}`);
    process.exit(1);
  }
};

export default connectDB;