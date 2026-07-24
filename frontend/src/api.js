import { readString, removeValue, writeString } from './utils/storage';

export const API_OVERRIDE_KEY = 'quotation-ai/api-base-url';
// Use the current IP/Hostname where the frontend is loaded, so it works seamlessly on mobile over Wi-Fi
export const DEFAULT_API_BASE = 'https://quotation-ai-backend-dn5t.onrender.com';

const normalizeBase = (value) => String(value || '').trim().replace(/\/+$/, '');

export function getApiBase() {
  const fromStorage = normalizeBase(readString(API_OVERRIDE_KEY, ''));
  if (fromStorage) return fromStorage;

  const isElectron =
    typeof window !== 'undefined' &&
    (window.location.protocol === 'file:' ||
      (window.navigator && window.navigator.userAgent && window.navigator.userAgent.includes('Electron')) ||
      Boolean(window.desktopApp && window.desktopApp.isDesktop));

  if (isElectron) {
    return 'http://127.0.0.1:8000';
  }

  const fromEnv = normalizeBase(process.env.REACT_APP_API_URL || '');
  return fromEnv || DEFAULT_API_BASE;
}

export function hasApiBaseOverride() {
  return Boolean(normalizeBase(readString(API_OVERRIDE_KEY, '')));
}

export function setApiBaseOverride(nextBase) {
  const normalized = normalizeBase(nextBase);
  if (!normalized) {
    removeValue(API_OVERRIDE_KEY);
    return '';
  }
  writeString(API_OVERRIDE_KEY, normalized);
  return normalized;
}

export function clearApiBaseOverride() {
  removeValue(API_OVERRIDE_KEY);
}

const BASE = getApiBase();

export default BASE;

