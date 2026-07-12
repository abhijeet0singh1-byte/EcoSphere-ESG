import mongoose from "mongoose";

const attachmentSchema = new mongoose.Schema(
  {
    fileName: String,
    url: String,
    mimeType: String,
    size: Number,
  },
  { _id: false }
);

export const baseFields = {
  organizationId: {
    type: mongoose.Schema.Types.ObjectId,
    required: true,
    index: true,
    ref: "Organization",
  },
  createdBy: {
    type: mongoose.Schema.Types.ObjectId,
    ref: "User",
  },
  updatedBy: {
    type: mongoose.Schema.Types.ObjectId,
    ref: "User",
  },
  notes: {
    type: String,
    trim: true,
  },
  attachments: {
    type: [attachmentSchema],
    default: [],
  },
};
