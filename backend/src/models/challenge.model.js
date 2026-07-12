import mongoose from "mongoose";
import { baseFields } from "./helpers/base-fields.model.js";

const challengeSchema = new mongoose.Schema(
  {
    ...baseFields,
    title: { type: String, required: true, trim: true },
    categoryId: { type: mongoose.Schema.Types.ObjectId, ref: "Category" },
    description: { type: String, trim: true },
    xpReward: { type: Number, default: 0, min: 0 },
    difficulty: { type: String, enum: ["easy", "medium", "hard"], default: "medium" },
    evidenceRequired: { type: Boolean, default: false },
    deadline: { type: Date },
    lifecycleStatus: {
      type: String,
      enum: ["draft", "active", "under_review", "completed", "archived"],
      default: "draft",
    },
    archivedAt: { type: Date },
    ownerUserId: { type: mongoose.Schema.Types.ObjectId, ref: "User" },
    status: { type: String, enum: ["active", "inactive"], default: "active" },
  },
  { timestamps: true }
);

challengeSchema.index({ organizationId: 1, lifecycleStatus: 1, deadline: 1 });

export const Challenge = mongoose.model("Challenge", challengeSchema);
