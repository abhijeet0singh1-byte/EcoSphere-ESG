import mongoose from "mongoose";
import { baseFields } from "./helpers/base-fields.model.js";

const emissionFactorSchema = new mongoose.Schema(
  {
    ...baseFields,
    name: { type: String, required: true, trim: true },
    sourceType: {
      type: String,
      enum: ["purchase", "manufacturing", "expense", "fleet", "manual"],
      required: true,
    },
    unit: { type: String, required: true, trim: true },
    factorValue: { type: Number, required: true, min: 0 },
    validFrom: { type: Date },
    validTo: { type: Date },
    metadata: { type: mongoose.Schema.Types.Mixed, default: {} },
    status: { type: String, enum: ["active", "inactive"], default: "active" },
  },
  { timestamps: true }
);

emissionFactorSchema.index({ organizationId: 1, sourceType: 1, name: 1 }, { unique: true });

export const EmissionFactor = mongoose.model("EmissionFactor", emissionFactorSchema);
