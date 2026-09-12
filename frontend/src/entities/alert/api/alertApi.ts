import { request } from "../../../shared/api/http";
import type { AlertItem } from "../model/types";

export function listAlerts() {
  return request<AlertItem[]>("/alerts");
}
