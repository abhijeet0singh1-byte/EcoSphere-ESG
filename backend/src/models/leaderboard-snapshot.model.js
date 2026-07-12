import mongoose from "mongoose";
import { baseFields } from "./helpers/base-fields.model.js";

const leaderboardSnapshotSchema = new mongoose.Schema(
  {
    ...baseFields,
    leaderboardType: { type: String, required: true, trim: true },
    departmentId: { type: mongoose.Schema.Types.ObjectId, ref: "Department" },
    employeeId: { type: mongoose.Schema.Types.ObjectId, ref: "User" },
    rank: { type: Number, required: true, min: 1 },
    score: { type: Number, default: 0 },
    xp: { type: Number, default: 0 },
    snapshotDate: { type: Date, default: Date.now },
    period: { type: String, trim: true },
    status: { type: String, enum: ["active", "archived"], default: "active" },
  },
  { timestamps: true }
);

leaderboardSnapshotSchema.index({ organizationId: 1, leaderboardType: 1, snapshotDate: -1 });

export const LeaderboardSnapshot = mongoose.model("LeaderboardSnapshot", leaderboardSnapshotSchema);
