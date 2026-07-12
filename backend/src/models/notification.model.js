import mongoose from "mongoose";
import { baseFields } from "./helpers/base-fields.model.js";

const notificationSchema = new mongoose.Schema(
  {
    ...baseFields,
    recipientUserId: { type: mongoose.Schema.Types.ObjectId, ref: "User", required: true, index: true },
    type: { type: String, required: true, trim: true },
    title: { type: String, required: true, trim: true },
    message: { type: String, required: true, trim: true },
    entityType: { type: String, trim: true },
    entityId: { type: String, trim: true },
    channel: { type: String, enum: ["in_app", "email"], default: "in_app" },
    readAt: { type: Date },
    sentAt: { type: Date },
    deliveryStatus: { type: String, enum: ["pending", "sent", "failed"], default: "pending" },
    status: { type: String, enum: ["active", "archived"], default: "active" },
  },
  { timestamps: true }
);

notificationSchema.index({ organizationId: 1, recipientUserId: 1, createdAt: -1 });

export const Notification = mongoose.model("Notification", notificationSchema);
