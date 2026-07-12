import mongoose from "mongoose";
import { baseFields } from "./helpers/base-fields.model.js";

const categorySchema = new mongoose.Schema(
  {
    ...baseFields,
    name: { type: String, required: true, trim: true },
    type: { type: String, enum: ["CSR Activity", "Challenge"], required: true },
    description: { type: String, trim: true },
    color: { type: String, trim: true },
    status: { type: String, enum: ["active", "inactive"], default: "active" },
  },
  { timestamps: true }
);

categorySchema.index({ organizationId: 1, type: 1, name: 1 }, { unique: true });

export const Category = mongoose.model("Category", categorySchema);
