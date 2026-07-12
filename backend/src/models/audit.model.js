import mongoose from "mongoose";
import { baseFields } from "./helpers/base-fields.model.js";

const auditSchema = new mongoose.Schema(
  {
    ...baseFields,
    title: { type: String, required: true, trim: true },
    auditType: { type: String, trim: true },
    startDate: { type: Date },
    endDate: { type: Date },
    auditorUserId: { type: mongoose.Schema.Types.ObjectId, ref: "User" },
    departmentId: { type: mongoose.Schema.Types.ObjectId, ref: "Department" },
    status: { type: String, enum: ["open", "in_progress", "closed", "archived"], default: "open" },
    findingsSummary: { type: String, trim: true },
  },
  { timestamps: true }
);

auditSchema.index({ organizationId: 1, status: 1, endDate: 1 });

export const Audit = mongoose.model("Audit", auditSchema);
