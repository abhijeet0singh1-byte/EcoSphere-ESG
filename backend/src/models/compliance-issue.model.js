import mongoose from "mongoose";
import { baseFields } from "./helpers/base-fields.model.js";

const complianceIssueSchema = new mongoose.Schema(
  {
    ...baseFields,
    auditId: { type: mongoose.Schema.Types.ObjectId, ref: "Audit", required: true },
    title: { type: String, required: true, trim: true },
    severity: { type: String, enum: ["low", "medium", "high", "critical"], default: "medium" },
    description: { type: String, trim: true },
    ownerUserId: { type: mongoose.Schema.Types.ObjectId, ref: "User", required: true },
    dueDate: { type: Date, required: true },
    status: { type: String, enum: ["open", "in_review", "resolved", "closed", "overdue"], default: "open" },
    overdueFlag: { type: Boolean, default: false },
    resolvedAt: { type: Date },
    resolutionNotes: { type: String, trim: true },
  },
  { timestamps: true }
);

complianceIssueSchema.index({ organizationId: 1, status: 1, dueDate: 1 });
complianceIssueSchema.index({ organizationId: 1, ownerUserId: 1 });

export const ComplianceIssue = mongoose.model("ComplianceIssue", complianceIssueSchema);
