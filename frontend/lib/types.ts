export interface TaxonomyCode {
  code: string;
  value: string;
  label: string;
  covered: boolean;
}

export interface PatientStateForm {
  in_counter_queue: boolean;
  in_nursing_queue: boolean;
  in_consultation_queue: boolean;
  counters_open_idle: number;
  counters_busy: number;
  nurses_present_idle: number;
  nurses_busy: number;
  room_vacant: boolean;
  clinician_checked_in: boolean;
  clinician_with_another_patient: boolean;
  sent_to_diagnostics: boolean;
  diagnostics_return_recorded: boolean;
  diagnostics_returned_within_sla: boolean;
  clinically_finished: boolean;
  records_cleared: boolean;
  transition_missing: boolean;
}

export interface ClassifyResponse {
  code: string | null;
  label: string | null;
  explanation: string;
  is_data_gap: boolean;
}

export interface CoverageResponse {
  total_coherent: number;
  total_raw: number;
  observed: number;
  data_gaps: number;
  coverage: number;
  residual_share: number;
  counts: Record<string, number>;
}
