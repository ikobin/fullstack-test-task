"use client";

import { useState } from "react";
import { Alert, Button, Card, Col, Container, Row } from "react-bootstrap";
import { UploadFileModal } from "../../../features/upload-file/ui/UploadFileModal";
import { useFileManager } from "../model/useFileManager";
import { AlertTable } from "./AlertTable";
import { FileTable } from "./FileTable";

export function FileManager() {
  const { files, alerts, isLoading, errorMessage, setErrorMessage, loadData } = useFileManager();
  const [showModal, setShowModal] = useState(false);

  return (
    <Container fluid className="py-4 px-4 bg-light min-vh-100">
      <Row className="justify-content-center">
        <Col xxl={10} xl={11}>
          <Card className="shadow-sm border-0 mb-4">
            <Card.Body className="p-4">
              <div className="d-flex justify-content-between align-items-start gap-3 flex-wrap">
                <div>
                  <h1 className="h3 mb-2">Управление файлами</h1>
                  <p className="text-secondary mb-0">
                    Загрузка файлов, просмотр статусов обработки и ленты алертов.
                  </p>
                </div>
                <div className="d-flex gap-2">
                  <Button variant="outline-secondary" onClick={() => void loadData()}>
                    Обновить
                  </Button>
                  <Button variant="primary" onClick={() => setShowModal(true)}>
                    Добавить файл
                  </Button>
                </div>
              </div>
            </Card.Body>
          </Card>

          {errorMessage ? (
            <Alert variant="danger" className="shadow-sm">
              {errorMessage}
            </Alert>
          ) : null}

          <FileTable files={files} isLoading={isLoading} />
          <AlertTable alerts={alerts} isLoading={isLoading} />
        </Col>
      </Row>

      <UploadFileModal
        show={showModal}
        onHide={() => setShowModal(false)}
        onUploaded={() => loadData(true)}
        onError={setErrorMessage}
      />
    </Container>
  );
}
