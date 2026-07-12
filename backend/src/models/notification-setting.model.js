import mongoose from "mongoose";
import { baseFields } from "./helpers/base-fields.model.js";

const notificationSettingSchema = new mongoose.Schema(
  {
    ...baseFields,
    inAppEnabled: { type: Boolean, default: true },
    emailEnabled: { type: Boolean, default: true },
    reminderSchedule: { type: String, default: "daily" },
    badgeUnlockNotifications: { type: Boolean, default: true },
    complianceNotifications: { type: Boolean, default: true },
    approvalNotifications: { type: Boolean, default: true },
    policyReminderNotifications: { type: Boolean, default: true },
    status: { type: String, enum: ["active", "inactive"], default: "active" },
  },
  { timestamps: true }
);

notificationSettingSchema.index({ organizationId: 1 }, { unique: true });

export const NotificationSetting = mongoose.model("NotificationSetting", notificationSettingSchema);
