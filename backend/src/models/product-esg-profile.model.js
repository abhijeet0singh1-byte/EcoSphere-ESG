import mongoose from "mongoose";
import { baseFields } from "./helpers/base-fields.model.js";

const productESGProfileSchema = new mongoose.Schema(
  {
    ...baseFields,
    productId: { type: String, required: true, trim: true },
    productName: { type: String, required: true, trim: true },
    categoryId: { type: mongoose.Schema.Types.ObjectId, ref: "Category" },
    emissionFactorId: { type: mongoose.Schema.Types.ObjectId, ref: "EmissionFactor" },
    packagingType: { type: String, trim: true },
    recyclable: { type: Boolean, default: false },
    sustainabilityAttributes: { type: mongoose.Schema.Types.Mixed, default: {} },
    status: { type: String, enum: ["active", "inactive"], default: "active" },
  },
  { timestamps: true }
);

productESGProfileSchema.index({ organizationId: 1, productId: 1 }, { unique: true });

export const ProductESGProfile = mongoose.model("ProductESGProfile", productESGProfileSchema);
