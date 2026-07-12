import mongoose from "mongoose";
import { baseFields } from "./helpers/base-fields.model.js";

const organizationScoreSchema = new mongoose.Schema(
  {
    ...baseFields,
    environmentalWeight: { type: Number, default: 40 },
    socialWeight: { type: Number, default: 30 },
    governanceWeight: { type: Number, default: 30 },
    environmentalScore: { type: Number, default: 0 },
    socialScore: { type: Number, default: 0 },
    governanceScore: { type: Number, default: 0 },
    totalScore: { type: Number, default: 0 },
    scoreDate: { type: Date, default: Date.now },
    status: { type: String, enum: ["final", "draft"], default: "final" },
  },
  { timestamps: true }
);

organizationScoreSchema.index({ organizationId: 1, scoreDate: -1 });

export const OrganizationScore = mongoose.model("OrganizationScore", organizationScoreSchema);
