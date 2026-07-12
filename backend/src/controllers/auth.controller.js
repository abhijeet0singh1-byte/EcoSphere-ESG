import { User } from "../models/user.model.js";
import { createSession, deleteSession } from "../services/session.store.js";

const sessionCookieOptions = {
  httpOnly: true,
  sameSite: "lax",
  secure: process.env.NODE_ENV === "production",
  maxAge: 1000 * 60 * 60 * 24,
};

export const login = async (req, res) => {
  const { email, password } = req.body;

  if (!email || !password) {
    return res.status(400).json({ message: "Email and password are required" });
  }

  const user = await User.findOne({ email: email.toLowerCase(), status: "active" }).select("+password");

  if (!user) {
    return res.status(401).json({ message: "Invalid credentials" });
  }

  const isValidPassword = await user.isPasswordCorrect(password);
  if (!isValidPassword) {
    return res.status(401).json({ message: "Invalid credentials" });
  }

  const sessionId = createSession(user._id.toString());
  res.cookie("sessionId", sessionId, sessionCookieOptions);

  return res.status(200).json({
    message: "Login successful",
    user: {
      id: user._id,
      fullName: user.fullName,
      email: user.email,
      role: user.role,
      organizationId: user.organizationId,
    },
  });
};

export const logout = async (req, res) => {
  const { sessionId } = req.cookies;
  deleteSession(sessionId);

  res.clearCookie("sessionId", sessionCookieOptions);
  return res.status(200).json({ message: "Logout successful" });
};
