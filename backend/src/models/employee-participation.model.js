import mongoose from "mongoose";
import { baseFields } from "./helpers/base-fields.model.js";

const proofSchema = new mongoose.Schema(
  {
    fileName: String,
    url: String,
  },
  { _id: false }
);

const employeeParticipationSchema = new mongoose.Schema(
  {
    ...baseFields,
    employeeId: { type: mongoose.Schema.Types.ObjectId, ref: "User", required: true, index: true },
    csrActivityId: { type: mongoose.Schema.Types.ObjectId, ref: "CSRActivity", required: true, index: true },
    proofFiles: { type: [proofSchema], default: [] },
    approvalStatus: { type: String, enum: ["pending", "approved", "rejected"], default: "pending" },
    pointsEarned: { type: Number, default: 0, min: 0 },
    approvedBy: { type: mongoose.Schema.Types.ObjectId, ref: "User" },
    approvedAt: { type: Date },
    completionDate: { type: Date },
    status: { type: String, enum: ["active", "archived"], default: "active" },
  },
  { timestamps: true }
);

employeeParticipationSchema.index({ organizationId: 1, employeeId: 1, csrActivityId: 1 }, { unique: true });

export const EmployeeParticipation = mongoose.model("EmployeeParticipation", employeeParticipationSchema);
