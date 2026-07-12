import mongoose from "mongoose";
import { baseFields } from "./helpers/base-fields.model.js";

const organizationSettingSchema = new mongoose.Schema(
  {
    ...baseFields,
    organizationName: { type: String, required: true, trim: true },
    scoringWeights: {
      environmental: { type: Number, default: 40 },
      social: { type: Number, default: 30 },
      governance: { type: Number, default: 30 },
    },
    autoEmissionCalculationEnabled: { type: Boolean, default: true },
    evidenceRequirementEnabled: { type: Boolean, default: false },
    badgeAutoAwardEnabled: { type: Boolean, default: true },
    defaultCurrency: { type: String, default: "USD" },
    locale: { type: String, default: "en" },
    timezone: { type: String, default: "UTC" },
  },
  { timestamps: true }
);

organizationSettingSchema.index({ organizationId: 1 }, { unique: true });

export const OrganizationSetting = mongoose.model("OrganizationSetting", organizationSettingSchema);
