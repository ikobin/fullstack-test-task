import { API_URL } from "../config";

export class ApiError extends Error {
  constructor(message: string) {
    super(message);
    this.name = "ApiError";
  }
}

export async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(`${API_URL}${path}`, {
    cache: "no-store",
    ...init,
  });

  if (!response.ok) {
    throw new ApiError("Не удалось выполнить запрос");
  }

  if (response.status === 204) {
    return undefined as T;
  }

  return (await response.json()) as T;
}

export function downloadUrl(fileId: string): string {
  return `${API_URL}/files/${fileId}/download`;
}
