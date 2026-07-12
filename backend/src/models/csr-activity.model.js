import mongoose from "mongoose";
import { baseFields } from "./helpers/base-fields.model.js";

const csrActivitySchema = new mongoose.Schema(
  {
    ...baseFields,
    title: { type: String, required: true, trim: true },
    categoryId: { type: mongoose.Schema.Types.ObjectId, ref: "Category" },
    description: { type: String, trim: true },
    location: { type: String, trim: true },
    activityDate: { type: Date, required: true },
    ownerUserId: { type: mongoose.Schema.Types.ObjectId, ref: "User" },
    capacity: { type: Number, min: 0 },
    evidenceRequired: { type: Boolean, default: false },
    status: { type: String, enum: ["draft", "active", "completed", "archived"], default: "draft" },
  },
  { timestamps: true }
);

csrActivitySchema.index({ organizationId: 1, activityDate: -1 });

export const CSRActivity = mongoose.model("CSRActivity", csrActivitySchema);
