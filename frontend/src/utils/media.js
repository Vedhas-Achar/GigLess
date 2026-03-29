const API_ORIGIN = 'http://localhost:8000'

export function resolveMediaUrl(path) {
  if (!path) return ''
  if (path.startsWith('http://') || path.startsWith('https://')) return path
  if (path.startsWith('/')) return `${API_ORIGIN}${path}`
  return `${API_ORIGIN}/${path}`
}
