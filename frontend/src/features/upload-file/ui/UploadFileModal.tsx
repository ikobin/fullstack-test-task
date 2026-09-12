"use client";

import { Button, Form, Modal } from "react-bootstrap";
import { useUploadFile } from "../model/useUploadFile";

type Props = {
  show: boolean;
  onHide: () => void;
  onUploaded: () => Promise<void> | void;
  onError: (message: string) => void;
};

export function UploadFileModal({ show, onHide, onUploaded, onError }: Props) {
  const { title, setTitle, setSelectedFile, isSubmitting, reset, handleSubmit } = useUploadFile({
    onSuccess: onUploaded,
    onError,
  });

  function handleClose() {
    reset();
    onHide();
  }

  return (
    <Modal show={show} onHide={handleClose} centered>
      <Form
        onSubmit={async (event) => {
          const uploaded = await handleSubmit(event);
          if (uploaded) {
            onHide();
          }
        }}
      >
        <Modal.Header closeButton>
          <Modal.Title>Добавить файл</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <Form.Group className="mb-3">
            <Form.Label>Название</Form.Label>
            <Form.Control
              value={title}
              onChange={(event) => setTitle(event.target.value)}
              placeholder="Например, Договор с подрядчиком"
            />
          </Form.Group>
          <Form.Group>
            <Form.Label>Файл</Form.Label>
            <Form.Control
              type="file"
              onChange={(event) =>
                setSelectedFile((event.target as HTMLInputElement).files?.[0] ?? null)
              }
            />
          </Form.Group>
        </Modal.Body>
        <Modal.Footer>
          <Button variant="outline-secondary" onClick={handleClose}>
            Отмена
          </Button>
          <Button type="submit" variant="primary" disabled={isSubmitting}>
            {isSubmitting ? "Загрузка..." : "Сохранить"}
          </Button>
        </Modal.Footer>
      </Form>
    </Modal>
  );
}
