let session = null;
const listeners = new Set();

export function getSession() {
  return session;
}

export function setSession(user) {
  session = user;
  listeners.forEach((fn) => fn(session));
}

export function clearSession() {
  session = null;
  listeners.forEach((fn) => fn(session));
}

export function onSessionChange(fn) {
  listeners.add(fn);
  return () => listeners.delete(fn);
}
