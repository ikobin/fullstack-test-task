import { request } from "../../../shared/api/http";
import type { FileItem } from "../model/types";

export function listFiles() {
  return request<FileItem[]>("/files");
}

export function createFile(formData: FormData) {
  return request<FileItem>("/files", {
    method: "POST",
    body: formData,
  });
}
