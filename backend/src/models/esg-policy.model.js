import mongoose from "mongoose";
import { baseFields } from "./helpers/base-fields.model.js";

const esgPolicySchema = new mongoose.Schema(
  {
    ...baseFields,
    title: { type: String, required: true, trim: true },
    policyCode: { type: String, required: true, trim: true },
    version: { type: String, required: true, trim: true },
    category: { type: String, trim: true },
    effectiveDate: { type: Date },
    expiryDate: { type: Date },
    documentUrl: { type: String, trim: true },
    acknowledgementRequired: { type: Boolean, default: true },
    status: { type: String, enum: ["draft", "published", "archived"], default: "draft" },
  },
  { timestamps: true }
);

esgPolicySchema.index({ organizationId: 1, policyCode: 1 }, { unique: true });

export const ESGPolicy = mongoose.model("ESGPolicy", esgPolicySchema);
