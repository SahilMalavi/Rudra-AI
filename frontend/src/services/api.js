import axios from "axios";

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL,
  timeout: 60000, // 60 second timeout
});

// Request interceptor for logging
api.interceptors.request.use(
  (config) => {
    console.log(`[API] ${config.method?.toUpperCase()} ${config.url}`);
    return config;
  },
  (error) => {
    console.error("[API] Request error:", error);
    return Promise.reject(error);
  },
);

// Response interceptor for error handling
api.interceptors.response.use(
  (response) => {
    console.log(`[API] Response from ${response.config.url}:`, response.status);
    return response;
  },
  (error) => {
    console.error("[API] Response error:", error);

    // Handle different error types
    if (error.response) {
      // Server responded with error status
      console.error(
        "[API] Server error:",
        error.response.status,
        error.response.data,
      );
    } else if (error.request) {
      // Request was made but no response received
      console.error("[API] No response received:", error.request);
    } else {
      // Error in request configuration
      console.error("[API] Request setup error:", error.message);
    }

    return Promise.reject(error);
  },
);

export const chatAPI = {
  sendMessage: async (message) => {
    if (!message || typeof message !== "string") {
      throw new Error("Invalid message: must be a non-empty string");
    }

    console.log("[chatAPI] Sending message:", message.substring(0, 50) + "...");

    const formData = new FormData();
    formData.append("message", message);

    try {
      const response = await api.post("/chat", formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });

      console.log("[chatAPI] Response received");
      return response.data;
    } catch (error) {
      console.error("[chatAPI] Error sending message:", error.message);
      throw new Error(
        error.response?.data?.error ||
          error.message ||
          "Failed to send message. Please try again.",
      );
    }
  },

  sendImageMessage: async (prompt, imageFile) => {
    if (!prompt || typeof prompt !== "string") {
      throw new Error("Invalid prompt: must be a non-empty string");
    }

    if (!imageFile || !(imageFile instanceof File)) {
      throw new Error("Invalid image: must be a File object");
    }

    if (!imageFile.type.startsWith("image/")) {
      throw new Error("Invalid file type: must be an image");
    }

    console.log(
      "[chatAPI] Sending image message:",
      prompt.substring(0, 50) + "...",
      "File:",
      imageFile.name,
    );

    const formData = new FormData();
    formData.append("prompt", prompt);
    formData.append("file", imageFile);

    try {
      const response = await api.post("/chat-with-image", formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });

      console.log("[chatAPI] Image response received");
      return response.data;
    } catch (error) {
      console.error("[chatAPI] Error sending image message:", error.message);
      throw new Error(
        error.response?.data?.error ||
          error.message ||
          "Failed to process image. Please try again.",
      );
    }
  },

  sendPDFMessage: async (prompt, pdfFile) => {
    if (!prompt || typeof prompt !== "string") {
      throw new Error("Invalid prompt: must be a non-empty string");
    }

    if (!pdfFile || !(pdfFile instanceof File)) {
      throw new Error("Invalid PDF: must be a File object");
    }

    if (pdfFile.type !== "application/pdf") {
      throw new Error("Invalid file type: must be a PDF");
    }

    console.log(
      "[chatAPI] Sending PDF message:",
      prompt.substring(0, 50) + "...",
      "File:",
      pdfFile.name,
    );

    const formData = new FormData();
    formData.append("prompt", prompt);
    formData.append("file", pdfFile);

    try {
      const response = await api.post("/chat-with-pdf", formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });

      console.log("[chatAPI] PDF response received");
      return response.data;
    } catch (error) {
      console.error("[chatAPI] Error sending PDF message:", error.message);
      throw new Error(
        error.response?.data?.error ||
          error.message ||
          "Failed to process PDF. Please try again.",
      );
    }
  },

  resetChat: async () => {
    console.log("[chatAPI] Resetting chat");

    try {
      const response = await api.post("/reset-chat");
      console.log("[chatAPI] Reset response received");
      return response.data;
    } catch (error) {
      console.error("[chatAPI] Error resetting chat:", error.message);
      throw new Error(
        error.response?.data?.error ||
          error.message ||
          "Failed to reset chat. Please try again.",
      );
    }
  },
};

export default api;
