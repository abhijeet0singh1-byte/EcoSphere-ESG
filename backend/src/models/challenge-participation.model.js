import mongoose from "mongoose";
import { baseFields } from "./helpers/base-fields.model.js";

const proofSchema = new mongoose.Schema(
  {
    fileName: String,
    url: String,
  },
  { _id: false }
);

const challengeParticipationSchema = new mongoose.Schema(
  {
    ...baseFields,
    challengeId: { type: mongoose.Schema.Types.ObjectId, ref: "Challenge", required: true, index: true },
    employeeId: { type: mongoose.Schema.Types.ObjectId, ref: "User", required: true, index: true },
    progress: { type: Number, default: 0, min: 0, max: 100 },
    proofFiles: { type: [proofSchema], default: [] },
    approvalStatus: { type: String, enum: ["pending", "approved", "rejected"], default: "pending" },
    xpAwarded: { type: Number, default: 0, min: 0 },
    approvedBy: { type: mongoose.Schema.Types.ObjectId, ref: "User" },
    approvedAt: { type: Date },
    completionDate: { type: Date },
    status: { type: String, enum: ["active", "archived"], default: "active" },
  },
  { timestamps: true }
);

challengeParticipationSchema.index({ organizationId: 1, challengeId: 1, employeeId: 1 }, { unique: true });

export const ChallengeParticipation = mongoose.model("ChallengeParticipation", challengeParticipationSchema);
