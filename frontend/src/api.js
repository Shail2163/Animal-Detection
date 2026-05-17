import axios from 'axios';

// API Configuration
const API_BASE_URL = 'http://localhost:8000';

// Create axios instance with default config
const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000, // 30 seconds timeout
  headers: {
    'Content-Type': 'multipart/form-data',
  },
});

// Request interceptor for logging
api.interceptors.request.use(
  (config) => {
    console.log('API Request:', config.method?.toUpperCase(), config.url);
    return config;
  },
  (error) => {
    console.error('API Request Error:', error);
    return Promise.reject(error);
  }
);

// Response interceptor for error handling
api.interceptors.response.use(
  (response) => {
    console.log('API Response:', response.status, response.data);
    return response;
  },
  (error) => {
    console.error('API Response Error:', error.response?.status, error.response?.data);
    
    // Handle different error types
    if (error.code === 'ECONNABORTED') {
      throw new Error('Request timeout. Please try again.');
    }
    
    if (error.response?.status === 413) {
      throw new Error('File too large. Please use a smaller image.');
    }
    
    if (error.response?.status === 415) {
      throw new Error('Unsupported file type. Please use JPG, PNG, or WEBP.');
    }
    
    if (error.response?.status >= 500) {
      throw new Error('Server error. Please try again later.');
    }
    
    if (error.response?.status === 404) {
      throw new Error('API endpoint not found. Please check server configuration.');
    }
    
    throw new Error(error.response?.data?.message || 'An unexpected error occurred.');
  }
);

/**
 * Upload image and get object detection results
 * @param {File} imageFile - The image file to process
 * @returns {Promise<Object>} Detection results
 */
export const detectObjects = async (imageFile) => {
  try {
    // Validate file
    if (!imageFile) {
      throw new Error('No image file provided');
    }
    
    if (!imageFile.type.startsWith('image/')) {
      throw new Error('File must be an image');
    }
    
    // Check file size (10MB limit)
    const maxSize = 10 * 1024 * 1024; // 10MB
    if (imageFile.size > maxSize) {
      throw new Error('File size must be less than 10MB');
    }
    
    // Create FormData
    const formData = new FormData();
    formData.append('file', imageFile);
    
    // Record start time for processing time calculation
    const startTime = Date.now();
    
    // Make API request
    const response = await api.post('/predict', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    
    const processingTime = Date.now() - startTime;
    
    // Process response - FIXED TO MATCH ACTUAL BACKEND RESPONSE
    const result = response.data;
    console.log('Backend response:', result); // Debug log

    // Add this line right after: const result = response.data;
console.log('BACKEND RESPONSE:', JSON.stringify(result, null, 2));

    // Add these lines right after "const result = response.data;"
    console.log('=== DEBUG INFO ===');
    console.log('Full backend response:', result);
    console.log('total_objects:', result.total_objects);
    console.log('image_info:', result.image_info);
    console.log('detections:', result.detections);
    console.log('==================');
    
    // Map backend response to frontend expected format
    const detectionResult = {
      success: result.success || true,
      processingTime,
      // FIXED: Use correct field names from backend response
      width: result.image_info?.width || 0,
      height: result.image_info?.height || 0,
      objectCount: result.total_objects || 0,
      objects: (result.detections || []).map(det => ({
        name: det.class,
        confidence: det.confidence
      })),
      // FIXED: Map detections to expected objects format
      objects: result.detections?.map(detection => ({
        name: detection.class,
        confidence: detection.confidence,
        bbox: detection.bbox,
        class_id: detection.class_id
      })) || [],
      // Use the base64 image from backend if available, otherwise original
      imageUrl: result.annotated_image || URL.createObjectURL(imageFile),
      processedImageUrl: result.annotated_image || URL.createObjectURL(imageFile),
      // Additional data from backend
      detections: result.detections || [],
      rawResponse: result // Keep raw response for debugging
    };
    
    console.log('Processed detection result:', detectionResult); // Debug log
    
    return detectionResult;
    
  } catch (error) {
    console.error('Detection error:', error);
    throw error;
  }
};

/**
 * Check if the API server is running
 * @returns {Promise<boolean>} True if server is accessible
 */
export const checkServerHealth = async () => {
  try {
    const response = await api.get('/health');
    return response.status === 200;
  } catch (error) {
    console.warn('Server health check failed:', error.message);
    return false;
  }
};

/**
 * Get server information
 * @returns {Promise<Object>} Server info
 */
export const getServerInfo = async () => {
  try {
    const response = await api.get('/');
    return response.data;
  } catch (error) {
    console.warn('Failed to get server info:', error.message);
    return null;
  }
};

// Export the configured axios instance for custom requests
export default api;