import axios, { AxiosInstance, AxiosRequestConfig, AxiosResponse } from 'axios';
import { toast } from 'react-hot-toast';

// API Response Types
export interface ApiResponse<T = any> {
  success: boolean;
  data?: T;
  error?: string;
  message?: string;
}

export interface PaginatedResponse<T> {
  data: T[];
  pagination: {
    page: number;
    limit: number;
    total: number;
    totalPages: number;
  };
}

// Create axios instance
const api: AxiosInstance = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1',
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor
api.interceptors.request.use(
  (config) => {
    // Add auth token if available
    const token = localStorage.getItem('auth_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor
api.interceptors.response.use(
  (response: AxiosResponse<ApiResponse>) => {
    return response;
  },
  (error) => {
    const { response } = error;
    
    if (response?.status === 401) {
      // Handle unauthorized access
      localStorage.removeItem('auth_token');
      localStorage.removeItem('user');
      window.location.href = '/auth/login';
      toast.error('Session expired. Please login again.');
    } else if (response?.status === 403) {
      toast.error('Access denied. You do not have permission to perform this action.');
    } else if (response?.status === 404) {
      toast.error('Resource not found.');
    } else if (response?.status === 422) {
      // Handle validation errors
      const errors = response.data?.error || 'Validation failed';
      toast.error(errors);
    } else if (response?.status >= 500) {
      toast.error('Server error. Please try again later.');
    } else {
      toast.error(response?.data?.error || 'An error occurred');
    }
    
    return Promise.reject(error);
  }
);

// API Methods
export const apiClient = {
  // Auth endpoints
  auth: {
    login: (credentials: { email: string; password: string }) =>
      api.post<ApiResponse<{ token: string; user: any }>>('/auth/login', credentials),
    
    register: (userData: { firstName: string; lastName: string; email: string; password: string }) =>
      api.post<ApiResponse<{ token: string; user: any }>>('/auth/register', userData),
    
    logout: () => api.post<ApiResponse>('/auth/logout'),
    
    refresh: () => api.post<ApiResponse<{ token: string }>>('/auth/refresh'),
    
    forgotPassword: (email: string) =>
      api.post<ApiResponse>('/auth/forgot-password', { email }),
    
    resetPassword: (token: string, password: string) =>
      api.post<ApiResponse>('/auth/reset-password', { token, password }),
    
    verifyEmail: (token: string) =>
      api.post<ApiResponse>('/auth/verify-email', { token }),
  },

  // User endpoints
  users: {
    getProfile: () => api.get<ApiResponse<any>>('/users/profile'),
    
    updateProfile: (data: Partial<any>) =>
      api.put<ApiResponse<any>>('/users/profile', data),
    
    changePassword: (data: { currentPassword: string; newPassword: string }) =>
      api.put<ApiResponse>('/users/change-password', data),
    
    uploadAvatar: (file: File) => {
      const formData = new FormData();
      formData.append('avatar', file);
      return api.post<ApiResponse<{ url: string }>>('/users/avatar', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });
    },
  },

  // Campaign endpoints
  campaigns: {
    getAll: (params?: { page?: number; limit?: number; status?: string; type?: string }) =>
      api.get<ApiResponse<PaginatedResponse<any>>>('/campaigns', { params }),
    
    getById: (id: string) => api.get<ApiResponse<any>>(`/campaigns/${id}`),
    
    create: (data: any) => api.post<ApiResponse<any>>('/campaigns', data),
    
    update: (id: string, data: Partial<any>) =>
      api.put<ApiResponse<any>>(`/campaigns/${id}`, data),
    
    delete: (id: string) => api.delete<ApiResponse>(`/campaigns/${id}`),
    
    send: (id: string) => api.post<ApiResponse>(`/campaigns/${id}/send`),
    
    duplicate: (id: string) => api.post<ApiResponse<any>>(`/campaigns/${id}/duplicate`),
    
    getAnalytics: (id: string) => api.get<ApiResponse<any>>(`/campaigns/${id}/analytics`),
  },

  // Template endpoints
  templates: {
    getAll: (params?: { page?: number; limit?: number; category?: string; isPublic?: boolean }) =>
      api.get<ApiResponse<PaginatedResponse<any>>>('/templates', { params }),
    
    getById: (id: string) => api.get<ApiResponse<any>>(`/templates/${id}`),
    
    create: (data: any) => api.post<ApiResponse<any>>('/templates', data),
    
    update: (id: string, data: Partial<any>) =>
      api.put<ApiResponse<any>>(`/templates/${id}`, data),
    
    delete: (id: string) => api.delete<ApiResponse>(`/templates/${id}`),
  },

  // AI Generation endpoints
  ai: {
    generateContent: (data: any) => api.post<ApiResponse<any>>('/ai/generate', data),
    
    generateSubject: (data: any) => api.post<ApiResponse<any>>('/ai/generate-subject', data),
    
    analyzeContent: (data: any) => api.post<ApiResponse<any>>('/ai/analyze', data),
    
    suggestImprovements: (data: any) => api.post<ApiResponse<any>>('/ai/suggest', data),
  },

  // Recipients endpoints
  recipients: {
    getAll: (params?: { page?: number; limit?: number; status?: string }) =>
      api.get<ApiResponse<PaginatedResponse<any>>>('/recipients', { params }),
    
    create: (data: any) => api.post<ApiResponse<any>>('/recipients', data),
    
    bulkCreate: (data: any[]) => api.post<ApiResponse<any[]>>('/recipients/bulk', data),
    
    update: (id: string, data: Partial<any>) =>
      api.put<ApiResponse<any>>(`/recipients/${id}`, data),
    
    delete: (id: string) => api.delete<ApiResponse>(`/recipients/${id}`),
    
    import: (file: File) => {
      const formData = new FormData();
      formData.append('file', file);
      return api.post<ApiResponse<{ imported: number; errors: any[] }>>('/recipients/import', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });
    },
  },

  // File upload endpoints
  files: {
    upload: (file: File, type: 'image' | 'document' = 'image') => {
      const formData = new FormData();
      formData.append('file', file);
      formData.append('type', type);
      return api.post<ApiResponse<{ url: string; filename: string }>>('/files/upload', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });
    },
    
    delete: (filename: string) => api.delete<ApiResponse>(`/files/${filename}`),
  },

  // Notifications endpoints
  notifications: {
    getAll: (params?: { page?: number; limit?: number; isRead?: boolean }) =>
      api.get<ApiResponse<PaginatedResponse<any>>>('/notifications', { params }),
    
    markAsRead: (id: string) => api.put<ApiResponse>(`/notifications/${id}/read`),
    
    markAllAsRead: () => api.put<ApiResponse>('/notifications/read-all'),
    
    delete: (id: string) => api.delete<ApiResponse>(`/notifications/${id}`),
  },

  // Settings endpoints
  settings: {
    get: () => api.get<ApiResponse<any>>('/settings'),
    
    update: (data: any) => api.put<ApiResponse<any>>('/settings', data),
  },
};

export default apiClient;
