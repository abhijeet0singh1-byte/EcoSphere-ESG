import mongoose from "mongoose";
import { baseFields } from "./helpers/base-fields.model.js";

const policyAcknowledgementSchema = new mongoose.Schema(
  {
    ...baseFields,
    policyId: { type: mongoose.Schema.Types.ObjectId, ref: "ESGPolicy", required: true },
    employeeId: { type: mongoose.Schema.Types.ObjectId, ref: "User", required: true },
    acknowledgedAt: { type: Date },
    policyVersion: { type: String, required: true, trim: true },
    reminderCount: { type: Number, default: 0, min: 0 },
    lastReminderAt: { type: Date },
    status: { type: String, enum: ["pending", "acknowledged", "overdue"], default: "pending" },
  },
  { timestamps: true }
);

policyAcknowledgementSchema.index(
  { organizationId: 1, policyId: 1, employeeId: 1, policyVersion: 1 },
  { unique: true }
);

export const PolicyAcknowledgement = mongoose.model("PolicyAcknowledgement", policyAcknowledgementSchema);
