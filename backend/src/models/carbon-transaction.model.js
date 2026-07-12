import mongoose from "mongoose";
import { baseFields } from "./helpers/base-fields.model.js";

const carbonTransactionSchema = new mongoose.Schema(
  {
    ...baseFields,
    transactionType: { type: String, trim: true },
    sourceModule: { type: String, trim: true },
    sourceRecordId: { type: String, trim: true },
    sourceRecordType: { type: String, trim: true },
    departmentId: { type: mongoose.Schema.Types.ObjectId, ref: "Department", index: true },
    employeeId: { type: mongoose.Schema.Types.ObjectId, ref: "User", index: true },
    productId: { type: String, trim: true },
    emissionFactorId: { type: mongoose.Schema.Types.ObjectId, ref: "EmissionFactor" },
    quantity: { type: Number, required: true, min: 0 },
    unit: { type: String, required: true, trim: true },
    emissionValue: { type: Number, required: true, min: 0 },
    calculatedAt: { type: Date, default: Date.now },
    calculationMethod: { type: String, enum: ["automatic", "manual"], default: "automatic" },
    adjustmentOfTransactionId: { type: mongoose.Schema.Types.ObjectId, ref: "CarbonTransaction" },
    status: { type: String, enum: ["active", "adjusted", "void"], default: "active" },
  },
  { timestamps: true }
);

carbonTransactionSchema.index({ organizationId: 1, calculatedAt: -1 });
carbonTransactionSchema.index({ organizationId: 1, departmentId: 1, calculatedAt: -1 });

export const CarbonTransaction = mongoose.model("CarbonTransaction", carbonTransactionSchema);
