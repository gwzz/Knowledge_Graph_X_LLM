export interface MedicalRecord {
  id?: number;
  name: string;
  describes?: string;
  symptom?: string;
  seek_medical_attention_immediately?: number;
  follow_up?: number;
  follow_up_describe?: string;
  type_ab?: string;
  is_emergency?: number;
  urgency_level?: number;
}

export interface ApiResponse<T> {
  success: boolean;
  data?: T;
  message?: string;
  error?: string;
}