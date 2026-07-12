import mongoose from "mongoose";
import { baseFields } from "./helpers/base-fields.model.js";

const auditLogSchema = new mongoose.Schema(
  {
    ...baseFields,
    actorUserId: { type: mongoose.Schema.Types.ObjectId, ref: "User" },
    action: { type: String, required: true, trim: true },
    entityType: { type: String, required: true, trim: true },
    entityId: { type: String, required: true, trim: true },
    payload: { type: mongoose.Schema.Types.Mixed, default: {} },
    ipAddress: { type: String, trim: true },
    userAgent: { type: String, trim: true },
    status: { type: String, enum: ["active", "archived"], default: "active" },
    createdAt: { type: Date, default: Date.now },
  },
  { timestamps: false }
);

auditLogSchema.index({ organizationId: 1, entityType: 1, entityId: 1, createdAt: -1 });

export const AuditLog = mongoose.model("AuditLog", auditLogSchema);
