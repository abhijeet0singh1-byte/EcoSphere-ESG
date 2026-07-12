import mongoose from "mongoose";
import { baseFields } from "./helpers/base-fields.model.js";

const departmentScoreSchema = new mongoose.Schema(
  {
    ...baseFields,
    departmentId: { type: mongoose.Schema.Types.ObjectId, ref: "Department", required: true },
    environmentalScore: { type: Number, default: 0 },
    socialScore: { type: Number, default: 0 },
    governanceScore: { type: Number, default: 0 },
    totalScore: { type: Number, default: 0 },
    scoreDate: { type: Date, default: Date.now },
    scorePeriod: { type: String, trim: true },
    status: { type: String, enum: ["final", "draft"], default: "final" },
  },
  { timestamps: true }
);

departmentScoreSchema.index({ organizationId: 1, departmentId: 1, scoreDate: -1 });

export const DepartmentScore = mongoose.model("DepartmentScore", departmentScoreSchema);
