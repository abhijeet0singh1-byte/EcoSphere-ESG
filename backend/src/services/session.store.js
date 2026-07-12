import crypto from "crypto";

const SESSION_TTL_MS = 1000 * 60 * 60 * 24; // 24 hours
const sessions = new Map();

export const createSession = (userId) => {
  const sessionId = crypto.randomBytes(32).toString("hex");
  sessions.set(sessionId, {
    userId,
    createdAt: Date.now(),
  });

  return sessionId;
};

export const getSession = (sessionId) => {
  const session = sessions.get(sessionId);
  if (!session) {
    return null;
  }

  const expired = Date.now() - session.createdAt > SESSION_TTL_MS;
  if (expired) {
    sessions.delete(sessionId);
    return null;
  }

  return session;
};

export const deleteSession = (sessionId) => {
  if (!sessionId) {
    return false;
  }

  return sessions.delete(sessionId);
};
