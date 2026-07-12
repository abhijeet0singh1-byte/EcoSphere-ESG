import mongoose from "mongoose";
import { baseFields } from "./helpers/base-fields.model.js";

const rewardSchema = new mongoose.Schema(
  {
    ...baseFields,
    name: { type: String, required: true, trim: true },
    description: { type: String, trim: true },
    pointsRequired: { type: Number, default: 0, min: 0 },
    xpRequired: { type: Number, default: 0, min: 0 },
    stock: { type: Number, required: true, min: 0 },
    imageUrl: { type: String, trim: true },
    redemptionLimitPerEmployee: { type: Number, default: 1, min: 1 },
    status: { type: String, enum: ["active", "inactive"], default: "active" },
  },
  { timestamps: true }
);

rewardSchema.index({ organizationId: 1, name: 1 }, { unique: true });

export const Reward = mongoose.model("Reward", rewardSchema);
