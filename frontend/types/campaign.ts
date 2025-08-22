export interface Campaign {
  id: string
  name: string
  subject: string
  content?: string
  status: 'draft' | 'scheduled' | 'sending' | 'sent' | 'archived'
  audience_id?: string
  template_id?: string
  scheduled_at?: string
  sent_at?: string
  settings: CampaignSettings
  analytics?: CampaignAnalytics
  created_at: string
  updated_at: string
}

export interface CampaignSettings {
  from_name: string
  from_email: string
  reply_to?: string
  subject_line?: string
  preview_text?: string
  tracking_enabled: boolean
  unsubscribe_enabled: boolean
  resend_to_unopened: boolean
  resend_delay_hours: number
}

export interface CampaignAnalytics {
  sent: number
  delivered: number
  opened: number
  clicked: number
  bounced: number
  unsubscribed: number
  spam_reports: number
  delivery_rate: number
  open_rate: number
  click_rate: number
  bounce_rate: number
  unsubscribe_rate: number
}

export interface CampaignCreate {
  name: string
  subject: string
  audience_id?: string
  template_id?: string
  scheduled_at?: string
  settings: Partial<CampaignSettings>
}

export interface CampaignUpdate {
  name?: string
  subject?: string
  content?: string
  audience_id?: string
  template_id?: string
  scheduled_at?: string
  settings?: Partial<CampaignSettings>
}

export interface CampaignListResponse {
  campaigns: Campaign[]
  pagination: PaginationInfo
}

export interface PaginationInfo {
  page: number
  limit: number
  total: number
  pages: number
}

export interface CampaignFilters {
  status?: string
  search?: string
  date_from?: string
  date_to?: string
  audience_id?: string
}

export interface CampaignSchedule {
  scheduled_at: string
}

export interface CampaignSendResponse {
  message: string
  estimated_recipients: number
}
