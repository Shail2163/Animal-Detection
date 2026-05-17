import React, { useState } from 'react';
import ImageUpload from './ImageUpload';
import './App.css';

function App() {
  const [detectionResult, setDetectionResult] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleDetectionComplete = (result) => {
    setDetectionResult(result);
    setIsLoading(false);
    setError(null);
  };

  const handleDetectionError = (error) => {
    setError(error);
    setIsLoading(false);
    setDetectionResult(null);
  };

  const handleDetectionStart = () => {
    setIsLoading(true);
    setError(null);
    setDetectionResult(null);
  };

  const handleReset = () => {
    setDetectionResult(null);
    setError(null);
    setIsLoading(false);
  };

  return (
    <div className="app">
      <header className="app-header">
        <div className="container">
          <div className="header-content">
            <div className="logo">
              <div className="logo-icon">🎯</div>
              <h1>Object Detection AI</h1>
            </div>
            <p className="subtitle">
              Advanced object detection powered by YOLOv11
            </p>
          </div>
        </div>
      </header>

      <main className="app-main">
        <div className="container">
          <div className="upload-section">
            <ImageUpload
              onDetectionStart={handleDetectionStart}
              onDetectionComplete={handleDetectionComplete}
              onDetectionError={handleDetectionError}
              isLoading={isLoading}
              onReset={handleReset}
              hasResult={!!detectionResult}
            />
          </div>

          {isLoading && (
            <div className="loading-section">
              <div className="loading-spinner"></div>
              <p>Analyzing your image...</p>
            </div>
          )}

          {error && (
            <div className="error-section">
              <div className="error-icon">⚠️</div>
              <h3>Processing Failed</h3>
              <p>{error}</p>
            </div>
          )}

          {detectionResult && !isLoading && (
            <div className="result-section">
              <div className="result-header">
                <div className="success-icon">✅</div>
                <h3>Detection Complete</h3>
              </div>
              <div className="result-content">
                <div className="result-image">
                  <img 
                    src={detectionResult.processedImageUrl || detectionResult.imageUrl} 
                    alt="Detection Result" 
                    className="result-img"
                  />
                </div>
                <div className="result-info">
                  <h4>Analysis Summary</h4>
                  <div className="info-grid">
                    <div className="info-item">
                      <span className="info-label">Image Size</span>
                      <span className="info-value">
                        {detectionResult.width} × {detectionResult.height}
                      </span>
                    </div>
                    <div className="info-item">
                      <span className="info-label">Objects Found</span>
                      <span className="info-value">{detectionResult.objectCount}</span>
                    </div>
                    <div className="info-item">
                      <span className="info-label">Processing Time</span>
                      <span className="info-value">{detectionResult.processingTime}ms</span>
                    </div>
                  </div>
                  
                  {detectionResult.objects && detectionResult.objects.length > 0 ? (
                    <div className="detected-objects">
                      <h5>Detected Objects</h5>
                      <div className="objects-list">
                        {detectionResult.objects.map((obj, index) => (
                          <div key={index} className="object-item">
                            <span className="object-name">{obj.name}</span>
                            <span className="object-confidence">
                              {Math.round(obj.confidence * 100)}%
                            </span>
                          </div>
                        ))}
                      </div>
                    </div>
                  ) : (
                    <div className="detected-objects">
                      <h5>No Objects Detected</h5>
                      <p style={{color: '#64748b', fontSize: '14px', margin: 0}}>
                        No objects were found above the confidence threshold.
                      </p>
                    </div>
                  )}
                </div>
              </div>
            </div>
          )}
        </div>
      </main>

      <footer className="app-footer">
        <div className="container">
          <p>© 2024 Object Detection AI. Built with YOLOv11 and FastAPI.</p>
        </div>
      </footer>
    </div>
  );
}

export default App;