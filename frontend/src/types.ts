export interface Fan {
  id: string
  name: string
  email: string
  city: string
  total_spend_cents: number
  attendance_count: number
  last_purchase_days_ago: number
  genres: string[]
  email_status: string
}

export interface Segment {
  name: string
  count: number
  fan_ids: string[]
}

export interface Campaign {
  segment: string
  fan_count: number
  subject_line: string
  email_body: string
  sms_body: string
  send_estimate: number
  projected_open_rate: number
  ai_generated?: boolean
  source?: 'claude' | 'database' | 'template'
}

export interface CustomFilter {
  genres?: string[]
  cities?: string[]
  min_spend_cents?: number
  max_spend_cents?: number
  min_attendance?: number
  max_last_purchase_days?: number
  email_status?: string
  radius_miles?: number
  event_lat?: number
  event_lng?: number
}
