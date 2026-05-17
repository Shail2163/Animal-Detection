import React, { useState, useRef } from 'react';
import { Upload, Image as ImageIcon, X, Zap, RefreshCw } from 'lucide-react';
import { detectObjects } from './api';

const ImageUpload = ({ 
  onDetectionStart, 
  onDetectionComplete, 
  onDetectionError, 
  isLoading,
  onReset,
  hasResult 
}) => {
  const [selectedImage, setSelectedImage] = useState(null);
  const [dragActive, setDragActive] = useState(false);
  const fileInputRef = useRef(null);

  const handleDrag = (e) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true);
    } else if (e.type === "dragleave") {
      setDragActive(false);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleFile(e.dataTransfer.files[0]);
    }
  };

  const handleFile = (file) => {
    if (file && file.type.startsWith('image/')) {
      setSelectedImage(file);
      if (hasResult && onReset) {
        onReset();
      }
    } else {
      onDetectionError('Please select a valid image file (JPG, PNG, WEBP).');
    }
  };

  const handleFileInput = (e) => {
    if (e.target.files && e.target.files[0]) {
      handleFile(e.target.files[0]);
    }
  };

  const handleUpload = async () => {
    if (!selectedImage) {
      onDetectionError('Please select an image first.');
      return;
    }

    onDetectionStart();

    try {
      const result = await detectObjects(selectedImage);
      onDetectionComplete(result);
    } catch (error) {
      onDetectionError(error.message || 'Failed to process image. Please try again.');
    }
  };

  const clearImage = () => {
    setSelectedImage(null);
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
    if (hasResult && onReset) {
      onReset();
    }
  };

  const formatFileSize = (bytes) => {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(1)) + ' ' + sizes[i];
  };

  return (
    <div className="image-upload">
      <div className="upload-container">
        {!selectedImage ? (
          <div
            className={`upload-area ${dragActive ? 'drag-active' : ''}`}
            onDragEnter={handleDrag}
            onDragLeave={handleDrag}
            onDragOver={handleDrag}
            onDrop={handleDrop}
            onClick={() => fileInputRef.current?.click()}
          >
            <div className="upload-content">
              <div className="upload-icon">
                <Upload size={40} />
              </div>
              <h3>Select an Image</h3>
              <p>Drag and drop your image here, or click to browse</p>
              <div className="upload-formats">
                <span>JPG, PNG, WEBP up to 10MB</span>
              </div>
            </div>
            <input
              ref={fileInputRef}
              type="file"
              accept="image/*"
              onChange={handleFileInput}
              style={{ display: 'none' }}
            />
          </div>
        ) : (
          <div className="image-preview">
            <div className="preview-header">
              <div className="preview-info">
                <ImageIcon size={20} />
                <div className="file-info">
                  <span className="file-name">{selectedImage.name}</span>
                  <span className="file-size">{formatFileSize(selectedImage.size)}</span>
                </div>
              </div>
              <button 
                className="clear-button"
                onClick={clearImage}
                disabled={isLoading}
                title="Remove image"
              >
                <X size={16} />
              </button>
            </div>
            
            <div className="preview-image">
              <img 
                src={URL.createObjectURL(selectedImage)} 
                alt="Selected image preview" 
                className="preview-img"
              />
            </div>
            
            <div className="preview-actions">
              <button 
                className="upload-button"
                onClick={handleUpload}
                disabled={isLoading}
              >
                {isLoading ? (
                  <>
                    <div className="button-spinner"></div>
                    Analyzing...
                  </>
                ) : (
                  <>
                    <Zap size={18} />
                    Detect Objects
                  </>
                )}
              </button>
              
              <button 
                className="change-button"
                onClick={() => fileInputRef.current?.click()}
                disabled={isLoading}
              >
                <RefreshCw size={16} />
                Change Image
              </button>
            </div>
            
            <input
              ref={fileInputRef}
              type="file"
              accept="image/*"
              onChange={handleFileInput}
              style={{ display: 'none' }}
            />
          </div>
        )}
      </div>
      
      <div className="upload-tips">
        <h4>Tips for Best Results</h4>
        <ul>
          <li>Use clear, well-lit images</li>
          <li>Ensure objects are clearly visible</li>
          <li>Higher resolution images work better</li>
          <li>Avoid blurry or heavily distorted images</li>
        </ul>
      </div>
    </div>
  );
};

export default ImageUpload;