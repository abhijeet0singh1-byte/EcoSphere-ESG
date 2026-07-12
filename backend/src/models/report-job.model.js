import mongoose from "mongoose";
import { baseFields } from "./helpers/base-fields.model.js";

const reportJobSchema = new mongoose.Schema(
  {
    ...baseFields,
    reportType: { type: String, required: true, trim: true },
    filters: { type: mongoose.Schema.Types.Mixed, default: {} },
    requestedBy: { type: mongoose.Schema.Types.ObjectId, ref: "User" },
    exportFormat: { type: String, enum: ["pdf", "excel", "csv"], required: true },
    fileUrl: { type: String, trim: true },
    jobStatus: { type: String, enum: ["queued", "running", "completed", "failed"], default: "queued" },
    startedAt: { type: Date },
    completedAt: { type: Date },
    status: { type: String, enum: ["active", "archived"], default: "active" },
  },
  { timestamps: true }
);

reportJobSchema.index({ organizationId: 1, jobStatus: 1, createdAt: -1 });

export const ReportJob = mongoose.model("ReportJob", reportJobSchema);
