import { FormEvent, useState } from "react";
import { createFile } from "../../../entities/file/api/fileApi";

type Options = {
  onSuccess: () => Promise<void> | void;
  onError: (message: string) => void;
};

export function useUploadFile({ onSuccess, onError }: Options) {
  const [title, setTitle] = useState("");
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);

  function reset() {
    setTitle("");
    setSelectedFile(null);
  }

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();

    if (!title.trim() || !selectedFile) {
      onError("Укажите название и выберите файл");
      return false;
    }

    setIsSubmitting(true);

    const formData = new FormData();
    formData.append("title", title.trim());
    formData.append("file", selectedFile);

    try {
      await createFile(formData);
      reset();
      await onSuccess();
      return true;
    } catch (error) {
      onError(error instanceof Error ? error.message : "Произошла ошибка");
      return false;
    } finally {
      setIsSubmitting(false);
    }
  }

  return {
    title,
    setTitle,
    selectedFile,
    setSelectedFile,
    isSubmitting,
    reset,
    handleSubmit,
  };
}
