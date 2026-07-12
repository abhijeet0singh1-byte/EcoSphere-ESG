import mongoose from "mongoose";
import { baseFields } from "./helpers/base-fields.model.js";

const departmentSchema = new mongoose.Schema(
  {
    ...baseFields,
    code: { type: String, required: true, trim: true },
    name: { type: String, required: true, trim: true },
    parentDepartmentId: { type: mongoose.Schema.Types.ObjectId, ref: "Department" },
    headUserId: { type: mongoose.Schema.Types.ObjectId, ref: "User" },
    employeeCount: { type: Number, default: 0, min: 0 },
    status: { type: String, enum: ["active", "inactive"], default: "active" },
  },
  { timestamps: true }
);

departmentSchema.index({ organizationId: 1, code: 1 }, { unique: true });
departmentSchema.index({ organizationId: 1, parentDepartmentId: 1 });

export const Department = mongoose.model("Department", departmentSchema);
