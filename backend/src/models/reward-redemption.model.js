import mongoose from "mongoose";
import { baseFields } from "./helpers/base-fields.model.js";

const rewardRedemptionSchema = new mongoose.Schema(
  {
    ...baseFields,
    rewardId: { type: mongoose.Schema.Types.ObjectId, ref: "Reward", required: true },
    employeeId: { type: mongoose.Schema.Types.ObjectId, ref: "User", required: true },
    pointsSpent: { type: Number, required: true, min: 0 },
    quantity: { type: Number, required: true, min: 1 },
    redemptionCode: { type: String, trim: true, index: true },
    status: {
      type: String,
      enum: ["pending", "approved", "fulfilled", "cancelled", "rejected"],
      default: "pending",
    },
    redeemedAt: { type: Date, default: Date.now },
    fulfilledAt: { type: Date },
  },
  { timestamps: true }
);

rewardRedemptionSchema.index({ organizationId: 1, employeeId: 1, redeemedAt: -1 });

export const RewardRedemption = mongoose.model("RewardRedemption", rewardRedemptionSchema);
