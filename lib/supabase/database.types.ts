export type Json =
    | string
    | number
    | boolean
    | null
    | { [key: string]: Json | undefined }
    | Json[]

export interface Database {
    public: {
        Tables: {
            user_profiles: {
                Row: {
                    id: string
                    email: string
                    full_name: string | null
                    specialty: string | null
                    organization: string | null
                    profile_picture_url: string | null
                    created_at: string | null
                    updated_at: string | null
                }
                Insert: {
                    id: string
                    email: string
                    full_name?: string | null
                    specialty?: string | null
                    organization?: string | null
                    profile_picture_url?: string | null
                    created_at?: string | null
                    updated_at?: string | null
                }
                Update: {
                    id?: string
                    email?: string
                    full_name?: string | null
                    specialty?: string | null
                    organization?: string | null
                    profile_picture_url?: string | null
                    created_at?: string | null
                    updated_at?: string | null
                }
            }
            queries: {
                Row: {
                    id: string
                    user_id: string
                    query_text: string
                    category: string | null
                    created_at: string | null
                    updated_at: string | null
                }
                Insert: {
                    id?: string
                    user_id: string
                    query_text: string
                    category?: string | null
                    created_at?: string | null
                    updated_at?: string | null
                }
                Update: {
                    id?: string
                    user_id?: string
                    query_text?: string
                    category?: string | null
                    created_at?: string | null
                    updated_at?: string | null
                }
            }
            answers: {
                Row: {
                    id: string
                    query_id: string
                    user_id: string
                    answer_text: string
                    citations: Json | null
                    created_at: string | null
                }
                Insert: {
                    id?: string
                    query_id: string
                    user_id: string
                    answer_text: string
                    citations?: Json | null
                    created_at?: string | null
                }
                Update: {
                    id?: string
                    query_id?: string
                    user_id?: string
                    answer_text?: string
                    citations?: Json | null
                    created_at?: string | null
                }
            }
            vzp_medicines: {
                Row: {
                    id: string
                    name: string
                    inn: string | null
                    atc_code: string | null
                    coverage_type: string | null
                    coverage_percentage: number | null
                    indications: Json | null
                    alternatives: Json | null
                    created_at: string | null
                    updated_at: string | null
                }
                Insert: {
                    id?: string
                    name: string
                    inn?: string | null
                    atc_code?: string | null
                    coverage_type?: string | null
                    coverage_percentage?: number | null
                    indications?: Json | null
                    alternatives?: Json | null
                    created_at?: string | null
                    updated_at?: string | null
                }
                Update: {
                    id?: string
                    name?: string
                    inn?: string | null
                    atc_code?: string | null
                    coverage_type?: string | null
                    coverage_percentage?: number | null
                    indications?: Json | null
                    alternatives?: Json | null
                    created_at?: string | null
                    updated_at?: string | null
                }
            }
            user_preferences: {
                Row: {
                    id: string
                    user_id: string
                    theme: string | null
                    language: string | null
                    notifications_enabled: boolean | null
                    email_digest: boolean | null
                    created_at: string | null
                    updated_at: string | null
                }
                Insert: {
                    id?: string
                    user_id: string
                    theme?: string | null
                    language?: string | null
                    notifications_enabled?: boolean | null
                    email_digest?: boolean | null
                    created_at?: string | null
                    updated_at?: string | null
                }
                Update: {
                    id?: string
                    user_id?: string
                    theme?: string | null
                    language?: string | null
                    notifications_enabled?: boolean | null
                    email_digest?: boolean | null
                    created_at?: string | null
                    updated_at?: string | null
                }
            }
        }
    }
}
