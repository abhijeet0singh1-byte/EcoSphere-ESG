import mongoose from "mongoose";
import { baseFields } from "./helpers/base-fields.model.js";

const environmentalGoalSchema = new mongoose.Schema(
  {
    ...baseFields,
    title: { type: String, required: true, trim: true },
    description: { type: String, trim: true },
    metricType: { type: String, required: true, trim: true },
    targetValue: { type: Number, required: true },
    unit: { type: String, required: true, trim: true },
    startDate: { type: Date },
    endDate: { type: Date },
    ownerDepartmentId: { type: mongoose.Schema.Types.ObjectId, ref: "Department" },
    progressValue: { type: Number, default: 0 },
    status: { type: String, enum: ["draft", "active", "completed", "archived"], default: "draft" },
  },
  { timestamps: true }
);

environmentalGoalSchema.index({ organizationId: 1, status: 1 });

export const EnvironmentalGoal = mongoose.model("EnvironmentalGoal", environmentalGoalSchema);
