import mongoose from "mongoose";
import { baseFields } from "./helpers/base-fields.model.js";

const badgeSchema = new mongoose.Schema(
  {
    ...baseFields,
    name: { type: String, required: true, trim: true },
    description: { type: String, trim: true },
    icon: { type: String, trim: true },
    unlockRuleType: { type: String, required: true, trim: true },
    unlockRuleValue: { type: Number, default: 0 },
    unlockRuleJson: { type: mongoose.Schema.Types.Mixed, default: {} },
    xpThreshold: { type: Number, default: 0 },
    completedChallengesThreshold: { type: Number, default: 0 },
    status: { type: String, enum: ["active", "inactive"], default: "active" },
  },
  { timestamps: true }
);

badgeSchema.index({ organizationId: 1, name: 1 }, { unique: true });

export const Badge = mongoose.model("Badge", badgeSchema);
