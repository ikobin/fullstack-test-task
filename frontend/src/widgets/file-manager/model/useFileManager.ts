import { useCallback, useEffect, useState } from "react";
import { listAlerts } from "../../../entities/alert/api/alertApi";
import type { AlertItem } from "../../../entities/alert/model/types";
import { listFiles } from "../../../entities/file/api/fileApi";
import type { FileItem } from "../../../entities/file/model/types";

function isPending(file: FileItem) {
  return file.processing_status === "uploaded" || file.processing_status === "processing";
}

export function useFileManager() {
  const [files, setFiles] = useState<FileItem[]>([]);
  const [alerts, setAlerts] = useState<AlertItem[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);

  const loadData = useCallback(async (silent = false) => {
    if (!silent) {
      setIsLoading(true);
    }
    setErrorMessage(null);

    try {
      const [filesData, alertsData] = await Promise.all([listFiles(), listAlerts()]);
      setFiles(filesData);
      setAlerts(alertsData);
    } catch (error) {
      setErrorMessage(error instanceof Error ? error.message : "Произошла ошибка");
    } finally {
      if (!silent) {
        setIsLoading(false);
      }
    }
  }, []);

  useEffect(() => {
    void loadData();
  }, [loadData]);

  useEffect(() => {
    if (!files.some(isPending)) {
      return;
    }

    const timer = window.setInterval(() => {
      void loadData(true);
    }, 3000);

    return () => window.clearInterval(timer);
  }, [files, loadData]);

  return {
    files,
    alerts,
    isLoading,
    errorMessage,
    setErrorMessage,
    loadData,
  };
}
